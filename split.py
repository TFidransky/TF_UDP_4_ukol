import json
import quadtree

# třída pro řešení pokud je vstupní soubor prázdný. Nechci užívat Pandas
class EmptyFileException(Exception):
    def __init__(self, message):
        self.message = message

class Feature:
    # inicializace do třídy několik proměnných
    def __init__(self, feature, x_coord, y_coord):
        self.feature = feature
        self.x_coord = x_coord
        self.y_coord = y_coord

    # vrací string se souřadnicemi (inicializovanými v inicializátoru)
    def __str__(self):
        return "Coord: " + str(self.x_coord) + ", " + str(self.y_coord) + "\n"

# Otevírá GeoJSON, pokud je vstupní soubor ve špatném formátu, je prázdný nebo neexistuje na správné pozici, tak program vyhodí adekvátní error kód a ukončí program
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

# Převádí data GeoJSON souboru na seznam objektů features. Funkce přijímá jako vstupní proměnnou "data" (soubor už zkontrolovaný pro správný vstup)
# Poté vrací seznam objektů "features"
def parse_to_features(data):
    features = []
    for feature in data["features"]:
        features.append(Feature(feature, feature["geometry"]["coordinates"][0], feature["geometry"]["coordinates"][1]))

    return features

# Funkce zapisující data do nového souboru "output.geojson" Přijímá dva vstupní parametry (seznam objektů "features" a objekt geojson souboru "data")
def write_to_file(features, data):
    out_file = open("output.geojson", "w", encoding="utf-8-sig")
    json_features = []
    for f in features:
        json_features.append(f.feature)
    data["features"] = json_features
    json.dump(data, out_file, ensure_ascii=False, indent=4)

# Funkce, která obsahuje hlavní průběh programu. V základu otevírá program se souborem specificky pojmenovaným "input.geojson", takže buď lze změnit tady, 
# případně program je možné upravit tento program tak, aby se ptal uživatele na název souboru.
# Po otevření souboru převádí data na seznam "features", vytváří quadtree a zapisuje data do souboru
def main():
    data = open_geojson("input.geojson")
    features = parse_to_features(data)
    result = []
    qt = quadtree.QuadTree(quadtree.Point(-90, 90), quadtree.Point(90, 90), quadtree.Point(-90, -90),
                           quadtree.Point(90, -90), result)
    for f in features:
        qt.insert(f)
    qt.divide()
    write_to_file(result, data)

main()
