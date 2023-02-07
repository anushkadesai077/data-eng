import streamlit as st
import boto3
import re
import scraper_mapdata
import pandas as pd

# Initialize the S3 client
s3 = boto3.client("s3")

states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", 
"IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS",
 "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", 
 "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

nexrad_stations = {
"AK": ["PAHC", "PAHO", "PAJK", "PAKN"],
"AL": ["KBMX", "KHTX", "KMXX", "KEOX"],
"AR": ["KLZK", "KLRF", "KSHV"],
"AZ": ["KEMX", "KFDX", "KPSR"],
"CA": ["KDAX", "KHNX", "KMUX"],
"CO": ["KCYS", "KFTG", "KGRB"],
"CT": ["KOKX"],
"DC": ["KLWX"],
"DE": ["KDOX"],
"FL": ["KAMX", "KBYX", "KEYW", "KMLB"],
"GA": ["KFFC", "KJGX"],
"HI": ["PHKI"],
"IA": ["KDMX", "KDVX", "KOAX"],
"ID": ["KBOI", "KIDA", "KPIH"],
"IL": ["KILX", "KLOT"],
"IN": ["KIND", "KLOT"],
"KS": ["KDDC", "KGLD", "KICT"],
"KY": ["KLMK", "KPAH"],
"LA": ["KLCH", "KLIX"],
"MA": ["KBOX"],
"MD": ["KMTN"],
"ME": ["KGYX"],
"MI": ["KGRR", "KDTX"],
"MN": ["KMPX"],
"MO": ["KDZX", "KSGF"],
"MS": ["KJAN", "KMOB"],
"MT": ["KGGW", "KTFX"],
"NC": ["KGSP", "KMHX"],
"ND": ["KBIS", "KFGF"],
"NE": ["KLBF", "KOAX"],
"NH": ["KGYX"],
"NJ": ["KPHI"],
"NM": ["KABQ", "KFMX"],
"NV": ["KREV"],
"NY": ["KALY", "KBGM"],
"OH": ["KCLE", "KILN"],
"OK": ["KFDR", "KOUN"],
"OR": ["KPDT", "KRTX"],
"PA": ["KCCX", "KPBZ"],
"RI": ["KBOX"],
"SC": ["KCAE", "KCHS"],
"SD": ["KABR", "KFSD"],
"TN": ["KHTX", "KMEG"],
"TX": ["KBRO", "KCRP", "KEWX", "KFWD", "KGRK", "KHGX", "KLCH", "KLZK", "KMAF", "KMRX", "KSHV", "KSJT"],
"UT": ["KPUC"],
"VT": ["KBTV"],
"VA": ["KAKQ", "KLWX", "KMHX"],
"WA": ["KATX", "KOTX"],
"WV": ["KRLX"],
"WI": ["KARX", "KGRB", "KMKX"],
"WY": ["KCYS", "KRIW"]
}

def fetch_files_by_fields(year, day, hour):
    # Search the files by filtering through the fields
    pass

def fetch_file_by_filename(filename):
    # Search the file by its complete name
    pass

def goes_fetch_file_by_filename(file_name):
    # # Search the file by its complete name
    # pattern = re.compile(r'OR_ABI-L1b-RadC-M\dC\d\d_G\d\d_s\d{15}_e\d{15}_c\d{15}\.nc')
    # if not pattern.match(filename):
    #     raise ValueError("Invalid filename format")
    
    # elements = filename.split("_")
    # year = elements[3][3:7]
    # day_of_year = elements[3][7:10]
    # path = f"ABI-L1b-RadC/{year}/{day_of_year}/{elements[4][0:3]}/"
    # link = f"https://noaa-goes18.s3.amazonaws.com/{path}{filename}"
    
    # return link
    input_url = "https://noaa-goes18.s3.amazonaws.com/"
    file_name = file_name.strip()
    file_list = file_name.split("_")
    sublist=file_list[1].split("-")
    if (sublist[2].isalpha()) is False:
        sublist[2] = sublist[2][:-1]
    sublist_date = file_list[3]

    final_url = input_url+"-".join(sublist[0:3])+'/'+sublist_date[1:5]+'/'+sublist_date[5:8]+'/'+sublist_date[8:10]+'/'+file_name

    return final_url

def copy_file_to_bucket(file_path):
    # Copy the selected file to your S3 bucket
    pass

def retrieve_url_from_bucket(file_path):
    # Retrieve the URL of the file from your S3 bucket
    pass


