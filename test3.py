from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
import urllib3
import sys
import itertools
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

http = urllib3.PoolManager()


http = urllib3.PoolManager()



current_supply_and_demand_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
response = http.request('GET',current_supply_and_demand_url)
soup=BeautifulSoup(response.data, "html.parser")

tables = soup.findAll("table")
depth2 = []
depth3 = []

for t in tables:
	if len(t.find_parents("table")) == 2:
		depth2.append(t)





for t in tables:
	if len(t.find_parents("table")) == 3:
		depth3.append(t)


"""get coal data"""

x=StringIO(depth3[0])
dfs = pd.read_html(x, header=1)
df0=dfs[0]
df0['Generation_Type'] = 'COAL'




x=StringIO(depth3[1])
dfs = pd.read_html(x)
df1=dfs[0]




"""Get Gas Data"""

simple_cycle_list=[]
combined_cycle_list=[]
cogeneration_list=[]

test=0
i=0
type=0
print "test1"
print df1[0]
print "test2"
print df1[0].loc[0]
