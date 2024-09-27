import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

tsla = yf.Ticker("TSLA")

tsla_data = tsla.history(period="max")

tsla_data.reset_index(inplace=True)
tsla_data.head(n=5)
tsla_data.columns

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url=url)
html_data

soup = BeautifulSoup(html_data.content, "html.parser")
soup

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

table_obj = soup.find_all("table")[1]

for table_row in table_obj.find("tbody").find_all("tr"):
    table_row = table_row.find_all("td")
    date = table_row[0].text
    revenue = table_row[1].text

    tesla_revenue = pd.concat([tesla_revenue,
                               pd.DataFrame({"Date": [date], "Revenue": [revenue]})],
                              ignore_index=True)

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail(n=5)

gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.tail(n=5)

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url=url)
soup = BeautifulSoup(html_data.content, "html.parser")

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

table_obj = soup.find_all("table")[1]

for table_row in table_obj.find("tbody").find_all("tr"):
    table_row = table_row.find_all("td")
    date = table_row[0].text
    revenue = table_row[1].text

    gme_revenue = pd.concat([gme_revenue,
                             pd.DataFrame({"Date": [date], "Revenue": [revenue]})],
                            ignore_index=True)
gme_revenue.head()
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
gme_revenue.tail(n=5)

make_graph(tsla_data, tesla_revenue, "Tesla")
make_graph(gme_data, gme_revenue, "GameStop")


