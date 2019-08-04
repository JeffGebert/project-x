from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
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


current_supply_and_demand_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
response = http.request('GET',current_supply_and_demand_url)
soup=BeautifulSoup(response.data, "html.parser")

tables = soup.findAll("table")
depth2 = []
depth3 = []

for t in tables:
	 if len(t.find_parents("table")) == 2:
	   depth2.append(t)



"""summary detail"""
x=StringIO(depth2[2])
dfsummary = pd.read_html(x, header=0)
dfsummary1=dfsummary[0]
dfsummary1.columns = ['Summary', 'Values']



json_summary=dfsummary1.to_json(orient='index')

print json_summary
