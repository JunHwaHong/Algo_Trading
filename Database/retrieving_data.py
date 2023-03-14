#!/usr/bin/python
# -*- coding: utf-8 -*-

# retrieving_data.py

from __future__ import print_function

import pandas as pd
import mysql.connector
from config import get_secret

if __name__ == "__main__":
    # Connect to the MySQL instance
    db_host = get_secret("DB_HOST")
    db_user = get_secret("DB_USER")
    db_pass = get_secret("DB_PASS")
    db_name = get_secret("DB_NAME")
    con = mysql.connector.connect(
            host=db_host, user=db_user, passwd=db_pass, database=db_name
        )

    # Select all of the historic Google adjusted close data
    sql = """SELECT dp.price_date, dp.adj_close_price
            FROM symbol AS sym
            INNER JOIN daily_price AS dp
            ON dp.symbol_id = sym.id
            WHERE sym.ticker = 'GOOG'
            ORDER BY dp.price_date ASC;"""

    # Create a pandas dataframe from the SQL query
    goog = pd.read_sql_query(sql, con=con, index_col='price_date')

    # Output the dataframe tail
    print(goog.tail())