from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import json
import urllib3
import itertools
from lxml import html
import csv
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

http = urllib3.PoolManager()

app = Flask(__name__)




http = urllib3.PoolManager()




@app.route("/test", methods=['GET','POST'])
def test():

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
	simple_cycle_dictionary={}
	cogeneration_dictionary={}




	for i in keys:
	    combined_cycle_dictionary[i] = None

	combined_cycle_list.pop(0)
	asset=[]
	mc=[]
	tng=[]
	dcr=[]
	Generation_Type=[]
	combined_cycle_data=[]
	i=0
	while i <len(combined_cycle_list):
		temp=combined_cycle_list[i].to_dict()
		asset.append(temp.pop(0))
		mc.append(int(temp.pop(1)))
		tng.append(int(temp.pop(2)))
		dcr.append(int(temp.pop(3)))
		Generation_Type.append('Combined Cycle')
		i += 1

	combined_cycle_data.append(asset)
	combined_cycle_data.append(mc)
	combined_cycle_data.append(tng)
	combined_cycle_data.append(dcr)
	combined_cycle_data.append(Generation_Type)



	dfcombined_cycle = pd.DataFrame(combined_cycle_data)
	dfcombined_cycle = dfcombined_cycle.transpose()
	dfcombined_cycle.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

	dfcombined_cycle['MC'] = dfcombined_cycle['MC'].astype('int64')
	dfcombined_cycle['TNG'] = dfcombined_cycle['TNG'].astype('int64')
	dfcombined_cycle['DCR'] = dfcombined_cycle['DCR'].astype('int64')



	for i in keys:
	    simple_cycle_dictionary[i] = None

	simple_cycle_list.pop(0)
	asset=[]
	mc=[]
	tng=[]
	dcr=[]
	Generation_Type=[]
	cogeneration_data=[]
	i=0
	while i <len(simple_cycle_list):
		temp=simple_cycle_list[i].to_dict()
		asset.append(temp.pop(0))
		mc.append(int(temp.pop(1)))
		tng.append(int(temp.pop(2)))
		dcr.append(int(temp.pop(3)))
		Generation_Type.append('Simple Cycle')
		i += 1

	cogeneration_data.append(asset)
	cogeneration_data.append(mc)
	cogeneration_data.append(tng)
	cogeneration_data.append(dcr)
	cogeneration_data.append(Generation_Type)



	dfcogeneration = pd.DataFrame(cogeneration_data)
	dfcogeneration = dfcogeneration.transpose()
	dfcogeneration.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

	dfcogeneration['MC'] = dfcogeneration['MC'].astype('int64')
	dfcogeneration['TNG'] = dfcogeneration['TNG'].astype('int64')
	dfcogeneration['DCR'] = dfcogeneration['DCR'].astype('int64')





	for i in keys:
	    cogeneration_dictionary[i] = None

	simple_cycle_list.pop(0)
	asset=[]
	mc=[]
	tng=[]
	dcr=[]
	Generation_Type=[]
	cogeneration_data=[]
	i=0
	while i <len(simple_cycle_list):
		temp=simple_cycle_list[i].to_dict()
		asset.append(temp.pop(0))
		mc.append(int(temp.pop(1)))
		tng.append(int(temp.pop(2)))
		dcr.append(int(temp.pop(3)))
		Generation_Type.append('Simple Cycle')
		i += 1

	cogeneration_data.append(asset)
	cogeneration_data.append(mc)
	cogeneration_data.append(tng)
	cogeneration_data.append(dcr)
	cogeneration_data.append(Generation_Type)



	dfsimple_cycle = pd.DataFrame(cogeneration_data)
	dfsimple_cycle = dfsimple_cycle.transpose()
	dfsimple_cycle.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

	dfsimple_cycle['MC'] = dfsimple_cycle['MC'].astype('int64')
	dfsimple_cycle['TNG'] = dfsimple_cycle['TNG'].astype('int64')
	dfsimple_cycle['DCR'] = dfsimple_cycle['DCR'].astype('int64')


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


	for i in keys:
	    simple_cycle_dictionary[i] = None

	simple_cycle_list.pop(0)
	asset=[]
	mc=[]
	tng=[]
	dcr=[]
	Generation_Type=[]
	simple_cycle_data=[]
	i=0
	while i <len(simple_cycle_list):
		temp=simple_cycle_list[i].to_dict()
		asset.append(temp.pop(0))
		mc.append(int(temp.pop(1)))
		tng.append(int(temp.pop(2)))
		dcr.append(int(temp.pop(3)))
		Generation_Type.append('Simple Cycle')
		i += 1

	simple_cycle_data.append(asset)
	simple_cycle_data.append(mc)
	simple_cycle_data.append(tng)
	simple_cycle_data.append(dcr)
	simple_cycle_data.append(Generation_Type)



	dfsimple_cycle = pd.DataFrame(simple_cycle_data)
	dfsimple_cycle = dfsimple_cycle.transpose()
	dfsimple_cycle.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

	dfsimple_cycle['MC'] = dfsimple_cycle['MC'].astype('int64')
	dfsimple_cycle['TNG'] = dfsimple_cycle['TNG'].astype('int64')
	dfsimple_cycle['DCR'] = dfsimple_cycle['DCR'].astype('int64')

	df_row = pd.concat([df0, dfcombined_cycle,dfsimple_cycle,dfcogeneration,df2,df3,df4])
	df_row=df_row.reset_index(drop=True)

	json_units = df_row.to_json(orient='index')


	return json_units


