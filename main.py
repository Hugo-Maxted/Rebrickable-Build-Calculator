import rebrick
import json

rebrick.init("7a034c160c02ba197f95bf916b613e80")

bld = json.loads(rebrick.lego.get_set(int(input("Set to build: "))).read())
print(f"Building: {bld['name']} ({bld['set_num'][:-2]})")

print("\nSets to use:")
sets = []
set = input("Set: ")
while set:
  sets.append(json.loads(rebrick.lego.get_set(int(set)).read()))
  print(f"Added: {sets[-1]['name']} ({sets[-1]['set_num'][:-2]})")
  set = input("Set: ")

print(
    f"\nUsing {len(sets)} set(s) with {sum([i['num_parts'] for i in sets])} parts")
print("\nCalculating...")

mparts = {}
for i in json.loads(
  rebrick.lego.get_set_elements(int(bld['set_num'][:-2])).read())["results"]:
  if not i["is_spare"]:
      mparts[i["part"]["part_num"]] = i["quantity"]

sparts = []
for i in sets:
  temp = {}
  for i in json.loads(
    rebrick.lego.get_set_elements(int(i['set_num'][:-2])).read())["results"]:
    if not i["is_spare"]:
      temp[i["part"]["part_num"]] = i["quantity"]
  sparts.append(temp)
