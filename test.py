import xml.etree.ElementTree as ET

def main():
    dataPath = "data/export.xml";
    dataDict = extractData(dataPath)

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
        if child.tag == 'Record':
            attrib = child.attrib
            if attrib['type'] in dict:
                dict[attrib['type']].append(attrib)
            else:
                dict[attrib['type']] = [attrib]

    print("different data types: ")
    for k,v in dict.items():
        print("key: '%s',  count: %s" %(k, len(v)))

    return dict


if __name__ == "__main__":
    main()
