def cleandata(data): #this script is here to clean data from additionnal character, to make it usable as a list
    newdata = []
    for sample in data:
        tempdata = str(sample)
        tempdata = tempdata.replace('(','')
        tempdata = tempdata.replace(')','')
        tempdata = tempdata.replace(',','')
        tempdata = tempdata.replace('\'','')
        newdata.append(tempdata)

    return newdata
