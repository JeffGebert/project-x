from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import urllib3
import csv
import itertools
import sys



"""Long term wind forecast"""

date=[]
most_likely=[]

url = 'http://ets.aeso.ca/Market/Reports/Manual/Operations/prodweb_reports/wind_power_forecast/WPF_LongTerm.csv'
http = urllib3.PoolManager()
r = http.request("GET",url)
r.status
response = r.data
cr = csv.reader(response.decode('utf-8').splitlines())
for row in itertools.islice(cr,3,30):
    date.append(row[0])
    most_likely.append(row[2])


"""short term wind forecast"""

short_term_date=[]
short_term_most_likely=[]

url = 'http://ets.aeso.ca/Market/Reports/Manual/Operations/prodweb_reports/wind_power_forecast/WPF_ShortTerm.csv'
http = urllib3.PoolManager()
r = http.request("GET",url)
r.status
response = r.data
cr = csv.reader(response.decode('utf-8').splitlines())
for row in itertools.islice(cr,3,16):
    short_term_date.append(row[0])
    short_term_most_likely.append(row[2])


for item in short_term_date:
	print item

print "hello"
short_term_wind=[]
long_term_wind=[]
x = len(short_term_date)
i=0
for i in range(0,x):
	short_term_wind.append(dict(zip(('date','value'),(short_term_date[i],float(short_term_most_likely[i])))))
	long_term_wind.append(dict(zip(('date','value'),(date[i],float(most_likely[i])))))
	i=i+1


output=json.dumps(short_term_wind)
output2=json.dumps(long_term_wind)

print output
print output2
