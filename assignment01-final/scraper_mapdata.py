import requests
import boto3
import re
import os
import time
import plotly.graph_objects as go

def scrape_nexrad_locations():

    """Function scrapes a .txt file found on the internet containg NEXRAD satellite station locations. It scrapes for
    details like longitude, latitude, state, county, elevation and ground station ID for the satellites geoprapically 
    located in the USA. Initially, the function sets up a boto3 client for accessing AWS CloudWatch to perform logging 
    to a log group and log stream. This client has its own AWS access & secret key generated from AWS with 
    necessary permissions that should be stored in your .env file.
    -----
    Returns:
    A dictionary containing path for all subfolders 
    """

    #authenticate S3 client for logging with your user credentials that are stored in your .env config file
    clientLogs = boto3.client('logs',
                            region_name='us-east-1',
                            aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                            )

    #initialise containers for relevant data
    nexrad=[]
    satellite_metadata = {
        'id': [],
        'ground_station': [],
        'state': [],
        'county': [],
        'latitude': [],
        'longitude': [],
        'elevation': []
    }
    clientLogs.put_log_events(      #logging to AWS CloudWatch logs
        logGroupName = "assignment01-logs",
        logStreamName = "db-logs",
        logEvents = [
            {
            'timestamp' : int(time.time() * 1e3),
            'message' : "Scraping data for NEXRAD statellite locations"
            }
        ]
    )
    #url used to scrape NEXRAD satellite location data to plot on map
    url = "https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt"

    try:
        response = requests.get(url)    #recording the response from the webpage
        response.raise_for_status()
    except requests.exceptions.HTTPError as err_http:
        clientLogs.put_log_events(      #logging to AWS CloudWatch logs
            logGroupName = "assignment01-logs",
            logStreamName = "db-logs",
            logEvents = [
                {
                'timestamp' : int(time.time() * 1e3),
                'message' : "Exited due to HTTP error while accessing URL"
                }
            ]
        )  
        raise SystemExit(err_http)
    except requests.exceptions.ConnectionError as err_conn:
        clientLogs.put_log_events(      #logging to AWS CloudWatch logs
            logGroupName = "assignment01-logs",
            logStreamName = "db-logs",
            logEvents = [
                {
                'timestamp' : int(time.time() * 1e3),
                'message' : "Exited due to connection error while accessing URL"
                }
            ]
        )
        raise SystemExit(err_conn)
    except requests.exceptions.Timeout as err_to:
        clientLogs.put_log_events(      #logging to AWS CloudWatch logs
            logGroupName = "assignment01-logs",
            logStreamName = "db-logs",
            logEvents = [
                {
                'timestamp' : int(time.time() * 1e3),
                'message' : "Exited due to timeout error while accessing URL"
                }
            ]
        )
        raise SystemExit(err_to)
    except requests.exceptions.RequestException as err_req:
        clientLogs.put_log_events(      #logging to AWS CloudWatch logs
            logGroupName = "assignment01-logs",
            logStreamName = "db-logs",
            logEvents = [
                {
                'timestamp' : int(time.time() * 1e3),
                'message' : "Exited due to fatal error"
                }
            ]
        )
        raise SystemExit(err_req)

    #traverse extracted txt data line by line
    lines = response.text.split('\n')
    for line in lines:
        line=line.strip()   #strip leading and trailing whitespaces
        word_list = line.split(" ")
        if (word_list[-1].upper() == 'NEXRAD'):     #check if the data belongs to a NEXRAD satellite
            nexrad.append(line)
    nexrad = [i for i in nexrad if 'UNITED STATES' in i]    #only consider satellites over USA

    #extracting state and county information 
    id=0    #to store in database
    for satellite in nexrad:
        id+=1
        satellite = satellite.split("  ")
        satellite =  [i.strip() for i in satellite if i != ""]
        satellite_metadata['id'].append(id)
        satellite_metadata['ground_station'].append(satellite[0].split(" ")[1])
        for i in range(len(satellite)):
            if (re.match(r'\b[A-Z][A-Z]\b',satellite[i].strip())):      #use regex to match with the state field containing 2 capital letters
                satellite_metadata['state'].append(satellite[i][:2])    #append state field to final dict
                satellite_metadata['county'].append(satellite[i][2:])   #append county field to final dict

    #extracting latitude, longitude and elevation information 
    for satellite in nexrad:
        satellite = satellite.split(" ")
        satellite =  [i.strip() for i in satellite if i != ""]      #strip for any whitespaces if the string is not empty
        for i in range(len(satellite)):
            if (re.match(r'^-?[0-9]\d(\.\d+)?$',satellite[i])):     #use regex to match with the coordinate string
                state_county = satellite[i].split()
                satellite_metadata['latitude'].append(satellite[i])     #append latitude as string to final dict
                satellite_metadata['longitude'].append(satellite[i+1])  #append longtidue as string to final dict
                satellite_metadata['elevation'].append(int(satellite[i+2]))     #append elevation as int to final dict
                break
    
    clientLogs.put_log_events(      #logging to AWS CloudWatch logs
        logGroupName = "assignment01-logs",
        logStreamName = "db-logs",
        logEvents = [
            {
            'timestamp' : int(time.time() * 1e3),
            'message' : "Successfully scraped NEXRAD statellite location data"
            }
        ]
    )

    return satellite_metadata   #this dict has the final scraped data