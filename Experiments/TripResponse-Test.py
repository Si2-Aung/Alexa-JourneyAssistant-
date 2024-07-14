import requests
import StationID
import xml.etree.ElementTree as ET
import CurrentTime 
import Constants


#Define the Parameters and request
current_time_with_delta = CurrentTime.get_currentTime_with_delta(13)
current_date = current_time_with_delta.date()
base_url = "https://www.rmv.de/hapi/trip"
originId = StationID.getID("Darmstadt Friedrich-Ebert-Platz")
destID = StationID.getID("Darmstadt Hauptbahnhof")
params = {
    'accessId': Constants.ACCESS_ID,
    'originCoordLat': Constants.ORIGIN_COORD_LAT,  
    'originCoordLong': Constants.ORIGIN_COORD_LONG,    
    "r": 1500,
    'destId': destID,     # Ersetzen Sie dies mit der ID der Ziel-Haltestelle
    "date": current_date.strftime("%Y-%m-%d"),  # Aktuelles Datum
    "time": current_time_with_delta.strftime("%H:%M"),  # Requested Time
    "originwalk" : "1,0,5000",
    "numF": 1,
    "tariff" : 0
    # Fügen Sie hier weitere Parameter hinzu, falls benötigt
}

# Senden der Anfrage
response = requests.get(base_url, params=params)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    root = ET.fromstring(response.content)
    for child in root:
         print(child.tag, child.attrib)
         for subchild in child:
             print(subchild.tag, subchild.attrib)
             for subchildd in subchild:
                 print(subchildd.tag, subchildd.attrib)
         print("______________________________________________________________________________________________________________________")

else:
    # Es gab ein Problem mit der Anfrage
    print('Fehler bei der Anfrage:', response.status_code)
    print("Antworttext:", response.text)

