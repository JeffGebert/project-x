from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import json
import urllib3
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

http = urllib3.PoolManager()

"""get forecast vs actual and load data"""

forecast_vs_actual_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/ActualForecastReportServlet?contentType=html"
response = http.request('GET',forecast_vs_actual_url)
soup=BeautifulSoup(response.data, "html.parser")

table_array=[]
tables = soup.findAll("table")

for t in tables:
	table_array.append(t)

new_table=table_array[2]
data2=[]
for td in new_table.findChildren('td'):
	data2.append(td.text.strip())


x=len(data2)

b=0

data3=[]

while b<x:
	temp={}
	temp = {

	"date(he)":data2[b],
	"real_time_forecast":data2[b+2],
	"actual_price":data2[b+3],
	"day_ahead_load_forecast":data2[b+4],
	"actual_ail":data2[b+5],
	"Forecast_actual_ail_diff":data2[b+6]

	}
	data3.append(temp)
	b=b+9

print data3
