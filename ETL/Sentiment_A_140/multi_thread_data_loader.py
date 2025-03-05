# import pandas as pd
# import polars as pl
# import requests
# import sqlite3
# from sqlalchemy import create_engine
# from concurrent.futures import ThreadPoolExecutor


# #CSV file theke data load
# def load_csv(file_path,use_polars = False):
#     if use_polars:
#         return pl.read_csv(file_path,encoding="ISO-8859-1")
#     else:
#         return pd.read_csv(file_path,encoding="ISO-8859-1")

# #API theke data load
# def load_api(api_url,use_polars = False):
#     response = requests.get(api_url) #API call
#     data =  response.json() #JSON data receive

#     if use_polars:
#         return pl.DataFrame(data)
#     else:
#         return pd.DataFrame(data)
    

# def load_multiple_sources(file_paths, api_url, use_polars=False):
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         futures = []
        
#         # Load data from CSV files
#         for file_path in file_paths:
#             futures.append(executor.submit(load_csv, file_path, use_polars))
            
#         # Load data from API
#         futures.append(executor.submit(load_api, api_url, use_polars))
#         results = [future.result() for future in futures]
#     print(results)
#     return results



# # # ফাংশন যা একসাথে CSV, API, এবং SQL ডেটা লোড করবে
# # def load_multiple_sources(file_paths, api_url, 
# # connection_string, query, use_polars=False):
# #     results = []
    
# #     # CSV ফাইলগুলো লোড কর
# #     for file_path in file_paths:
# #         results.append(load_csv(file_path, use_polars))
    
# #     # API থেকে ডেটা লোড কর
# #     results.append(load_api(api_url, use_polars))
    
# #     # SQL থেকে ডেটা লোড কর
# #     # results.append(load_sql(connection_string, query, use_polars))
    




    

# # ডেটাসেট ব্যবহার:

# file_paths = ['training.1600000.processed.noemoticon.csv', 'Senti140.csv']  # CSV ফাইল পাথ
# api_url = 'https://jsonplaceholder.typicode.com/posts'  # API URL


# # import mysql.connector
# # # Replace these with your database details
# # username = 'root'       # Your MySQL username
# # # (default for XAMPP is 'root')
# # password = ''          # Your MySQL password
# # # (default for XAMPP is "" (empty))
# # database_name = 'sample_nlp_5'  # Your database name
# # host = '127.0.0.1'      # Default host for local
# # # MySQL server
# # port = 3306             # Default MySQL port (as
# # # integer)

# # # Establish the connection using mysql-connector
# # conn = mysql.connector.connect(
# #     host=host,
# #     user=username,
# #     password=password,
# #     database=database_name,
# #     port=port
# # )

# # # রেজাল্ট দেখানো
# # for df in results:
# #     print(df.head())

# # connection_string = 'sqlite:///your_database.db'  # SQLite DB কানেকশন
# # query = 'SELECT * FROM your_table'  # SQL কুয়েরি

# results = load_multiple_sources(file_paths, api_url, use_polars=False)
















import pandas as pd
import polars as pl
import requests
from concurrent.futures import ThreadPoolExecutor

# CSV file loading function
def load_csv(file_path, use_polars=False):
    if use_polars:
        return pl.read_csv(file_path, encoding="ISO-8859-1")
    else:
        return pd.read_csv(file_path, encoding="ISO-8859-1")

# API data loading function
def load_api(api_url, use_polars=False):
    response = requests.get(api_url)  # API call
    data = response.json()  # Convert JSON response to dictionary

    if use_polars:
        return pl.DataFrame(data)
    else:
        return pd.DataFrame(data)

# Load data from multiple sources (CSV & API)
def load_multiple_sources(file_paths, api_url, use_polars=False):
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []

        # Load data from CSV files
        for file_path in file_paths:
            futures.append(executor.submit(load_csv, file_path, use_polars))

        # Load data from API
        futures.append(executor.submit(load_api, api_url, use_polars))

        results = [future.result() for future in futures]
    print(results)
    return results  # Return all results

# Define dataset file paths and API URL
file_paths = [r"G:\NLP BATCH 5\Sentiment_A_140\Senti140(2).csv",
              r"G:\NLP BATCH 5\Sentiment_A_140\Senti140.csv"]

api_url = 'https://jsonplaceholder.typicode.com/posts'  # Sample API URL

# Load data
results = load_multiple_sources(file_paths, api_url, use_polars=False)



