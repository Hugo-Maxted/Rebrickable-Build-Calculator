import rebrick
import json

rebrick.init("7a034c160c02ba197f95bf916b613e80")

building = json.loads(rebrick.lego.get_set(int(input("Set to build: "))).read())

print(f"Building: {building['name']} ({building['set_num']})")

print("\nSets to use:")
using = []
set = input("Set: ")
while set:
  using.append(json.loads(rebrick.lego.get_set(int(set)).read()))
  print(f"Added: {using[-1]['name']} ({using[-1]['set_num']})")
  set = input("Set: ")

print(f"\nUsing {len(using)} set(s) with {sum([i['num_parts'] for i in using])} parts")
