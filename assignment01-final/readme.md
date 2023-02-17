# Building a Data Exploration Tool for Geospatial Startups: Utilizing NOAA's NexRad and GOES Satellite Data Sources
-----

> Status ✅: Active 

----- 

## Index
  - [Abstract 📝](#abstract)
  - [Data Sources 💽](#data-sources)
  - [Streamlit 🖥️](#streamlit)
  - [S3 🧊](#s3-)
  - [SQLite DB 🛢](#sqlite-db)
  - [Unit Testing ⚒️](#unit-testing)
  - [Great Expectations ☑️](#great-expectations)




## Abstract
The task involves building a data exploration tool for a geospatial startup. The tool utilizes publicly available data sources, specifically the NexRad and GOES satellite datasets, to make it easier for data analysts to download data. The data sources can be found on the National Oceanic and Atmospheric Administration (NOAA) website and the tool has several capabilities to support data exploration and download. The following capabilties can be performed from this project:

- scrape the open registry for NOAA GOES and NEXRAD satellites on AWS S3 
- generate a download link from the registry based on input parameters or filename on UI
- get 


The test site for the project hosted on [Streamlit Cloud](https://streamlit.io/cloud) can be accessed [here](https://anushkadesai077-data-eng-assignment01-finalstreamlit-app-p0g6vh.streamlit.app/).

## Data Sources
The National Oceanic and Atmospheric Administration (NOAA) is a government agency responsible for monitoring the weather and climate of the United States. It operates two types of satellites, the [Geostationary Operational Environmental Satellite (GOES)](https://www.goes.noaa.gov) and the [Next Generation Weather Radar (NexRad)](https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar) , which collect data on various meteorological phenomena. This data is then made publicly available through the NOAA website, allowing data analysts to easily access it. We have aimed to build a data exploration tool that leverages these publicly available data sources to simplify the process of downloading and analyzing the data.


## SQLite DB
After the metadata is scraped and stored as dataframes each corresponding to GOES18,NexRad and NexRad location maps, we first check if the database exists and initialize it if there is no database. Once a connection to the database is established, SQL queries are made to create tables to store the scraped data (GOES, NexRad and  NexRad location maps) in the [SQLite](https://www.sqlite.org/index.html) database. The tables are named GOES_METADATA, NEXRAD_METADATA and MAPDATA_NEXRAD.In order to enable the users to search by field criteria on Streamlit UI, they should be presented with the values based on their selection. This is done in the backend through SQL queries to the database to fetch data depending on the user’s selections dynamically.


## Streamlit
The data exploration tool for the Geospatial startup uses the Python library [Streamlit](https://streamlit.iohttps://streamlit.io) for its user interface. The tool offers a user-friendly experience with three distinct pages, each dedicated to NexRad, GOES, and NexRad location maps. On each page, users can choose between downloading satellite data based on filename or specific field criteria. The UI then displays a download link to the S3 bucket, enabling users to successfully retrieve the desired satellite images.

### Steps:
1. Install Streamlit package

```
pip install streamlit
```

2. Create a new file [streamlit_app.py](streamlit_app.py) to build a UI for the app. Code snippet for main function, depicting 3 different pages for GOES, NEXRAD and NEXRAD locations Map:
```
def main():
    st.set_page_config(page_title="Weather Data Files", layout="wide")
    page = st.sidebar.selectbox("Select a page", ["GOES-18", "NEXRAD", "NEXRAD Locations - Map"])   #main options of streamlit app

    if page == "GOES-18":
        with st.spinner("Loading..."): #spinner element
            goes_main()
    elif page == "NEXRAD":
        with st.spinner("Loading..."): #spinner element
            nexrad_main()
    elif page == "NEXRAD Locations - Map":
        with st.spinner("Generating map..."): #spinner element
            map_main()

```
3. Run the code
```
streamlit run streamlit_app.py
```



## Unit Testing
[PyTest](https://docs.pytest.org/en/7.1.x/contents.html) framework implemented to write tests which is easy to use but can be scaled to support functional testing for applications and libraries.

### Steps:
1. Install PyTest package
```
pip3 install pytest

#For HTML PyTest Report, Install package:
pip3 install pytest-html
```

2. Create Tests
* Create a new file [test.py](test.py), containing test functions
* Implemented testing functions `test_gen_goes_url(), test_gen_nexrad_url()` that tests functions `generate_goes_url(filename), generate_nexrad_url(filename)` which takes goes and nexrad filenames to generate respective urls.

```
# Code snippet for test functions

def test_gen_goes_url():
    assert generate_goes_url(fileGOES1) == urlGOES1
def test_gen_nexrad_url():
    assert generate_nexrad_url(fileNEXRAD1) == urlNEXRAD1
    
```
3. Run tests
```
pytest -v test.py
```
4. Export test result to log or html file
```
# Export to log file
pytest -v test.py > test_results.log

# Export to html file 
pytest --html=test_results.html test.py
```

## Great Expectations
[Great Expectations](https://docs.greatexpectations.io/docs/) is a tool used to validate, document and profile data in order to eliminate pipeline debt. The python library has been used on extracted GOES18 and NEXRAD csv data in this assignment.

### Steps

**1. Setup**

1.1. Install Great_Expectation module
```
pip3 install great_expectations
```
1.2. Verify version
```
great_expectations --version
```
output:`great_expectations, version 0.15.47`

1.3. Initialize Base Directory
```
great_expectations init
```
- Change working directory to Great Expectations base directory
```
cd great_expectations
```
- Create data folder for datasource to import `GOES18` and `NEXRAD` data

1.4. Import data into Repo

> GOES18

> NEXRAD

**2. Datasource**

Configured datasources in order to connect to `GOES18` and `NEXRAD` data.

2.1. Create datasource with CLI

```
great_expectations datasource new
```

*Options to select from prompt:*

> `1` - Local File 
>
> `1` - Pandas
>
> `data` - Relative path to GOES and NEXRAD datasets

- `datasource_new` python notebook is generated

* Rename datasource name i.e. `goes18-nexrad_datasource` 

* Edit `example.yml` file to ignore non csv files

```
example_yaml = f"""
name: goes18-nexrad_datasource
class_name: Datasource
execution_engine:
  class_name: PandasExecutionEngine
data_connectors:
  default_inferred_data_connector_name:
    class_name: InferredAssetFilesystemDataConnector
    base_directory: data
    default_regex:
      group_names:
        - data_asset_name
      pattern: (.*)\.csv
  default_runtime_data_connector_name:
    class_name: RuntimeDataConnector
    assets:
      my_runtime_asset_name:
        batch_identifiers:
          - runtime_batch_identifier_name
"""
print(example_yaml)
```

- Save the datasource Configuration and close Jupyter notebook
- Wait for terminal to show `Saving file at /datasource_new.ipynb`

**3. Expectations**

3.1 Create Expectation Suite with CLI

```
great_expectations suite new
```

*Options to select from prompt:*

>`3` - Automatically, using a Data Assistant
>
>`1` - Select index of file `goes18_db_extract.csv` 
>
>*or*
>
>`2` - Select index of file `nexrad_db_extract.csv`
>
> Suite Name: `goes18_suite` or `nexrad_suite` based on data file selected from prompt

*Note: Proceed with steps 3 and onwards for each data file at a time.*

- suite python notebook is generated

- Update `exclude_column_names`:

  - `goes18_suite`
  
 
  ```
  exclude_column_names = [
  # "id",
  # "product",
  # "year",
  # "day",
  # "hour",
  ]
  ```
  
  - `nexrad_suite`
  
  
  ```
  exclude_column_names = [
  # "id",
  # "year",
  # "month",
  # "day",
  # "ground_station",
  ]
  ```
 - Run all cells to create default expectation and analyze the result

 - Wait for terminal to show `Saving file at /*.ipynb`

 - Modify JSON files for suite as per need
 
 For `goes18_suite`:
 
 ```
 great_expectations suite edit goes18_suite
 ```
 
  For `nexrad_suite`:
 
 ```
 great_expectations suite edit nexrad_suite
 ```
 
 *Options to select from prompt:*
 
 >`1` - Manually, without interacting with a sample batch of data (default)
 
 
**4. Data Validation**

4.1. Create Checkpoint 

For `GOES18` checkpoint:

```
great_expectations checkpoint new goes18_checkpoint_v0.1
```

For `NEXRAD` checkpoint:
```
great_expectations checkpoint new nexrad_checkpoint_v0.1
```

- checkpoint python notebook is generated, run all cells to generate report in new page

**5. Deploy using GitHub Actions**

 - Go to Project Settings
 - Navigate to GitHub Pages 
 - Select `GitHub Actions` as source for build and deployment
 - Configure Static HTML for GitHub Actions workflow to deploy static files in a repository without a build
 - Set path to `great_expectations/uncommitted/data_docs/local_site` in `static.yml` file
 - Commit changes

-----
> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
> 
> Vraj: 25%, Poojitha: 25%, Merwin: 25%, Anushka: 25%
-----


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


    

   [Next Generation Weather Radar (NexRad)]: <https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar>
   [Geostationary Operational Environmental Satellite (GOES)]: <https://www.goes.noaa.gov>
   
