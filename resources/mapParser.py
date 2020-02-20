import re, json

provinces = {}
vertices = []
polygonPattern = r'<polygon id="([^"]*)" class="[^"]*" points="((?:\d+\.?\d*,\d+\.?\d*\s+)+)"\/>'
nameIdPattern = r'_x3((?:\d_)\d*)_x5F_([\w-]+)'
with open("map.svg") as svgFile:
    #print(help(re.findall))
    polygons = re.findall(polygonPattern, svgFile.read())
    for polygon in polygons:
        print(re.findall(nameIdPattern, polygon[0]), polygon[0])
        try:
            nameId = re.findall(nameIdPattern, polygon[0])[0]
        except IndexError:
            continue
        pid = int(nameId[0].replace("_", ""))
        name = nameId[1]
        vertexList = []
        for point in polygon[1].split():
            lon = float(point.split(",")[0]) / 4000 * (56.55 - -21.55) - 21.55
            lat = float(point.split(",")[1]) / 4000 * (-37.50 - 40.49) + 40.49
            """
            0, 0 -> -21.55, 40.49
            0, 4000 -> 56.55, 40.49
            4000, 4000 -> 56.55, -37.50
            4000, 0 -> -21.55, -37.50

            Longitude: -21.55 to 56.55
            Latitude: -37.50 to 40.49
            """
            for v in range(len(vertices)):
                if abs(lon - vertices[v]["lon"]) < 0.01 and abs(lat - vertices[v]["lat"]) < 0.01:
                    vertexList.append(v)
                    break
            else:
                vertexList.append(len(vertices))
                vertices.append({"lon": lon, "lat": lat})
        provinces[pid] = {"name": name, "id": pid, "vertices": vertexList}
    vertices = { v : vertices[v] for v in range(len(vertices)) }

outdict = {"vertices": vertices, "provinces": provinces}

with open("parsedMap.json", "w") as writeFile:
    writeFile.write(json.dumps(outdict, indent=4))

