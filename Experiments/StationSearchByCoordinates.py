import requests
import StationID as StationID
import xml.etree.ElementTree as ET
import Constants

def getStationsByCoordinates (coordLat, coordLong, radius):
    response = send_Request(coordLat,coordLong,radius)
    validate(response)
    list_Of_Stations = list_Stations(response)
    return list_Of_Stations


def send_Request(coordLat, coordLong, radius):
    base_url = "https://www.rmv.de/hapi/location.nearbystops"
    params = {
        'accessId': Constants.ACCESS_ID,
        'originCoordLat': coordLat,         
        'originCoordLong': coordLong,      
        "r": radius,                        
    }
    response = requests.get(base_url, params=params)
    return response


def validate (response: requests.Response):
    if response.status_code == 200:
        return
    else: raise Exception.add_note("FEHLER")


def list_Stations(response):
    list_Of_Stations = []
    allStop = extractAllStopsFromResponse(response)

    for stop in allStop:
        stop_Data = extractUsefullDataFromStop(stop)
        list_Of_Stations.append(stop_Data)

    return list_Of_Stations


def extractAllStopsFromResponse(response):
    namespace = {'ns': 'http://hacon.de/hafas/proxy/hafas-proxy'}
    xml_formated_response = ET.fromstring(response.content)
    allStop = xml_formated_response.findall(".//ns:StopLocation", namespace) #search for all the stops from response
    return allStop


def extractUsefullDataFromStop(stop):
        stop_info = { 
            'Station': stop.get('name'),
            'ID': stop.get('extId'),
            'Distanz': stop.get('dist')
        }   
        return stop_info

list = getStationsByCoordinates(49.880644,8.654501,800)
print(list)
















#TESTER

"""base_url = "https://www.rmv.de/hapi/location.nearbystops"
params = {
    'accessId': '308cbcac-a06d-4b6a-8913-ba43435a37ef',
    'originCoordLat': 49.880644,  # Ersetzen Sie dies mit der ID der Start-Haltestelle
    'originCoordLong': 8.654501,     # Ersetzen Sie dies mit der ID der Ziel-Haltestelle
    "r": 800,                   #radius
}
response = requests.get(base_url, params=params)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    root = ET.fromstring(response.content)

    for child in root:
        print(child.tag, child.attrib)
        for subchild in child:
            print(subchild.tag, subchild.attrib)
            for subchildd in subchild:
                print(subchildd.tag, subchildd.attrib)  """

