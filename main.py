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

print(f"\nUsing {len(sets)} set(s) with {sum([i['num_parts'] for i in sets])} parts")
print("\nCalculating...")

mparts = {}
for i in json.loads(rebrick.lego.get_set_elements(int(bld["set_num"][:-2]), color_details=False, page_size=10000).read())["results"]:
  if not i["is_spare"]:
    if i["part"]["part_num"] in mparts:
      mparts[i["part"]["part_num"]] += i["quantity"]
    else:
      mparts[i["part"]["part_num"]] = i["quantity"]

sparts = []
for i in sets:
  temp = {}
  for i in json.loads(rebrick.lego.get_set_elements(int(i["set_num"][:-2]), color_details=False, page_size=10000).read())["results"]:
    if not i["is_spare"]:
      if i["part"]["part_num"] in temp:
        temp[i["part"]["part_num"]] += i["quantity"]
      else:
        temp[i["part"]["part_num"]] = i["quantity"]
  sparts.append(temp)

fparts = [{} for i in range(len(sets) + 1)]
for i in mparts:
  for j in range(0, len(sets)):
    if i in sparts[j]:
      if sparts[j][i] >= mparts[i]:
        fparts[j + 1][i] = sparts[j][i]
        mparts[i] = 0
        break
      else:
        fparts[j + 1][i] = sparts[j][i]
        mparts[i] -= sparts[j][i]
    if mparts[i] > 0:
      fparts[0][i] = mparts[i]

print("\nMissing parts:")
[print(f"{i}: {fparts[0][i]}") for i in fparts[0]]
for i in range(0, len(sets)):
  print(f"\nParts in {sets[i]['name']} ({sets[i]['set_num'][:-2]})")
  [print(f"{j}: {fparts[i][j]}") for j in fparts[i]]
