from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import urllib3
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

http = urllib3.PoolManager()

app = Flask(__name__)




current_supply_and_demand_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
response = http.request('GET',current_supply_and_demand_url)
soup=BeautifulSoup(response.data, "html.parser")


tables = soup.findAll("table")
depth3 = []
for t in tables:
  if len(t.find_parents("table")) == 3:
    depth3.append(t)


x=StringIO(depth3[0])
dfs = pd.read_html(x, header=1)
df=dfs[0]
df['Generation_Type'] = 'COAL'
print df


out = df.to_json(orient='records')
print out

"""find coal plant data"""

"""tables = soup.find_all('table')[14]"""

"""df = pd.read_html(str(table))"""


"""print(df[0].to_json(orient='records'))"""


#make a POST request


"""res = requests.post('http://localhost:5000/api/controllers/post_df', out)
print 'response from server:',res.text
out = res.json()"""


@app.route('/hello')
def hello():
	return "stefano is gay"


@app.route('/hello2')
def hello2():
	return "stefano is really gay"
@app.route("/test", methods=['GET','POST'])
def test():
    return jsonify(out)


if __name__ == "__main__":
  app.run()
