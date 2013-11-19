import requests
import datetime
import xml.etree.cElementTree as ET

def converttosat(mydate):
    '''
    INPUT: a datetime.date object

    Converts date to following Saturday.
    '''
    #############################################
    ###        CONVERT TO SATURDAY            ###
    #############################################
    
    dayofweek = mydate.weekday()
    if dayofweek==5:
        print "That's a Saturday."
        return mydate
    elif dayofweek<5:
        toadd = 5-dayofweek
    elif dayofweek==6:
        toadd = 6
    finaldate = mydate+datetime.timedelta(days=toadd)
    return finaldate

def getaliyahdata(mydate):
    '''
    INPUT: A datetime.date object

    Accesses Hebcal's REST API to get parasha name for that day
    (details on precise syntax for that here:
        http://www.hebcal.com/home/195/jewish-calendar-rest-api )

    Parses Hebcal's "aliyah.xml" file to get full kriyah aliyah data for
    that parasha (file found here: http://www.hebcal.com/dist/ )

    '''

    (year, month, day) = (mydate.year, mydate.month, mydate.day)

    #############################################
    ###    ACCESS HEBCAL FOR PARASHA NAME     ###
    #############################################

    caldata = {'v':'1',
               'cfg':'json',
               'nh':'on',
               'nx':'on',
               'year':str(year),
               'month':str(month),
               'ss':'on',
               'mf':'on',
               'c':'on',
               'zip':'94702',
               'm':'0',
               's':'on'
               }
    hebcalrawdata = requests.get('http://www.hebcal.com/hebcal/', params=caldata)

    jsondic = hebcalrawdata.json()
    for item in jsondic["items"]:
        if (item['date']==str(mydate)) and (item['category']=="parashat"):
            parashaname = item['title'][9:]

    #############################################
    ###        ALIYAH.XML PARSING PART        ###
    #############################################

    # Learned how to do this at:
    # http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree/

    aliyahtree = ET.ElementTree(file='aliyah.xml')
    searchstring = 'parsha[@id="%s"]/fullkriyah/aliyah' % (parashaname)

    #############################################################
    # CURRENTLY:  Prints raw data; returns a list of dictionaries
    # containing aliyah data in the structure from the XML file
    #############################################################
    
    finalanswer = []
    for elem in aliyahtree.iterfind(searchstring):
        print elem.attrib
        finalanswer.append(str(elem.attrib))
    return {'parashaname':parashaname,'aliyot':finalanswer}


##year = input("Input year: ")
##month = input("Input month number: ")
##day = input("Input date: ")
##
##testdate = datetime.date(year, month, day)
##
##getaliyahdata(testdate)