def main():
    st.set_page_config(page_title="Weather Data Files", layout="wide")
    page = st.sidebar.selectbox("Select a page", ["NEXRAD", "GOES-18", "NEXRAD Locations - Map"])

    if page == "NEXRAD":
        nexrad_main()
    elif page == "GOES-18":
        goes_main()
    elif page == "NEXRAD Locations - Map":
        map_main()


def nexrad_main():
    #st.set_page_config(page_title="NEXRAD Doppler Radar Sites", page_icon=":radar_dish:", layout="wide")

    st.title("NEXRAD Doppler Radar Sites")
    st.markdown(
        """
        <style>
            .title {
                text-align: center;
                color: #2F80ED;
            }
        </style>
        <h2 class="title">Find the Latest NEXRAD Radar Data</h2>
        <p>Use the following options to search for NEXRAD radar data.</p>
        """,
        unsafe_allow_html=True,
    )

    ##search options
    search_by_fields = st.sidebar.checkbox("Search by Fields")
    search_by_filename = st.sidebar.checkbox("Search by Filename")

    # search by fields
    if search_by_fields:
        year = st.selectbox("Year", [2020, 2021, 2022, 2023], key='year')
        month = st.selectbox("Month", range(1,13), key='month')
        day = st.selectbox("Day", range(1,32), key='day')
        state = st.selectbox("State", states, key='state')
        station = st.selectbox("NEXRAD Station", nexrad_stations[state], key='station')

        #display selections
        st.write("Selected values: Year:", year, ", Month:", month, ", Day:", day, ", State:", state, ", Station:", station)

        files = fetch_files_by_fields(year, month, day, state, station)

        if files:
            file_select = st.selectbox("Select a file", files, key='file')
        else:
            st.warning("No files found.")

        if file_select:
            file_path = copy_file_to_bucket(file_select)
            url = retrieve_url_from_bucket(file_path)
            st.write("URL of the selected file:", url)
            st.success("File copied successfully.")

        # search by filename
    if search_by_filename:
        filename = st.text_input("Enter the filename")

        file = fetch_file_by_filename(filename)

        if file:
            st.write("Link of the file available on NEXRAD bucket:", file)

def goes_main():
    #st.set_page_config(page_title="GOES Satellite Sites", page_icon=":satellite:", layout="wide")

    st.title("GOES Satellite Sites")
    st.markdown(
        """
        <style>
            .title {
                text-align: center;
                color: #2F80ED;
            }
        </style>
        <h2 class="title">Find the Latest GOES Radar Data</h2>
        <p>Use the following options to search for GOES radar data.</p>
        """,
        unsafe_allow_html=True,
    )

    ##search options
    search_by_fields = st.sidebar.checkbox("Search by Fields")
    search_by_filename = st.sidebar.checkbox("Search by Filename")

    # search by fields
    if search_by_fields:
        year = st.selectbox("Year", [2022, 2023], key='year')
        #month = st.selectbox("Month", range(1,13), key='month')
        if year==2022:
            day = st.selectbox("Day", range(209,366), key='day')
        elif year==2023:
            day = st.selectbox("Day", range(1,33), key='day')
        hour = st.selectbox("Hour", range(0,25), key='hour')
        station = 'ABI-L1b-RadC'


        #display selections
        st.write("Selected values: Year:", year, ", Day:", day, ", Station:", station)

        files = fetch_files_by_fields(year, day, hour)

        if files:
            file_select = st.selectbox("Select a file", files, key='file')
        else:
            st.warning("No files found.")

        if file_select:
            file_path = copy_file_to_bucket(file_select)
            url = retrieve_url_from_bucket(file_path)
            st.write("URL of the selected file:", url)
            st.success("File copied successfully.")

    # search by filename
    if search_by_filename:
        filename = st.text_input("Enter the filename")

        file = goes_fetch_file_by_filename(filename)

        st.write("Link of the file available on GOES bucket:",filename)

        if file:
            st.write("Link of the file available on GOES bucket:",file)


def map_main():
    # st.title("Map Page")
    st.markdown(
        """
        <h1 style="background-color:#1c1c1c; color: white; text-align: center; padding: 15px; border-radius: 10px">
            Map Page
        </h1>
        """,
        unsafe_allow_html=True,
    )

    map_data = scraper_mapdata.get_map_data()
    st.plotly_chart(map_data, use_container_width=True, height=700)


if __name__ == "__main__":
    main()