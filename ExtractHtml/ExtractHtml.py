#! Insert newline in html
import sys
import logging
import time
import datetime
import re
from bs4 import BeautifulSoup
import json

#
#<span class="lecture__item__link__name">AWS - 10,000 Foot Overview Part 4</span> </span> 
#<span class="lecture__item__link__time mr20" ng-style="item.length ? {} : {opacity: 0}">6:59</span> <!----><span ng-click="toggleProgress($event, item)" ng-class="{&#39;disabled&#39;: progressDisabled(item)}" ng-if="!(item.type === &#39;quiz&#39; &amp;&amp; item.quizType === &#39;practice-test&#39;)" class="tooltip-container lecture__item__link__icon lecture__item__link__progress"> <i class="bold udi udi-check"></i> <i class="icon-spin udi udi-spinner"></i> <!----> </span><!----> </a> <ul ng-show="resources.length &gt; 0" ng-class="isFreePreviewer ? &#39;disabled&#39; : &#39;&#39;" class="lecture__resources ng-hide" resources="item.supplementaryAssets" api-resource="SupplementaryAsset" api-params="{courseId: section.courseId, lectureId: item.id}"> <!----> <a class="resources__more-button ng-hide" ng-click="limit = limit + 10" ng-show="resources.length &gt; 3 &amp;&amp; limit &lt; resources.length" translate=""><span>Show more (-3)</span></a> </ul> </li><!----><li class="lecture__item  comp...
#
#<span class="cur-section" translate-comment="Example: Section 1" ng-if="section.isPublished"> <span translate=""><span>Section:</span></span> 2 </span><!----> <!----> 

name = "lecture__item__link__name"
duration = "lecture__item__link__time mr20"
sectiontitle = "curriculum-navigation__section__title"

formattedData = ""
searchString="<span class="
counter = 0
placeholder = 0
unformattedSize = 0
formattedSize = 0
viewerLength = 20
logfilename = ""
section="Section {}: {}\t\t\n"
topics="\t{} {}\t{}\n"
exceldata = ""

ts = time.time()
lblTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-c%m-%d %H:%M:%S')
logTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')
logfilename = logTimestamp+'ExtractHtml.log'
logging.basicConfig(filename=logfilename,level=logging.DEBUG,format='%(asctime)s %(message)s' )
logging.info("#########################################################")
logging.info("#################### START EXECUTION at %s ####################", lblTimestamp)


with open("Syllabus.html", "r") as sourceFile:
    bulkdata = sourceFile.read()
unformattedSize =  len(bulkdata)
logging.debug("Source file contains %d characters", unformattedSize)
counter = bulkdata.count(searchString)
logging.debug("Token |%s| was found %d times.", searchString, counter)

soup = BeautifulSoup(bulkdata, "html.parser")


#find a list of all div elements
divsSectionTitles = soup.find_all('div', {'class' : sectiontitle})
sectionslist = [div.get_text() for div in divsSectionTitles]
for index in range(len(divsSectionTitles)):
    logging.info("\t Section %d: \t %s", index+1, sectionslist[index])
    exceldata+=section.format(index+1, sectionslist[index])


# find a list of all span elements
spansName = soup.find_all('span', {'class' : name})
logging.debug ("Found %d names", len(spansName))
spansDuration = soup.find_all('span', {'class' : duration})
logging.debug ("Found %d durations", len(spansDuration))

# create a list of lines corresponding to element texts
nameslist = [span.get_text() for span in spansName]
durationlist = [span.get_text() for span in spansDuration]

for index in range(len(nameslist)):
    if (len(durationlist[index]) == 4):
        durationlist[index] = "00:0"+durationlist[index]
    elif (len(durationlist[index]) == 5):
         durationlist[index] = "00:"+durationlist[index]
    logging.info("\t %d. %s \t  %s ", index+1, nameslist[index], durationlist[index])
    exceldata+=topics.format(index+1, nameslist[index], durationlist[index])
#print (*nameslist, sep='\n')
#print (*durationlist, sep='\n')

#with open(logfilename, "r") as logFile:
 #   logdata = logFile.read()
#with open(logfilename+".json", 'w') as outfile:
 #   json.dump(logdata, outfile)
with open(logfilename+".csv", 'w') as outfile:
    outfile.write(exceldata)

sys.exit(0)
# collect the dates from the list of lines using regex matching groups
found_dates = []
for line in lines:
    m = re.search(r'(\d{2}/\d{2}/\d{2} \d+:\d+[a|p]m)', line)
    if m:
        found_dates.append(m.group(1))

# print the dates we collected
for date in found_dates:
    print(date)

for index in range(0,  counter):
    logging.debug("Searching from bulkdata location %d", placeholder)
    walker  = bulkdata.find(searchString, placeholder)
    logging.debug ("Token found at (walker): %d", walker)
    logging.debug ("Preparing to copy from (placeholder %d to walker %d) into formattedData length of %d", placeholder, walker,len(formattedData))
#    logging.debug ("Before: last 10 characters %s and first 10 of new string %s", formattedData[-10:],bulkdata[placeholder:10])
    formattedData+=bulkdata[placeholder:walker]
    formattedData+= '\n'
#    logging.debug("After: 20 characters of the concatenated string %s [%d:%d]", formattedData[walker-10:20], walker-10, viewerLength)
    walker+=1
    placeholder = walker
    logging.debug("Processed item(s):  %d", index)

formattedSize = len(formattedData)
with open("FormattedSyllabus.html", "w") as formattedFile:
   formattedFile.write(formattedData)
sourceFile.close()
formattedFile.close()
logging.debug ("File size prior to process %d after %d with an additional character count of %d", unformattedSize,formattedSize, formattedSize-unformattedSize)
ts = time.time()
lblTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
logging.info("##################### END EXECUTION at %s ####################", lblTimestamp)
logging.info("#########################################################")
