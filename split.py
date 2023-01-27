import json
import quadtree

class EmptyFileException(Exception):
    def __init__(self, message):
        self.message = message

class Feature:
    def __init__(self, feature, x_coord, y_coord):
        self.feature = feature
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __str__(self):
        return "Coord: " + str(self.x_coord) + ", " + str(self.y_coord) + "\n"

def open_geojson(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            if f.tell() == f.seek(0, 2):
                raise EmptyFileException(f"Vstupní soubor {filename} je prázdný.")
            f.seek(0)
            data = json.load(f)
    except FileNotFoundError:
        print(f"Vstupní soubor {filename} nebyl nalezen.")
        exit(1)
    except EmptyFileException:
        print(f"Vstupní soubor {filename} byl prázdný")
        exit(1)
    except json.JSONDecodeError:
        print(f"Nevhodný formát vstupního souboru {filename}.")
        exit(1)
    return data

def parseToFeatures(data):
    features = []
    for feature in data["features"]:
        features.append(Feature(feature, feature["geometry"]["coordinates"][0], feature["geometry"]["coordinates"][1]))

    return features

def writeToFile(features, data):
    out_file = open("output.geojson", "w", encoding="utf-8-sig")
    json_features = []
    for f in features:
        json_features.append(f.feature)
    data["features"] = json_features
    json.dump(data, out_file, ensure_ascii=False, indent=4)

def main():
    data = open_geojson("input.geojson")
    features = parseToFeatures(data)
    result = []
    qt = quadtree.QuadTree(quadtree.Point(-90, 90), quadtree.Point(90, 90), quadtree.Point(-90, -90),
                           quadtree.Point(90, -90), result)
    for f in features:
        qt.insert(f)
    qt.divide()
    writeToFile(result, data)

main()
