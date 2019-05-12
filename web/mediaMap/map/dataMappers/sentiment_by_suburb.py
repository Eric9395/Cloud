import json
#COMP90024 TEAM 20


with open('../static/map/img/sentiment_by_suburbs.geojson') as f:
    geojson = json.load(f)

with open('../static/map/img/sentiment_by_suburbs.geojson') as data:
    json = json.load(data)

    for key in json


    for feature in geojson["features"]:
        properties = feature["properties"]

        sentiment = properties["pos_rate"]

        if sentiment is None:
            properties["color"] = "#8E8080"
        elif float(sentiment) < 0.2:
            properties["color"] = "#FA8072"
        elif float(sentiment) < 0.4:
            properties["color"] = "#F08080"
        elif float(sentiment) < 0.6:
            properties["color"] = "#DC143C"
        elif float(sentiment) < 0.8:
            properties["color"] = "#FF0000"
        else:
            properties["color"] = "FFC6AE"

    with open('../static/map/res/melbourne_suburbs.geojson', 'w') as outFile:
        json.dump(geojson, outFile)
