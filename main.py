import rebrick
import json

rebrick.init("7a034c160c02ba197f95bf916b613e80")

set = json.loads(rebrick.lego.get_set(input("Set to build: ")).read())
print(f"Building: {set['name']} ({set['set_num'][:-2]})")

print("\nSets to use:")
sets = []
i = input("Set: ")
while i:
  sets.append(json.loads(rebrick.lego.get_set(i).read()))
  print(f"Added: {sets[-1]['name']} ({sets[-1]['set_num'][:-2]})")
  i = input("Set: ")

print(f"\nUsing {len(sets)} set(s) to build {set['name']} ({set['set_num'][:-2]})")
print("\nCalculating...")

set["parts"] = {}
for i in json.loads(rebrick.lego.get_set_elements(set["set_num"], color_details=False, page_size=10000).read())["results"]:
  if not i["is_spare"]:
    if i["part"]["part_num"] in set["parts"]:
      set["parts"][i["part"]["part_num"]] += i["quantity"]
    else:
      set["parts"][i["part"]["part_num"]] = i["quantity"]

for i in range(len(sets)):
  sets[i]["parts"] = {}
  for j in json.loads(rebrick.lego.get_set_elements(sets[i]["set_num"], color_details=False, page_size=10000).read())["results"]:
    if not j["is_spare"]:
      if j["part"]["part_num"] in sets[i]["parts"]:
        sets[i]["parts"][j["part"]["part_num"]] += j["quantity"]
      else:
        sets[i]["parts"][j["part"]["part_num"]] = j["quantity"]

parts = [{} for i in range(len(sets) + 1)]
for i in set["parts"]:
  for j in range(len(sets)):
    if i in sets[j]["parts"]:
      if sets[j]["parts"][i] >= set["parts"][i]:
        parts[j + 1][i] = sets[j]["parts"][i]
        set["parts"][i] = 0
        break
      else:
        parts[j + 1][i] = sets[j]["parts"][i]
        set["parts"][i] -= sets[j]["parts"][i]
    if set["parts"][i] > 0:
      parts[0][i] = set["parts"][i]

print(f"\nMissing parts ({sum([parts[0][i] for i in parts[0]])} total):")
[print(f"{i}: {parts[0][i]}") for i in parts[0]]
for i in range(0, len(sets)):
  print(f"\nParts in {sets[i]['name']} ({sets[i]['set_num'][:-2]}) ({sum([parts[i][j] for j in parts[i]])} total):")
  [print(f"{j}: {parts[i][j]}") for j in parts[i]]
