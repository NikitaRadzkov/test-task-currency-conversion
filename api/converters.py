from io import StringIO

from xml.etree import ElementTree as ET

import pandas as pd

from api.constants import TIME_PERIOD_COLUMN_NAME, OBS_VALUE_COLUMN_NAME


class EuropeanCentralBankXMLDataToDataFrameConverter:
    def __init__(self, data: str):
        self._data = data
        self._root = ET.fromstring(data)

    def get_namespaces(self):
        return {
            key: value
            for _, (key, value) in ET.iterparse(
                    StringIO(self._data), events=("start-ns",),
                )
        }

    @property
    def generic_namespace(self):
        return self.get_namespaces()['generic']

    def process(self) -> pd.DataFrame:
        result = []
        for elem in self._root.findall(path=".//{%s}Obs" % self.generic_namespace):
            time_period = elem.find(
                path=".//{%s}ObsDimension" % self.generic_namespace
            ).attrib["value"]
            obs_value = float(
                elem.find(path=".//{%s}ObsValue" % self.generic_namespace).attrib[
                    "value"
                ]
            )

            result.append({
                TIME_PERIOD_COLUMN_NAME: time_period,
                OBS_VALUE_COLUMN_NAME: obs_value,
            })

        return pd.DataFrame(data=result)

