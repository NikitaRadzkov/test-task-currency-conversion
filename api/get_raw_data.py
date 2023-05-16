import pandas as pd
import requests
import xml.etree.ElementTree as ElementTree


def get_raw_data(identifier: str) -> pd.DataFrame:
    url = f"https://sdw-wsrest.ecb.europa.eu/service/data/BP6/{identifier}?detail=dataonly"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    root = ElementTree.fromstring(response.content)

    data = []
    for obs in root.findall(".//generic:Obs",
                            namespaces={"generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}):
        time_period = obs.find("./generic:ObsDimension", namespaces={
            "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}).attrib["value"]
        obs_value = float(obs.find("./generic:ObsValue", namespaces={
            "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}).attrib["value"])
        data.append({"TIME_PERIOD": time_period, "OBS_VALUE": obs_value})

    df = pd.DataFrame(data)
    return df


raw_data = get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")

print("Raw Data", raw_data)
