import xml.etree.ElementTree as ET
import JourneyDuration
import Constants
import re

def more_details_for_trip(response):
    namespace = Constants.NAMESPACE
    first_trip = extract_first_trip_from_response(response,namespace)
    list_of_stations= list_trip_stations(first_trip)
    list_of_connections = list_trip_connections(first_trip,namespace)
    trip_details = merge_connections_and_stations(list_of_connections,list_of_stations)
    alexa_speech = process_list_to_speech(trip_details, first_trip)
    return alexa_speech

def extract_first_trip_from_response(response, namespace):
    root = ET.fromstring(response.content)
    all_trips = root.findall(".//ns:Trip", namespace)
    #It can happen, that a trip gets canceled
    #Then it searches for the first trip which is avialable which always starts with "valid" or "alternative"
    for trip in all_trips: 
        if 'valid' not in trip.attrib or trip.get("alternative") == True: 
            return trip
    raise Exception.add_note("FEHLER bei Tripsuche")

def list_trip_stations(Trip):
    unformatted_station_list = Trip.get('ctxRecon')
    #Filtere die Location, aber nur jedes zweite weil es sich wiederholt
    formatted_station_list = re.findall(r"@O=([^@]+)@", unformatted_station_list)
    formatted_station_list_without_duplicates = formatted_station_list[1::2]
    return formatted_station_list_without_duplicates

def list_trip_connections(first_trip,namespace):
    connection_list = []
    for connection in first_trip.findall(".//ns:Leg", namespace):
        connection_info = extract_connection_details(connection)
        connection_list.append(connection_info)
    return connection_list

def extract_connection_details(connection):
    bus_number = connection.get('name')
    connection_duration = re.findall(r'\d+', connection.get('duration'))[0]
    travel_direction = connection.get('direction')
    connection_list = { 
        'Bus_line': bus_number,
        'Dauer': connection_duration,
        'Richtung': travel_direction
    }   
    return connection_list

def merge_connections_and_stations(connections, stations):
    for i in range(len(connections)):
        connections[i]['bis'] = stations[i]
    return connections

def process_list_to_speech (trip_details,trip):
    depatureTime = JourneyDuration.extract_Depature_Time_from_Trip(trip)
    respond = "Laufe um " + depatureTime + " zum " + trip_details[0]["bis"]+ ". "
    for i in range(1,len(trip_details)):
        transport_Mittel = trip_details[i]["Bus_line"]
        fahrtrichtung = trip_details[i]["Richtung"]
        fahrtziel = trip_details[i]["bis"]
        if transport_Mittel == "Fußweg":
            respond = respond + "Laufe von dort bis " + fahrtziel + ". " 
        else: 
            respond = respond + "Nehme von da " + transport_Mittel + " Richtung " + fahrtrichtung + ", bis " + fahrtziel + ". "
    return respond


alexaspeech, response = JourneyDuration.getAlexaFormattedTravelTime("3004734")
result  = more_details_for_trip(response)
print(result)
