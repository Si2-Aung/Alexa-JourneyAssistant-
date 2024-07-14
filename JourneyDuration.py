import requests
from datetime import datetime,timedelta
import pytz
import xml.etree.ElementTree as ET
import Constants


def getAlexaFormattedTravelTime(destinationId):
    response = fetch_Trips_to_destination(destinationId)
    validate(response)
    trip = extract_FirstTrip_fromResponse(response)
    departure_time = extract_Depature_Time_from_Trip(trip)
    arrival_time = extract_Arrival_Time_from_Trip(trip)
    travel_time = calculate_travel_time(departure_time,arrival_time)

    alexa_speech = f"Ab {departure_time} wirst du in etwa {travel_time} Minuten um {arrival_time} ankommen. Benötigst du mehr Infos?"
    return alexa_speech, response

def fetch_Trips_to_destination(destinationId):
    current_time_with_delta = get_currentTime_with_delta(5)
    current_date = current_time_with_delta.date().strftime("%Y-%m-%d")
    base_url = "https://www.rmv.de/hapi/trip"
    destID = destinationId
    params = {
    'accessId': Constants.ACCESS_ID,
    'originCoordLat': Constants.ORIGIN_COORD_LAT,  
    'originCoordLong': Constants.ORIGIN_COORD_LONG,     
    "r": 1500,                                              #Max radius to search for stops
    'destId': destID,     
    "date": current_date,  
    "time": current_time_with_delta,  
    "numF": 2,                                              #Amount op trips to fetch
    }
    response= requests.get(base_url, params=params)
    return response

def get_currentTime_with_delta(delta):
    desired_timezone = pytz.timezone('Europe/Berlin')
    current_utc_time = datetime.now(pytz.utc)
    current_time_in_desired_timezone = current_utc_time.astimezone(desired_timezone)
    # Delta is the timeframe that should be added for the trip search
    time_delta = timedelta(minutes=delta)
    result_time = current_time_in_desired_timezone + time_delta
    return result_time.strftime("%H:%M")

def validate (response: requests.Response):
    if response.status_code == 200:
        return
    else: raise Exception.add_note("FEHLER beim Request")

def extract_FirstTrip_fromResponse(response):
    root = ET.fromstring(response.content)
    all_trips = root.findall(".//ns:Trip", Constants.NAMESPACE)

    #It can happen, that a trip gets canceled
    #Then it searches for the first trip which is avialable
    #the next aviable Trip always starts with "valid" or "alternative"
    for trip in all_trips: 
        if 'valid' not in trip.attrib or trip.get("alternative") == True: 
            return trip
    raise Exception.add_note("FEHLER bei Tripsuche")

def extract_Depature_Time_from_Trip(trip):
    depature_time = trip.find(".//ns:Origin", Constants.NAMESPACE).get('time')
    return depature_time

def extract_Arrival_Time_from_Trip(trip):
    arrival_time = trip.find(".//ns:Destination", Constants.NAMESPACE).get('time')
    return arrival_time

def calculate_travel_time(departure_time, arrival_time):
    strpied_departure_time = datetime.strptime(departure_time, '%H:%M:%S')
    strpied_arrival_time = datetime.strptime(arrival_time, '%H:%M:%S')
    
    # Special case, if the next day is reached
    if strpied_arrival_time < strpied_departure_time:
        time_difference = (strpied_arrival_time + timedelta(days=1) - strpied_departure_time).total_seconds() / 60
    else:
        time_difference = (strpied_arrival_time - strpied_departure_time).total_seconds() / 60
    
    return abs(int(time_difference))