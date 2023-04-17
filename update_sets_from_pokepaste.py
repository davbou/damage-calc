from pokemon_formats import PokePaste
import json
import os 

def handle_set(json_dict):

    y1 = ["hp", "at", "df", "sa", "sd", "sp"]
    y2 = [str(a) for a in json_dict['evs'].values()]
    evDict = dict(zip(y1, y2))

    z = {
            "level": json_dict['Level'],
            "item":json_dict['item'],
            "ability":json_dict['ability'].strip(),
            "nature":json_dict['nature'], 
            "moves":[m.strip() for m in json_dict['moves']], 
            "evs":evDict
        }
    
    return(z)

with open("/Users/erikguterman/Documents/GitHub/dav-damage-calc/src/js/data/sets/raid_bosses.js") as js_file: 
    data = js_file.readline().removeprefix("var SETDEX_SV = ").removesuffix(";\n")

allSets = json.loads(data)

url = input("Pokepaste URL:")
set_type = input("How should the sets be titled?")

pokepaste_json = PokePaste.retrieve_pokepaste(url)

names = [name['species'] for name in pokepaste_json]
duplicates = list(set([name for name in names if names.count(name) > 1]))

for item in duplicates:
    dupes = list(filter(lambda mon: mon['species'] == item, pokepaste_json))
    for dupe in dupes:
        # print(Showdown.jsonToShowdown([dupe]))
        name = input("What should the title of this set be?")

        set_json = handle_set(dupe)
        species = dupe['species'].strip()

        if species in allSets.keys():
            if name in allSets[species].keys():
                overwriteCheck = input("Do you want to overwrite the existing set with this name? (Y) or (N)").lower()
                if overwriteCheck != "y":
                    print("not overwriting")
                    continue
            allSets[species][name] = set_json
            pokepaste_json.remove(dupe)
        else:
            allSets[species] = {name:set_json}
            pokepaste_json.remove(dupe)

for set in pokepaste_json:
        set_json = handle_set(set)
        species = set['species'].strip()

        if species in allSets.keys():
            if set_type in allSets[species].keys():
                overwriteCheck = input("Do you want to overwrite the existing set with this name? (Y) or (N)").lower()
                if overwriteCheck != "y":
                    print("not overwriting")
                    continue
            allSets[species][set_type] = set_json
        else:
            allSets[species] = {set_type:set_json}

try:
    os.remove("/Users/erikguterman/Documents/GitHub/dav-damage-calc/src/js/data/sets/raid_bosses_old.js")
except:
    pass

os.rename("/Users/erikguterman/Documents/GitHub/dav-damage-calc/src/js/data/sets/raid_bosses.js", "/Users/erikguterman/Documents/GitHub/dav-damage-calc/src/js/data/sets/raid_bosses_old.js")

with open('/Users/erikguterman/Documents/GitHub/dav-damage-calc/src/js/data/sets/raid_bosses.js', 'w') as out_file:
  out_file.write('var SETDEX_SV = %s;' % json.dumps(allSets))