@app.route("/generation_summary", methods=['GET','POST'])
def test2():

	current_supply_and_demand_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
	response = http.request('GET',current_supply_and_demand_url)
	soup=BeautifulSoup(response.data, "html.parser")

	tables = soup.findAll("table")
	depth2 = []
	depth3 = []

	for t in tables:
	  if len(t.find_parents("table")) == 2:
	    depth2.append(t)


	"""Generation detail"""

	x=StringIO(depth2[3])
	dfgeneration = pd.read_html(x, header=1)
	dfgeneration1=dfgeneration[0]


	json_generation_summary=dfgeneration1.to_json(orient='index')

	return json_generation_summary

@app.route("/interchange", methods=['GET','POST'])
def test3():


	current_supply_and_demand_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
	response = http.request('GET',current_supply_and_demand_url)
	soup=BeautifulSoup(response.data, "html.parser")

	tables = soup.findAll("table")
	depth2 = []
	depth3 = []

	for t in tables:
	  if len(t.find_parents("table")) == 2:
	    depth2.append(t)





	"""Interchange"""
	x=StringIO(depth2[4])
	dfinterchange = pd.read_html(x, header=1)
	dfinterchange1=dfinterchange[0]
	dfinterchange1.columns=['PATH','ACTUAL_FLOW']

	json_interchange=dfinterchange1.to_json(orient='index')



	return json_interchange

@app.route("/Summary", methods=['GET','POST'])
def test4():



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

	return json_summary


@app.route("/forecastvsactual", methods=['GET','POST'])
def test5():

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

		"date":data2[b],
		"real_time_forecast":data2[b+2],
		"actual_price":data2[b+3],
		"day_ahead_load_forecast":data2[b+4],
		"actual_ail":data2[b+5],
		"Forecast_actual_ail_diff":data2[b+6]

		}
		data3.append(temp)
		b=b+9


	forecast_vs_actual_output = json.dumps(data3)

	return forecast_vs_actual_output

@app.route("/shorttermwind", methods=['GET','POST'])
def test6():


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
	    short_term_most_likely.append(float(row[2]))

	short_term_wind=[]
	x = len(short_term_date)
	i=0

	for i in range(0,x):
		short_term_wind.append(dict(zip(('date','value'),(short_term_date[i],float(short_term_most_likely[i])))))
		i=i+1


	print short_term_wind

	output2=json.dumps(short_term_wind)



	return output2

@app.route("/longtermwind", methods=['GET','POST'])
def test7():

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
	    most_likely.append(float(row[2]))

	long_term_wind=[]
	y = len(date)

	j=0
	for j in range(0,y):
		long_term_wind.append(dict(zip(('date','value'),(date[j],float(most_likely[j])))))
		j=j+1

	output3=json.dumps(long_term_wind)

	return output3

@app.route("/atc", methods=['GET','POST'])
def test8():

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
	      "he":int(data[a+1]),
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
	      "he":int(data[a+1]),
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



	return output




if __name__ == "__main__":
  app.run()
