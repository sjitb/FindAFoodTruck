# Find A Food Truck
This application will return the list of open food trucks.
The data source is provided by the 


## Environment Set-up:
1. Create Virtual Environment:<br>
`python -m venv env`
2. Launch Python Virtual Environment by executing:<br>
`.\env\Scripts\activate`
3. Install required libraries listed in `requirements.txt`<br>
`pip install -r requirements.txt`

## Execution and Results:
1. Run the app by executing: <br>
`python show_open_food_trucks.py`
2. The user is asked to input 

## Components:
1. `show_open_food_trucks.py`: driver function <br>
2. `api_client.py`: FoodTruckFinder class implements the rest client <br>
3. `utilities.py`: contains utility functions such as retrieving current time and day, and formatting output  <br>
4. `config.ini`: config file contains base url and app token

## Implementation Logic:
The goal was to utilize most of the functionalities of the Socrata API<br>
The base url for the API call is: <https://data.sfgov.org/resource/jjew-r69b.json><br>
### Authentication:
Authentication is done by using App Token obtained from <https://data.sfgov.org><br>
The App Token is passed along in the request URL in the form of the `$$app_token` parameter<br>
### Data Filter:
The built in filters utilized:<br>
1. `dayofweekstr`: Filter result by the current day of the week. Example: `?dayofweekstr=Saturday`<br>
2. `$where`: Use the structure of the where clause and use `start24` and `end24` fields to filter results for food trucks open at the current time. Example: `$where=start24<'18:52'and end24>'18:52'`<br>
3. `$select`: Use the select clause to fetch only the required fields, `applicant` and `location` in this case. This reduces the size of the response object. Example: `$select=applicant,location`<br>
4. `$order`: Use the order clause to order the response by a specific field, `applicant` in this case. Example: `$order=applicant`<br>
5. `$limit and $offset`: Use limit and offset parameter to implement pagination. Example: `$limit=5&$offset=0`<br>
<br>
Sample API call:<br>
https://data.sfgov.org/resource/jjew-r69b.json?$$app_token=###########&dayofweekstr=Saturday&$where=start24<'19:29'and end24>'19:29'&$select=applicant,location&$order=applicant&$limit=10&$offset=50
