# API documentation page: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews

import urllib.error, urllib.parse, urllib.request
import json
import sqlite3

# creating a database
connection = sqlite3.connect('requestshistorydata.sqlite')
cursr = connection.cursor()

cursr.executescript('''
DROP TABLE IF EXISTS Requests;
CREATE TABLE "Requests" (
	"id"	INTEGER NOT NULL UNIQUE,
	"request"	TEXT,
	"region"	TEXT,
	"year"	TEXT,
	"views"	TEXT,
    "url" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''')

# sample link: https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/2015100100/2015103100 
serviceurl = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'
secondarypart = 'all-access/all-agents/'

print("For more information about what's going on read README")

pk = 1
# creating a request
while True:
    # choosing a country
    while True:
        country = input("Print en if England\nPrint de if Germany\nWrite a country: ")
        if country == 'en':
            countrypart = 'en.wikipedia/'
            region = 'England'
            print('done')
            break
        elif country == 'de':
            countrypart = 'de.wikipedia/'
            region = 'Germany'
            print('done')
            break
        else:
            print("Wrong value, try one more time")

    # making a research part
    request = input("Write your request: ")
    words = request.split()
    x = 0
    requestpart = ''
    for word in words:
        word = word.strip()
        firstletter = word[:1].upper()
        word = firstletter + word[1:]
        words[x] = word
        requestpart = requestpart + words[x] + '_'
        x = x + 1
    requestpart = requestpart[:int(len(requestpart))-1] + '/daily/'
    print('done')

    # making a time pariod part (year)
    year = input('Write a year: ')
    timepart = year + '010100/' + year + '123100'
    print('done')

    url = serviceurl + countrypart + secondarypart + requestpart + timepart
    print('Your URL is:', url)
    print('')

    # retrieving json
    info = urllib.request.urlopen(url).read()
    js = json.loads(info)
    views = 0
    for item in js['items']:
        localviews = item['views']
        views = views + localviews
        
    cursr.execute('INSERT INTO Requests(request,region,year,url,views) VALUES (?,?,?,?,?)',(request,region,year,url,views))
    connection.commit()
    print('Okay, for', request,'topic there are', views,'views in the', year,'year in', region,'Wikipedia')
    print('')
    step = True
    while True:
        next_step = input('Some more requests?\nIf yes type yes\nIf no type no\nType here: ')
        if next_step=='yes':
            pk = pk + 1
            print('')
            print('Okay, here we go')
            print('')
            break
        elif next_step=='no':
            print('')
            print('Okay, see you soon')
            connection.commit()
            quit()
        else:
            print('Wrong value, try one more time\n')