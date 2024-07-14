import requests
import xml.etree.ElementTree as ET
import Constants
def getID (Name_of_Stop):
    
    base_url = "https://www.rmv.de/hapi/location.name"
    params = {
        'accessId': Constants.ACCESS_ID,  
        "input": Name_of_Stop,  
        "maxNo": 1,  # Maximale Anzahl der zurückgegebenen Haltestellen
    }

    # Senden der GET-Anfrage
    response = requests.get(base_url, params=params)

    # Check if somthing went wrong
    if response.status_code == 200:
        stop_information = response.text
        #Extrahiere die StopLocation-ID
        root = ET.fromstring(stop_information)  
        return root.find("{http://hacon.de/hafas/proxy/hafas-proxy}StopLocation").attrib.get("extId")
    
    else:
        return (f"Fehler: {response.status_code}")


"""print(getID("Darmstadt Hauptbahnhof"))"""