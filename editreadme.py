from datetimeparser.baseclasses import Constants

HEADER = "## List of Constants"

with open("README.md", "r") as f:
    readme = f.read()

i = 0
for j, line in enumerate(readme.split("\n")):
    if line == HEADER:
        i = j
        break

readme = "\n".join(readme.split("\n")[:i]) + "\n" + HEADER

constants_string = ""

for constant in Constants.ALL:
    alias_string = '\n'.join(f"<li>{item}</li>" for item in constant.alias)

    constants_string += f"""<details>
<summary><code>{constant.name}</code></summary>
<ul>
{alias_string}
</ul>
</details>"""

readme = readme.replace(HEADER, f"""{HEADER}

<details>
<summary>List of Constants</summary>
{constants_string}
</details>""")


with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)