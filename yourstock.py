import requests
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas_ta as ta

st.set_page_config(page_title='YourStock',layout='wide')
headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'application/json, text/plain, /',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'origin': 'https://www.nasdaq.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.nasdaq.com/',
    'accept-language': 'en-US,en;q=0.9',
}

params = (
    ('tableonly', 'true'),
    ('limit', '25'),
    ('offset', '0'),
    ('download', 'true'),
)

r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params)
data = r.json()['data']
df = pd.DataFrame(data['rows'], columns=data['headers'])

df1=df[['symbol','name']]
ticker=[]
for i in range(df1.shape[0]):
        ticker.append(df1['name'][i])
companies=st.multiselect('Select your companies',ticker)
value=st.multiselect('Select different values',['Open','Close','High','Low','Volume'])
for i in range(len(companies)):
        result=df1.loc[df1['name']==companies[i]]
        result=list(result['symbol'])
        stock=yf.download(result[0],period='1y')
        st.subheader(f':blue[The details of the company {companies[i]}] ')
        c1,c2=st.columns(2)
        with c1:
            fig=px.line(stock[value])
            st.plotly_chart(fig)
        with c2:
            st.table(stock.iloc[::-1].head(10))
        


