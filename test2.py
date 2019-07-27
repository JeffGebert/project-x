from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import urllib3
import csv
import itertools
import sys


http = urllib3.PoolManager()

"""transfer capacities and market offers"""
print "test"
real_time_atc="http://itc.aeso.ca/itc/public/realTimeAllocationReport.do;jsessionid=SPUi4-u_Xy171xTGqLi-iNOPzGEw80gynDeDYgWfYA_LbNcekFx4!249941794"
response = http.request('GET',real_time_atc)
soup=BeautifulSoup(response.data.decode('utf-8', 'ignore'), "html.parser")
data=[]

print "test1"
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
      "Offers_BC_IMPORT":data[a+3],
      "Offers_BC_EXPORT":data[a+4],
      "Offers_MATL_IMPORT":data[a+5],
      "Offers_MATL_EXPORT":data[a+6],
      "Offers_SK_IMPORT":data[a+7],
      "Offers_SK_EXPORT":data[a+8],
      "Offers_BC_MATL_Import":data[a+9],
      "Offers_BC_MATL_Export":data[a+10],
      "Offers_System_Import":data[a+11],
      "Offers_System_Export":data[a+12],
      "ATC_BC_IMPORT":data[a+55],
      "ATC_BC_EXPORT":data[a+56],
      "ATC_MATL_IMPORT":data[a+57],
      "ATC_MATL_EXPORT":data[a+58],
      "ATC_SK_IMPORT":data[a+59],
      "ATC_SK_EXPORT":data[a+60],
      "ATC_BC_MATL_IMPORT":data[a+61],
      "ATC_BC_MATL_EXPORT":data[a+62],
      "ATC_SYSTEM_IMPORT":data[a+63],
      "ATC_SYSTEM_EXPORT":data[a+64]
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
      "Offers_BC_EXPORT":data[a+4],
      "Offers_MATL_IMPORT":data[a+5],
      "Offers_MATL_EXPORT":data[a+6],
      "Offers_SK_IMPORT":data[a+7],
      "Offers_SK_EXPORT":data[a+8],
      "Offers_BC_MATL_Import":data[a+9],
      "Offers_BC_MATL_Export":data[a+10],
      "Offers_System_Import":data[a+11],
      "Offers_System_Export":data[a+12],
      "ATC_BC_IMPORT":data[a+55],
      "ATC_BC_EXPORT":data[a+56],
      "ATC_MATL_IMPORT":data[a+57],
      "ATC_MATL_EXPORT":data[a+58],
      "ATC_SK_IMPORT":data[a+59],
      "ATC_SK_EXPORT":data[a+60],
      "ATC_BC_MATL_IMPORT":data[a+61],
      "ATC_BC_MATL_EXPORT":data[a+62],
      "ATC_SYSTEM_IMPORT":data[a+63],
      "ATC_SYSTEM_EXPORT":data[a+64]
    }

    even_dict.append(temp)
    a=a+65


print even_dict
