from datetimeparser.utils.enums import (
    Constants,
    MonthConstants,
    WeekdayConstants,
    DatetimeConstants,
    NumberCountConstants,
    NumberConstants,
    DatetimeDeltaConstants
)


HEADER = "## List of Constants"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

i = 0
for j, line in enumerate(readme.split("\n")):
    if line == HEADER:
        i = j
        break

readme = "\n".join(readme.split("\n")[:i]) + "\n" + HEADER


def get_constant_list(headline, constant_list):
    constants_string = ""

    for constant in constant_list:
        alias_string = '\n'.join(f"<li>{item}</li>" for item in constant.alias)

        constants_string += f"""<details>
<summary><code>{constant.name}</code></summary>
<ul>
{alias_string}
</ul>
</details>"""

    return f"""
<details>
<summary>{headline}</summary>
{constants_string}
</details>"""


resulting_string = ""
resulting_string += get_constant_list("All Normal-Constants", Constants.ALL) + "\n<br />\n"
resulting_string += get_constant_list("All Day-Constants", DatetimeDeltaConstants.ALL) + "\n<br />\n"
resulting_string += get_constant_list("All Weekday-Constants", WeekdayConstants.ALL) + "\n<br />\n"
resulting_string += get_constant_list("All Month-Constants", MonthConstants.ALL) + "\n<br />\n"
resulting_string += get_constant_list("All Datetime-Constants", DatetimeConstants.ALL) + "\n<br />\n"
resulting_string += get_constant_list("All Number-Constants", NumberConstants.ALL) + "\n<br />\n"
resulting_string += get_constant_list("All NumberCount-Constants", NumberCountConstants.ALL) + "\n<br />\n"

readme = readme.replace(HEADER, f"{HEADER}\n{resulting_string}")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
