from bs4 import BeautifulSoup
import requests

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sqlite3

import csv
import os

import csv_sqlite

class StockRequest(BaseModel):
    stock_code: str

class StockPrice(BaseModel):
    stockid: str

def serch_stock(str):
    stocklist = csv_sqlite.Stock.find_any(str)
    return stocklist

def get_stock_price(stockid):
    url = 'https://finance.yahoo.co.jp/quote/' + stockid + '.T'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    price = soup.find(class_='StyledNumber__value__3rXW DataListItem__value__11kV').text
    # price = soup.find_all(class_='StyledNumber__value__3rXW DataListItem__value__11kV')
    return price

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stock")
def read_stock(request: StockRequest):
    stocks = serch_stock(request.stock_code)
    return stocks

@app.post('/price')
def read_price(request: StockPrice):
    price = get_stock_price(request.stockid)
    print(price)
    return price
