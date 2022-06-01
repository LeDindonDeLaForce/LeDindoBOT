import logging
import os
import mariadb
import logging
from twitchio.ext import routines
import time


commands = {}
params = {
    'user':'sgbd_user',
    'password':'sgbd_password'
    'host':'SGBD host IP or FQDN',
    'port':3306,
    'database':'TWITCH_BOT'
}

def init_commands():
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    try:
	# connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT * FROM commands"
        )
        commands_raw = cur.fetchall()

        for command in commands_raw:
            commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def find_command(message):
    command = message.content.split()[0]
    channel = message.author.channel.name

    command_text = commands.get((command, channel))

    return command_text


def add_command(command, channel, text):
    commands[(command, channel)] = text

    # Now adds it to db
    conn = None
    try:
        # connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""INSERT INTO commands VALUES (%s, %s, %s)""",
            (command, channel, text)
        )

        conn.commit()

        for command in commands_raw:
            logging.info(command[1])
            commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def edit_command(command, channel, text):
    commands[(command, channel)] = text

    # Now updates db
    conn = None
    try:
        # connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""UPDATE commands SET text=%s WHERE command=%s AND channel=%s """,
            (command, channel, text)
        )

        conn.commit()

        for command in commands_raw:
            logging.info(command[1])
            commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def remove_command(command, channel):
    commands.pop((command, channel))

    # Now updates db
    conn = None
    try:
        # connect to the MariaDB server
        logging.info('Initializing commands')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"DELETE FROM commands WHERE command='{command}' AND channel='{channel}'"
        )

        conn.commit()

        for command in commands_raw:
            logging.info(command[1])
            commands[(command[0], command[1])] = command[2]

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')

### ROUTINES ###

### ROUTINES ###
def routine_factory(channel, seconds, minutes, hours, routine_text):
    @routines.routine(seconds=seconds, minutes=minutes, hours=hours, wait_first=False)
    async def temp_routine():
        await channel.send(routine_text)

    return temp_routine


def add_routine(
        channel, name, seconds, minutes,
        hours, routine_text):

    # Now adds it to db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Adding new routine to db')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""INSERT INTO routines VALUES (%s, %s, %s, %s, %s, %s)""",
            (channel, name, seconds, minutes, hours, routine_text)
        )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def init_routines(bot):
    """ Connects to the MariaDB database server and initializes the custom commands dict """
    conn = None
    routines_db = {}
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Initializing routines')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT * FROM routines"
        )
        routines_raw = cur.fetchall()


        for routine in routines_raw:
            chan = bot.get_channel(routine[0])
            routines_db[routine[0] + '_' + routine[1]] = routine_factory(
                channel=chan,
                seconds=int(routine[2]),
                minutes=int(routine[3]),
                hours=int(routine[4]),
                routine_text=routine[5]
            )
            routines_db[routine[0] + '_' + routine[1]].start()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
        return routines_db


def remove_routine(channel, name):
    # Now updates db
    conn = None
    try:
        # read connection parameters
        #params = config(filename='database_commands.ini')

        # connect to the MariaDB server
        logging.info('Removing routine from db')
        conn = mariadb.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"DELETE FROM routines WHERE channel=%s AND name=%s",
            (channel, name)
        )

        conn.commit()

        # close the communication with the MariaDB
        cur.close()

    except (Exception, mariadb.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
