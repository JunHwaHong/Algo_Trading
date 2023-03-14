#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py
 
from __future__ import print_function

import datetime
import warnings

import mysql.connector
import requests
import FinanceDataReader as fdr
from config import get_secret

# Obtain a database connection to the MySQL instance
db_host = get_secret("DB_HOST")
db_user = get_secret("DB_USER")
db_pass = get_secret("DB_PASS")
db_name = get_secret("DB_NAME")
con = mysql.connector.connect(
        host=db_host, user=db_user, passwd=db_pass, database=db_name
    )


def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database.
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]


def get_daily_historic_data_FBR(
    ticker, start_date=(2019,1,1),
    end_date=datetime.date.today().timetuple()[0:3]
    ):
    """
    Obtains data from FinanceDataReader returns and a list of tuples.

    ticker: Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format
    """
    # Construct the Yahoo URL with the correct integer query parameters
    # for start and end dates. Note that some parameters are zero-based!

    start = datetime.datetime(*start_date)
    end = datetime.datetime(*end_date)

    # Try connecting to FinanceDataReader and obtaining the data
    # On failure, print an error message.
    try:
        fbr_df = fdr.DataReader(ticker, start, end)
        prices = []
        for row in fbr_df.iterrows():
            prices.append(
                (row[0], row[1]['Open'], row[1]['High'], row[1]['Low'], row[1]['Close'], row[1]['Adj Close'], row[1]['Volume'])
            )
    except Exception as e:
        print("Could not download FinanceDataReader data: %s" % e)

    return prices


def insert_daily_data_into_db(
    data_vendor_id, symbol_id, daily_data
    ):
    """
    Takes a list of tuples of daily data and adds it to the
    MySQL database. Appends the vendor ID and symbol ID to the data.

    daily_data: List of tuples of the OHLC data (with adj_close and volume)
    """
    # Create the time now
    now = datetime.datetime.utcnow()

    # Amend the data to include the vendor ID and symbol ID
    daily_data = [
        (data_vendor_id, symbol_id, d[0], now, now,
        d[1], d[2], d[3], d[4], d[5], d[6])
        for d in daily_data
    ]

    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date,
                last_updated_date, open_price, high_price, low_price,
                close_price, adj_close_price, volume"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % \
        (column_str, insert_str)
    
    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    with con:
        cur = con.cursor()
        cur.executemany(final_str, daily_data)
        con.commit()


if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    # from the Yahoo precision to Decimal(19,4) datatypes
    warnings.filterwarnings('ignore')

    # Loop over the tickers and insert the daily historical
    # data into the database
    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print("Adding data for %s: %s out of %s" %
        (t[1], i+1, lentickers)
        )
        fbr_data = get_daily_historic_data_FBR(t[1])
        insert_daily_data_into_db('1', t[0], fbr_data)
    print("Successfully added FinanceDataReader price to DB.")
