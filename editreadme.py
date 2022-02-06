from datetimeparser.baseclasses import Constants

with open("README-TEMPLATE.md", "r") as f:
    readme = f.read()

constants_string = ""

for constant in Constants.ALL:
    alias_string = '\n'.join(f"<li>{item}</li>" for item in constant.alias)

    constants_string += f"""<li>
    <details>
    <summary>``{constant.name}``</summary>
    <ul>
    {alias_string}
    </ul>
    </details>
    </li>"""

readme += f"""<details>
<summary>List of Constants</summary>
<ul style="list-style-type: none">
{constants_string}
</ul>
</details>"""

with open("README.md", "w") as f:
    f.write(readme)