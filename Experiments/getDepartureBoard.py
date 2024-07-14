import requests
import StationID as StationID
import xml.etree.ElementTree as ET
import CurrentTime
import Constants

def main(Station_Name):
    departure_info = []
    if Station_Name in["Friedrich-Ebert-Platz", "friedrih ebert Platz", "FRIEDRICH EBERT PLATZ"]:
        departure_info = process_FEP_depatures()
    elif Station_Name in["Willy-Brandt-Platz", "Willy brant  Platz", "willy brantd platz", "WILLY BRANDT PLATZ", "Willy Brandt PLATZ"]:
        departure_info = process_WBP_depatures()
    elif Station_Name in[ "Kopernikusplatz", "kopernikusplatz"]:
        departure_info = process_Kopernikus_depatures()
    elif Station_Name in ["Pallaswiesenstraße", "pallaswiesenstraße"]:
        departure_info = process_Pallas_depatures()
    else: departure_info = process_other_depatures(Station_Name)
    
    if not departure_info:
        return ("In der nächsten Stunde fährt dort kein Bus ab, laufe lieber")
    
    else:
        first_departure = departure_info[0]  # Das erste Element
        first_name = first_departure.get("name")
        first_time = first_departure.get("rTime")

        if len(departure_info) > 1:
            second_departure = departure_info[1]  # Das zweite Element, falls vorhanden
            second_name = second_departure.get("name")
            second_time = second_departure.get("rTime")

    result = "Als nächstes fährt " + first_name + " um " + first_time + " dann fährt " + second_name + " um " + second_time
    return result


def get_departure_info(Station_Name, time_added, maxJourneys):
    #Get the Current time with added delta 
    current_time_with_delta = CurrentTime.get_currentTime_with_delta(time_added)
    current_date = current_time_with_delta.date()

    #Define the Parameters and request
    base_url = "https://www.rmv.de/hapi/departureBoard"
    id = StationID.getID(Station_Name)
    params = {
        'accessId': Constants.ACCESS_ID,
        "id": id,  #Station-ID 
        "date": current_date.strftime("%Y-%m-%d"),  # Aktuelles Datum
        "time": current_time_with_delta.strftime("%H:%M"),  # Requested Time
        "duration": 60,  # Request duration in Minutes
        "maxJourneys": maxJourneys,  # Maximale Anzahl der angezeigten Fahrten
        "type": "DEP",  # Station Departure Board
    }
    response = requests.get(base_url, params=params)

    # Check if somthing went wrong
    if response.status_code == 200:
        data = response.text
        return data
    
    else:
        return (f"Fehler: {response.status_code}")



def process_FEP_depatures():
    # Get DepataureBoard
    depature_data_XML = get_departure_info("Darmstadt Friedrich-Ebert-Platz", 6, 4)
    departure_info = []
    
    #Filter the DepataureBoard and get the Name and time of the of the upcoming Bus 
    root = ET.fromstring(depature_data_XML)
    for departure_elem in root.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
        direction= departure_elem.get("direction")
        #Filter the direction I need
        if direction == "Darmstadt TU-Lichtwiese/Campus":
            name = departure_elem.get("name")
            time = departure_elem.get("time")
            rTime = departure_elem.get("rtTime")
        else: continue

        #If there is no Realtime available
        if rTime is None:
            rTime = time

        departure_info.append({
            "name": name,
            "rTime": rTime,
        })
    return departure_info


def process_WBP_depatures():
    # Get DepataureBoard
    depature_data_XML = get_departure_info("Darmstadt Willy-Brandt-Platz", 12,15)
    departure_info = []
    root = ET.fromstring(depature_data_XML)
    #Filter the DepataureBoard and get the Name and time of the of the upcoming Bus 
    for departure_elem in root.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
        direction= departure_elem.get("direction")
        #Filter the direction I need
        if direction in ["Darmstadt Hauptbahnhof", "Darmstadt Kleyerstraße"]:
            name = departure_elem.get("name")
            time = departure_elem.get("time")
            rTime = departure_elem.get("rtTime")
        else: continue

        #If there is no Realtime available
        if rTime is None:
            rTime = time
        
        departure_info.append({
            "name": name,
            "rTime": rTime,
        })
    return departure_info

def process_Pallas_depatures():
    depature_data_XML = get_departure_info("Darmstadt Pallaswiesenstraße", 8, 4)
    departure_info = []
    root = ET.fromstring(depature_data_XML)
    for departure_elem in root.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
        direction= departure_elem.get("direction")
        if direction in ["Darmstadt Böllenfalltor", "Darmstadt Schloss", "Alsbach-Hähnlein-Alsbach Am Hinkelstein",
                         "Darmstadt-Eberstadt Frankenstein","Darmstadt Hauptbahnhof","Darmstadt Mathildenplatz"]:
            name = departure_elem.get("name")
            time = departure_elem.get("time")
            rTime = departure_elem.get("rtTime")
        else: continue
        if rTime is None:
            rTime = time
        departure_info.append({
            "name": name,
            "rTime": rTime,
        })
    return departure_info

def process_Kopernikus_depatures():
    depature_data_XML = get_departure_info("Darmstadt Kopernikusplatz", 15, 7)
    departure_info = []
    root = ET.fromstring(depature_data_XML)
    for departure_elem in root.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
        direction= departure_elem.get("direction")
        if direction in ["Darmstadt Anne-Frank-Straße","Darmstadt Kleyerstraße"]:
            name = departure_elem.get("name")
            time = departure_elem.get("time")
            rTime = departure_elem.get("rtTime")
        else: continue
        if rTime is None:
            rTime = time
        departure_info.append({
            "name": name,
            "rTime": rTime,
        })
    return departure_info

def process_other_depatures(Station_name):
    name = "Darmstadt " + Station_name
    depature_data_XML = get_departure_info(name,5, 4)
    departure_info = []
    root = ET.fromstring(depature_data_XML)
    for departure_elem in root.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
        name = departure_elem.get("name")
        time = departure_elem.get("time")
        rTime = departure_elem.get("rtTime")
        if rTime is None:
            rTime = time
        departure_info.append({
            "name": name,
            "rTime": rTime,
        })
    return departure_info

# Beispielaufruf mit XML-Datenstring
data = get_departure_info("Darmstadt Willy-Brandt-Platz",15,1)
root = ET.fromstring(data)
for child in root:
    print(child.tag, child.attrib)
    for subchild in child:
        print(subchild.tag, subchild.attrib)
        for subsubchild in subchild:
            print(subsubchild.tag, subsubchild.attrib)
        
ergebnis = main("Willy-Brandt-Platz")
print(ergebnis)