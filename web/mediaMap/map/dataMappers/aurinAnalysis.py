import json
#COMP90024 TEAM 20


with open('../static/map/img/aurin.geojson') as f:
    geojson = json.load(f)

with open('../static/map/img/aurinData.json') as data:
    j2 = json.load(data)

    for feature in geojson["features"]:
        property = feature["properties"]
        suburb = property['SA3_NAME16']
        for feature in j2['features']:
            properties = feature["properties"]
            sub = properties['SSC_NAME']
            median = properties['median11']
            if sub == suburb:
                if median is None:
                    properties["color"] = "#B0C4DE"
                elif float(median) < 30000:
                    properties["color"] = "#B0E0E6"
                elif float(median) < 40000:
                    properties["color"] = "#00BFFF"
                elif float(median) < 50000:
                    properties["color"] = "#1E90FF"
                elif float(median) < 60000:
                    properties["color"] = "#4682B4"
                else:
                    properties["color"] = "#4169E1"

    with open('../static/map/res/aurin.geojson', 'w') as outFile:
        json.dump(geojson, outFile)
