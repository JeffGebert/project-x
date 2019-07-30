from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import html
import json
import urllib3
import csv
import itertools
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

http = urllib3.PoolManager()

app = Flask(__name__)


"""get forecast vs actual and load data"""

forecast_vs_actual_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/ActualForecastReportServlet?contentType=html"
response = http.request('GET',forecast_vs_actual_url)
soup=BeautifulSoup(response.data, "html.parser")

table_array=[]
tables = soup.findAll("table")

for t in tables:
	table_array.append(t)


x=StringIO(table_array[2])
dfs = pd.read_html(x)
forecast_vs_actual=dfs[0]


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


short_term_wind=dict(zip(short_term_date, short_term_most_likely))
long_term_wind=dict(zip(date,most_likely))

output2=json.dumps(short_term_wind)
output3=json.dumps(long_term_wind)


"""transfer capacities and market offers"""

page = requests.get('http://itc.aeso.ca/itc/public/realTimeAllocationReport.do;jsessionid=MoIds25m3WR0cjTujvfPvKG-0xnzui8FxmCczt2LtHB2zuK6jByi!514906425')
tree = html.fromstring(page.content)

date1 = tree.xpath("/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr/td/form/table[2]")
print date1


http = urllib3.PoolManager()

"""transfer capacities and market offers"""

real_time_atc="http://itc.aeso.ca/itc/public/realTimeAllocationReport.do;jsessionid=SPUi4-u_Xy171xTGqLi-iNOPzGEw80gynDeDYgWfYA_LbNcekFx4!249941794"
response = http.request('GET',real_time_atc)
soup=BeautifulSoup(response.data.decode('utf-8', 'ignore'), "html.parser")
data=[]

to_remove = soup.find_all("tr",{"class":"evenrow"})
for element in to_remove:
    children = element.findChildren("td")
    for child in children:
		x=child.findChildren()
		y=len(x)
		if y>0:
			try:
				data.append(child.find('b').get_text().strip())
			except:
				continue

		else:
			try:
				data.append(child.get_text().strip())
			except:
				continue



even_dict=[]

a=0

x=len(data)


while a < x:
    temp={}
    temp = {
      "date":data[a],
      "he":data[a+1],
      "Offers_BC_IMPORT":int(data[a+3]),
      "Offers_BC_EXPORT":int(data[a+4]),
      "Offers_MATL_IMPORT":int(data[a+5]),
      "Offers_MATL_EXPORT":int(data[a+6]),
      "Offers_SK_IMPORT":int(data[a+7]),
      "Offers_SK_EXPORT":int(data[a+8]),
      "Offers_BC_MATL_Import":int(data[a+9]),
      "Offers_BC_MATL_Export":int(data[a+10]),
      "Offers_System_Import":int(data[a+11]),
      "Offers_System_Export":int(data[a+12]),
      "ATC_BC_IMPORT":int(data[a+55]),
      "ATC_BC_EXPORT":int(data[a+56]),
      "ATC_MATL_IMPORT":int(data[a+57]),
      "ATC_MATL_EXPORT":int(data[a+58]),
      "ATC_SK_IMPORT":int(data[a+59]),
      "ATC_SK_EXPORT":int(data[a+60]),
      "ATC_BC_MATL_IMPORT":int(data[a+61]),
      "ATC_BC_MATL_EXPORT":int(data[a+62]),
      "ATC_SYSTEM_IMPORT":int(data[a+63]),
      "ATC_SYSTEM_EXPORT":int(data[a+64])
    }


    even_dict.append(temp)
    a=a+65

"""Get Odd rows"""

data=[]

to_remove = soup.find_all("tr",{"class":"oddrow"})
for element in to_remove:
    children = element.findChildren("td")
    for child in children:
		x=child.findChildren()
		y=len(x)
		if y>0:
			try:
				data.append(child.find('b').get_text().strip())
			except:
				continue

		else:
			try:
				data.append(child.get_text().strip())
			except:
				continue
a=0

x=len(data)


while a < x:
    temp={}
    temp = {
      "date":data[a],
      "he":data[a+1],
      "Offers_BC_IMPORT":int(data[a+3]),
      "Offers_BC_EXPORT":int(data[a+4]),
      "Offers_MATL_IMPORT":int(data[a+5]),
      "Offers_MATL_EXPORT":int(data[a+6]),
      "Offers_SK_IMPORT":int(data[a+7]),
      "Offers_SK_EXPORT":int(data[a+8]),
      "Offers_BC_MATL_Import":int(data[a+9]),
      "Offers_BC_MATL_Export":int(data[a+10]),
      "Offers_System_Import":int(data[a+11]),
      "Offers_System_Export":int(data[a+12]),
      "ATC_BC_IMPORT":int(data[a+55]),
      "ATC_BC_EXPORT":int(data[a+56]),
      "ATC_MATL_IMPORT":int(data[a+57]),
      "ATC_MATL_EXPORT":int(data[a+58]),
      "ATC_SK_IMPORT":int(data[a+59]),
      "ATC_SK_EXPORT":int(data[a+60]),
      "ATC_BC_MATL_IMPORT":int(data[a+61]),
      "ATC_BC_MATL_EXPORT":int(data[a+62]),
      "ATC_SYSTEM_IMPORT":int(data[a+63]),
      "ATC_SYSTEM_EXPORT":int(data[a+64])
    }

    even_dict.append(temp)
    a=a+65


output=json.dumps(even_dict)


@app.route("/forecastvsactual", methods=['GET','POST'])
def test():
    return output

@app.route("/shorttermwind", methods=['GET','POST'])
def test2():
    return output2

@app.route("/longtermwind", methods=['GET','POST'])
def test3():
    return output3



if __name__ == "__main__":
  app.run()
