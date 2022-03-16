import webbrowser
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

images = {}
set["parts"] = {}
for i in json.loads(rebrick.lego.get_set_elements(set["set_num"], color_details=False, page_size=10000).read())["results"]:
  if not i["is_spare"]:
    if i["part"]["part_num"] in set["parts"]:
      set["parts"][i["part"]["part_num"]] += i["quantity"]
    else:
      set["parts"][i["part"]["part_num"]] = i["quantity"]
    images[i["part"]["part_num"]] = i["part"]["part_img_url"]

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
        parts[j + 1][i] = set["parts"][i]
        set["parts"][i] = 0
        break
      else:
        parts[j + 1][i] = sets[j]["parts"][i]
        set["parts"][i] -= sets[j]["parts"][i]
    if set["parts"][i] > 0 and j == len(sets) - 1:
      parts[0][i] = set["parts"][i]

report = open("results.html", "w")
report.write(f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results</title>
  </head>
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap");
    body {'''{
      font-family: "Roboto", sans-serif;
    }'''}
    .element {'''{
      display: inline-block;
      width: 10%;
      text-align: center;
    }'''}
    img {'''{
      width: 100%;
    }'''}
  </style>
  <body>
    <h3>Missing pieces:</h3>
    {"".join([f"<div class='element'><img src='{images[i]}' alt='{i}' /><br /><b>{parts[0][i]}x</b> {i}</div>" for i in sorted(parts[0], key=parts[0].get, reverse=True)])}
    <br />
    <br />
    {"".join([f'''<h3>Pieces from {sets[i]['name']} ({sets[i]['set_num'][:-2]}):</h3>
    {"".join([f"<div class='element'><img src='{images[j]}' alt='{j}' /><br /><b>{parts[i + 1][j]}x</b> {j}</div>" for j in sorted(parts[i + 1], key=parts[i + 1].get, reverse=True)])}
    <br />
    <br />''' for i in range(len(sets))])}
  </body>
</html>
""")
report.close()

print("\nComplete!")
print("Opening results in your browser...")
webbrowser.open("results.html")
