import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import constants
import visualizer


def main():
    dataPath = "data/export.xml"
    dataDict = extractData(dataPath)
    desiredStepKeys = ["value", "startDate", "endDate"]
    beginDate = datetime(2019, 1, 1)
    endDate = datetime(2020, 1, 1)

    cleanedStepData = cleanData(dataDict[constants.STEP_KEY], desiredStepKeys)
    print("===== Data Preview =====")
    for i in range(10):
        print(dataDict[constants.FLIGHTS_CLIMBED_KEY][0])
    shortenedData = selectDataTimeframe(cleanedStepData, beginDate, endDate)
    print("===== Step Data Preview =====")
    for i in range(10):
        print(shortenedData[i])
    visualizer.stepHeatmap(shortenedData)

    print("finished main.")


def extractData(xmlPath):
    """Function to extract data from xml format and return a dictionary.

    Parameters
    ----------
    xmlPath : string
        Path of the xml file.

    Returns
    -------
    Dictionary[string] = List
        Dictionary containing extracted data. The keys are the different types
        of data and the values are lists of actual data points.

    """
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    dict = {}

    for child in root:
        # only care about 'Record' children, don't care about 'My' or
        # whatever the other one is
        if child.tag == "Record":
            attrib = child.attrib
            if attrib["type"] in dict:
                dict[attrib["type"]].append(attrib)
            else:
                dict[attrib["type"]] = [attrib]

    print("different data types: ")
    for k, v in dict.items():
        print("key: '%s',  count: %s" % (k, len(v)))

    return dict


def cleanData(rawData, desiredKeys):
    """Given a list of data points (dictiaries), filters out only the
    desiredKeys key values from the dictionaries.

    Parameters
    ----------
    rawData : List[Dictionary{}]
        List of data, datum are dictionaries.
    desiredKeys : List[String]
        List of key values to keep from rawData datum dictionaries.

    Returns
    -------
    List[Dictionary{}]
        Cleaned data.

    """
    cleaned = []
    my_timezone = -400
    for datum in rawData:
        cleanedDatum = {}
        for key in desiredKeys:
            if "Date" in key:
                [time, timezone] = datum[key].rsplit(" ", 1)
                time = datetime.fromisoformat(time)

                # divide by 100 because timezone is -400 (EST)
                hourDiff = (my_timezone - int(timezone)) / 100
                adjustedTime = None
                if hourDiff > 0:
                    adjustedTime = time + timedelta(hours=hourDiff)
                else:
                    adjustedTime = time - timedelta(hours=-hourDiff)
                cleanedDatum[key] = adjustedTime
            else:
                cleanedDatum[key] = datum[key]
        cleaned.append(cleanedDatum)

    # cleaned = [{ key: ( datetime.fromisoformat(datum[key].rsplit(' ', 1)[0]) if ("Date" in key) else datum[key]) for key in desiredKeys } for datum in rawData]
    return cleaned


def selectDataTimeframe(data, beginDate, endDate):
    shortenedData = []
    for datum in data:
        datumDate = datum["startDate"]
        if datumDate < beginDate:
            continue
        if datumDate > endDate:
            break
        shortenedData.append(datum)

    return shortenedData


if __name__ == "__main__":
    main()
