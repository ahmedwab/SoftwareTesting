# Import BeautifulSoup to read an XML file
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import pathlib
import statistics as sc

#XML content
content = []

#Path of python file
path = pathlib.Path().absolute()
reportFiles = os.listdir(path)

#Report Count
number_files = 0

#Count of bugs
bugCount = 0

#Dictionary of a report's status

dictionaryStatus = {
    "In Progress": 0,
    "Closed": 0,
    "Resolved": 0,
    "Open": 0,
    "Reopened": 0,
    "Patch Available": 0,


}

# List of Turnaround time for resolving an issue

turnaroundTime = []

# Function to analyze each indvidual report

def analyzeReport(fileName):
    with open(fileName, encoding="utf8", errors='ignore')as file:
        global number_files
        number_files +=1
        # Read each of the xml files
        content = file.readlines()
        # Combine the lines in the list into a string
        content = "".join(content)
        bs_content = bs(content, "lxml")

    try:
        bugType = bs_content.find("type")
    except TypeError:
        bugType = None

    try:
        resolution = bs_content.find("resolution")
    except TypeError:
            resolution = None

    try:
       status = bs_content.find("status")
    except TypeError:
            status = None

    #check if report is a bug
    if bugType!= None and bugType.string == "Bug":
        global bugCount
        bugCount+=1
        # check if resolution is closed or fixed
        if resolution != None:
            if resolution.string == "Fixed" or resolution.string == "Closed":
                dateCreated = datetime.strptime(bs_content.find("created").string,"%a, %d %b %Y %H:%M:%S %z")
                dateResolved = datetime.strptime(bs_content.find("resolved").string, "%a, %d %b %Y %H:%M:%S %z")
                timeTaken = dateResolved - dateCreated
                timeTaken = timeTaken.days
                turnaroundTime.append(timeTaken)
             #check status

            if status !=None:
                 status = status.string
            if status == 'Closed':
                 dictionaryStatus["Closed"] += 1

            if status == 'Open':
                dictionaryStatus["Open"] += 1

            if status == 'Patch Available':
                 dictionaryStatus["Patch Available"] += 1

            if status == 'Resolved':
                 dictionaryStatus["Resolved"] += 1

            if status == 'Reopened':
                dictionaryStatus["Reopened"] += 1

            if status == 'In Progress':
                dictionaryStatus["In Progress"] += 1


    

  

    
# Iterator to assess different reports
for file in reportFiles:
    if file == "search.py":
        continue
    analyzeReport(file)


#Results
print ("Number of Reports:", number_files-1)
print ("Number of Bug reports:", bugCount)
print(dictionaryStatus)
print("Analysis of Fixed or Closed bugs:")
print('Fastest fix(days):', min(turnaroundTime))
print('Slowest fix(days):', max(turnaroundTime))
print('Median fix(days):', sc.median(turnaroundTime))
print('Average fix(days):', round(sc.mean(turnaroundTime),2))



