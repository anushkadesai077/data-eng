import os
import sqlite3
import pandas as pd
from pathlib import Path

database_file_name = 'sql_scraped_database.db'    #the database (.db) file which has all the metadata that is needed populated in it
database_file_path = os.path.join(os.path.dirname(__file__),database_file_name)      #set path to the database file

def get_product_goes():
     
     """Function to query distinct product names present in the SQLite database's GOES_METADATA (GOES-18 satellite data) 
     table. The function handles case when table does not exists.
     -----
     Input parameters:
     None
     -----
     Returns:
     A list containing all distinct product names or False (bool) in case of error
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT product FROM GOES_METADATA"   #sql query to execute
     try: #added try-except block to handle case when GOES18 database/table is not populated
          df_product = pd.read_sql_query(query, db_conn)
     except:
          return False

     products = df_product['product'].tolist()    #convert the returned df to a list
     return products
     
def get_years_in_product_goes(selected_product):

     """Function to query distinct year values present in the SQLite database's GOES_METADATA (GOES-18 satellite data) table 
     for a given product.
     -----
     Input parameters:
     selected_product : str
          string containing product name
     -----
     Returns:
     A list containing all distinct years for given product name 
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT year FROM GOES_METADATA WHERE product = " + "\'" + selected_product + "\'" #sql query to execute
     df_year = pd.read_sql_query(query, db_conn)
     years = df_year['year'].tolist()   #convert the returned df to a list
     return years

def get_days_in_year_goes(selected_year, selected_product):

     """Function to query distinct day values present in the SQLite database's GOES_METADATA (GOES-18 satellite data) table 
     for a given year.
     -----
     Input parameters:
     selected_year : str
          string containing year
     selected_product : str
          string containing product name
     -----
     Returns:
     A list containing all distinct days for given year 
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT day FROM GOES_METADATA WHERE year = " + "\'" + selected_year + "\'" + "AND product = " + "\'" + selected_product + "\'" #sql query to execute
     df_day = pd.read_sql_query(query, db_conn)
     days = df_day['day'].tolist() #convert the returned df to a list
     return days

def get_hours_in_day_goes(selected_day, selected_year, selected_product):

     """Function to query distinct hour values present in the SQLite database's GOES_METADATA (GOES-18 satellite data) table 
     for a given day value.
     -----
     Input parameters:
     selected_day : str
          string containing day value
     selected_year : str
          string containing year
     selected_product : str
          string containing product name
     -----
     Returns:
     A list containing all distinct hours for given day 
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT hour FROM GOES_METADATA WHERE day = " + "\'" + selected_day + "\'" + "AND year = " + "\'" + selected_year + "\'" + "AND product = " + "\'" + selected_product + "\'" #sql query to execute
     df_hour = pd.read_sql_query(query, db_conn)
     hours = df_hour['hour'].tolist()   #convert the returned df to a list
     return hours

def get_years_nexrad():

     """Function to query distinct years present in the SQLite database's NEXRAD_METADATA (NEXRAD satellite data) 
     table. The function handles case when table does not exists.
     -----
     Input parameters:
     None
     -----
     Returns:
     A list containing all distinct years or False (bool) in case of error
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT year FROM NEXRAD_METADATA"
     try: #added try-except block to handle case when NEXRAD database/table is not populated
          df_year = pd.read_sql_query(query, db_conn)
     except:
          return False
     years = df_year['year'].tolist()   #convert the returned df to a list
     return years

def get_months_in_year_nexrad(selected_year):

     """Function to query distinct month values present in the SQLite database's NEXRAD_METADATA (NEXRAD satellite data) table 
     for a given year.
     -----
     Input parameters:
     selected_year : str
          string containing year
     -----
     Returns:
     A list containing all distinct month values 
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT month FROM NEXRAD_METADATA WHERE year = " + "\'" + selected_year + "\'"    #sql query to execute
     df_month = pd.read_sql_query(query, db_conn)
     months = df_month['month'].tolist()     #convert the returned df to a list
     return months

def get_days_in_month_nexrad(selected_month, selected_year):
     
     """Function to query distinct day values present in the SQLite database's NEXRAD_METADATA (NEXRAD satellite data) table 
     for a given month.
     -----
     Input parameters:
     selected_month : str
          string containing month value
     selected_year : str
          string containing year
     -----
     Returns:
     A list containing all distinct day values 
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT day FROM NEXRAD_METADATA WHERE month = " + "\'" + selected_month + "\'" + "AND year = " + "\'" + selected_year + "\'"   #sql query to execute
     df_day = pd.read_sql_query(query, db_conn)
     days = df_day['day'].tolist() #convert the returned df to a list
     return days

def get_stations_for_day_nexrad(selected_day, selected_month, selected_year):

     """Function to query distinct day values present in the SQLite database's NEXRAD_METADATA (NEXRAD satellite data) table 
     for a given month.
     -----
     Input parameters:
     selected_day : str
          string containing day value
     selected_month : str
          string containing month value
     selected_year : str
          string containing year
     -----
     Returns:
     A list containing all distinct day values 
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT DISTINCT ground_station FROM NEXRAD_METADATA WHERE day = " + "\'" + selected_day + "\'" + "AND month = " + "\'" + selected_month + "\'" + " AND year =" + "\'" + selected_year + "\'"   #sql query to execute
     df_station = pd.read_sql_query(query, db_conn)
     stations = df_station['ground_station'].tolist()  #convert the returned df to a list
     return stations

def get_nextrad_mapdata():

     """Function to query all data from the SQLite database's MAPDATA_NEXRAD (NEXRAD satellite locations) 
     table. The function handles case when table does not exists.
     -----
     Input parameters:
     None
     -----
     Returns:
     A dataframe containing entire table or False (bool) in case of error
     """

     db_conn = sqlite3.connect(database_file_path)     #connection to the db
     query = "SELECT * FROM MAPDATA_NEXRAD"
     try: #added try-except block to handle case when NEXRAD database/table is not populated
          df_mapdata = pd.read_sql_query(query, db_conn)
     except:
          return pd.DataFrame()
     return df_mapdata