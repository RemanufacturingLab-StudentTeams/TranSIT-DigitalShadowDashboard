# Instructions for running the Digital Shadow Dashboard (DSD)

## Basic setup

### 1. Installing required packages

Before running the digital shadow dashboard, first the required python packages need to be installed.

To start, open the terminal/command prompt. Ensure that the working directory is "Digital Shadow Dashboard". You can navigate to it 
using "cd" and "cd . .". The last name in the file path should say "\Digital Shadow Dashboard>"

Once you have navigated to the current directory, copy and run the following:

    pip install -r "requirements.txt"

This will install the required python packages used by the Digital Shadow Dashboard.

### 2. Running the web app

To run the web app, open the "Dash app.py" python script, I recommend doing this in a text editor like PyCharm or VS Code.
You can also just run the python file directly. Run the script, and it will launch the web app. 
If everything works correctly, you should see a log that looks like this:
    
    Dash is running on http://127.0.0.1:8050/
    
     * Serving Flask app 'Dash app'
       * Debug mode: on

To open the app, click the link, or copy "http://127.0.0.1:8050/" into your browser.

## Switching floorplans

### 1. Preparing new floorplan

To put a new floorplan, please ensure that it is formatted as a svg. It is recommended to first 'clean up' the floorplan by
removing any unnecessary information not needed for part location visualization. Some examples of information not needed for
this app: Fire escape information, grid lines, unnecessary icons. 

The more the floorplan is "cleaned up", the faster the app will run and load, and the easier it will be for users to interpret
information. It is also recommended to change the image to greyscale/black and white, so that overlayed information is easier to see.

Once this is done, name the svg file "FLOORPLAN.svg", and place it within the assets directory of the project. 

### 2. Updating location names

Once the new floorplan is added, ensure that the locations are correct by navigating to the "LOCATIONS.JSON" file in the data directory.
Additional data can be added for each location, but currently, the digital shadow only requires the names to be accurate. 

### 3. Adding coordinates of new locations 

Finally, the correct coordinates for each location must be added. In the data directory is placed the
POSITIONS.JSON file. Each of the locations mentioned in the LOCATIONS.JSON file must also be added here, 
along with its coordinates on the floorplan.

## Changing input data

To change input data, the simplest is using a new csv data file, to review historical manufacturing data, however this 
would not show changes in real time. Different options are included below for how the DSD can be configured. 

### 1. Replacing CSV file

In order to use a different cvs file, please make sure that the headers match the existing csv file called "event_data.csv"
in the "data" directory, and that the data formats are the same. The headers need to be: "Timestamp,id,status,location,Sublocation Name"

Once prepared, name your csv file "event_data.csv" and replace the previous csv file with the new one.

### 2. InfluxDB Input

This option currently requires code to be written by the user that periodically, or using a button for example, sends queries
to an influxDB time series database, and so updates in real time. The data will have to be converted to a pandas dataframe 
and then can be processed the same.

I have already used InfluxDB in the past, and will add an updated InfluxDB version of the code in future that can be used in this version.

### 3. API calls

Another option is to use API calls to retrieve data from the MES or ERP system, this is ideal for viewing it in real time and 
integrating the DSD directly with an industrial SMEs infrastructure, but requires an API call system to already be set up.

REST API was used by an SME partner and this proved a good option for retrieving data.

The updated code that can be used to do this will be added in the future.