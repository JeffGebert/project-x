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
print dfsummary

"""Generation detail"""

x=StringIO(depth2[3])
dfgeneration = pd.read_html(x, header=1)
print dfgeneration

"""Interchange"""
x=StringIO(depth2[4])
dfinterchange = pd.read_html(x, header=1)
print dfinterchange



for t in tables:
  if len(t.find_parents("table")) == 3:
    depth3.append(t)

print len(depth3)
"""get coal data"""

x=StringIO(depth3[0])
dfs = pd.read_html(x, header=1)
df0=dfs[0]
df0['Generation_Type'] = 'COAL'

print df0


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


while i < len(df1):

	if df1[0][i] =='Simple Cycle':
		i=i+1
		type=1
		continue

	elif df1[0][i] =='Cogeneration':
		i=i+1
		type=2
		continue


	elif df1[0][i] =='Combined Cycle':
		i=i+1
		type=3
		continue


	if type ==1:
		simple_cycle_list.append(df1.loc[i])
	elif type ==2:
		cogeneration_list.append(df1.loc[i])
		test=2
	elif type ==3:
		combined_cycle_list.append(df1.loc[i])

	i=i+1

keys = ['ASSET','MC','TNG', 'DCR', 'Generation_Type']
combined_cycle_dictionary = {}
for i in keys:
    combined_cycle_dictionary[i] = None

combined_cycle_list.pop(0)
asset=[]
mc=[]
tng=[]
dcr=[]
Generation_Type=[]
new_data=[]
i=0
while i <len(combined_cycle_list):
	temp=combined_cycle_list[i].to_dict()
	asset.append(temp.pop(0))
	mc.append(temp.pop(1))
	tng.append(temp.pop(2))
	dcr.append(temp.pop(3))
	Generation_Type.append('Combined Cycle')
	i += 1

new_data.append(asset)
new_data.append(mc)
new_data.append(tng)
new_data.append(dcr)
new_data.append(Generation_Type)



dfnew_data = pd.DataFrame(new_data)
dfnew_data = dfnew_data.transpose()
dfnew_data.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

"""Get Hydro Data"""
x=StringIO(depth3[2])
dfs = pd.read_html(x, header=1)
df2=dfs[0]
df2['Generation_Type'] = 'HYDRO'

"""Get Wind Data"""

x=StringIO(depth3[3])
dfs = pd.read_html(x, header=1)
df3=dfs[0]
df3['Generation_Type'] = 'WIND'


"""Get BIOMASS AND OTHER DATA"""
x=StringIO(depth3[4])
dfs = pd.read_html(x, header=1)
df4=dfs[0]
df4['Generation_Type'] = 'BIOMASS AND OTHER'


jsondf = df0.to_json( orient='index')
print jsondf
