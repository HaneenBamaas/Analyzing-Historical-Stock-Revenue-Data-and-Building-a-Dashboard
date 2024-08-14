#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[2]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[3]:


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


# In[4]:


tesla_data=yf.Ticker("TSLA")


# In[5]:


tesla=tesla_data.history(period="max")
tesla.reset_index(inplace=True)


# In[6]:


tesla.head()


# In[7]:


URL="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"


# In[8]:


html_data=requests.get(URL).text


# In[9]:


soup=BeautifulSoup(html_data,"html.parser")


# In[10]:


tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])


# In[11]:


for row in soup.find_all("tbody"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text
        tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[12]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[21]:


tesla_revenue.tail()


# In[22]:


GameStop=yf.Ticker("GME")


# In[23]:


gme_data=GameStop.history(period="max")
gme_data.reset_index(inplace=True)


# In[24]:


gme_data.head()


# In[25]:


URL2=" https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"


# In[26]:


html_data_2=requests.get(URL2).text


# In[27]:


soup2=BeautifulSoup(html_data_2,"html.parser")


# In[28]:


gme_revenue=pd.DataFrame(columns=["Date","Revenue"])


# In[30]:


for row in soup2.find_all("tbody"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text
        gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[31]:


gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]


# In[32]:


gme_revenue.tail()


# In[36]:


make_graph(tesla, tesla_revenue, 'Tesla')


# In[37]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




