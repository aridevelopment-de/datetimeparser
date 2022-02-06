<br />
<div align="center">
  <h1 align="center">datetimeparser</h1>

  <p align="center">
    A python parser library made for parsing english language into datetime objects
    <br />
    <br />
    <a href="https://github.com/aridevelopment-de/datetimeparser/issues">Report an issue</a>
    Â·
    <a href="https://github.com/aridevelopment-de/datetimeparser/issues">Request a new feature</a>
  </p>
</div>


## About The Project

Datetimeparser is a python library capable of parsing the english language into datetime objects.  
It was created due to the lack of such library and need for it. We knew that there was [dateutil](https://github.com/dateutil/dateutil/) but we wanted a more powerful parsing library.  
Datetimeparser can even parse complex grammar and sentence structure.

## Examples

Below you can find some examples of how datetimeparser can be used.  
The resulting value from the parser is a datetime object, integer or None, depending on the outcome:
- "Infinity" leads to -1
- A wrong input date leads to None

```python
from datetimeparser import parse

print(parse("next 3 years and 2 months"))
# 2025-04-06 11:43:28

print(parse("begin of advent of code 2022"))
# 2022-12-01 06:00:00

print(parse("in 1 Year 2 months 3 weeks 4 days 5 hours 6 minutes 7 seconds"))
# 2023-05-01 17:59:52

print(parse("10 days and 2 hours after 3 months before christmas 2020"))
# 
```

## Installation

Use pip to install the library:
```shell
$ pip install datetimeparser
```

## List of Constants

<details>
<summary>List of Constants</summary>
<details>
<summary><code>christmas</code></summary>
<ul>
<li>next christmas</li>
<li>xmas</li>
<li>next xmas</li>
</ul>
</details><details>
<summary><code>silvester</code></summary>
<ul>
<li>next silvester</li>
<li>new years eve</li>
<li>next new years eve</li>
</ul>
</details><details>
<summary><code>eastern</code></summary>
<ul>
<li>next eastern</li>
<li>easter</li>
<li>next easter</li>
</ul>
</details><details>
<summary><code>nicholas</code></summary>
<ul>
<li>next nicholas</li>
<li>nicholas day</li>
<li>next nicholas day</li>
</ul>
</details><details>
<summary><code>halloween</code></summary>
<ul>
<li>next halloween</li>
</ul>
</details><details>
<summary><code>april fools day</code></summary>
<ul>
<li>next april fools day</li>
<li>april fool day</li>
<li>next april fool day</li>
</ul>
</details><details>
<summary><code>thanksgiving</code></summary>
<ul>
<li>next thanksgiving</li>
</ul>
</details><details>
<summary><code>saint patrick's day</code></summary>
<ul>
<li>next saint patrick's day</li>
<li>saint patricks day</li>
<li>next saint patricks day</li>
<li>st. patrick's day</li>
<li>next st. patrick's day</li>
<li>saint st. day</li>
<li>next st. patricks day</li>
<li>st patrick's day</li>
<li>next st patrick's day</li>
<li>st patricks day</li>
<li>next st patricks day</li>
</ul>
</details><details>
<summary><code>valentines day</code></summary>
<ul>
<li>next valentines day</li>
<li>valentine</li>
<li>next valentine</li>
<li>valentine day</li>
<li>next valentine day</li>
</ul>
</details><details>
<summary><code>summer end</code></summary>
<ul>
<li>end of summer</li>
<li>end of the summer</li>
</ul>
</details><details>
<summary><code>winter end</code></summary>
<ul>
<li>end of winter</li>
<li>end of the winter</li>
</ul>
</details><details>
<summary><code>spring end</code></summary>
<ul>
<li>end of spring</li>
<li>end of the spring</li>
</ul>
</details><details>
<summary><code>fall end</code></summary>
<ul>
<li>end of fall</li>
<li>end of the fall</li>
<li>autumn end</li>
<li>end of autumn</li>
<li>end of the autumn</li>
</ul>
</details><details>
<summary><code>summer begin</code></summary>
<ul>
<li>summer</li>
<li>next summer</li>
<li>begin of summer</li>
<li>begin of the summer</li>
</ul>
</details><details>
<summary><code>winter begin</code></summary>
<ul>
<li>winter</li>
<li>next winter</li>
<li>begin of winter</li>
<li>begin of the winter</li>
<li>winter is coming</li>
</ul>
</details><details>
<summary><code>spring begin</code></summary>
<ul>
<li>spring</li>
<li>next spring</li>
<li>begin of spring</li>
<li>begin of the spring</li>
</ul>
</details><details>
<summary><code>fall begin</code></summary>
<ul>
<li>fall</li>
<li>begin of fall</li>
<li>begin of the fall</li>
<li>autumn begin</li>
<li>autumn</li>
<li>begin of autumn</li>
<li>begin of the autumn</li>
</ul>
</details><details>
<summary><code>morning</code></summary>
<ul>
<li>at morning</li>
<li>in the next morning</li>
<li>next morning</li>
<li>in the morning</li>
</ul>
</details><details>
<summary><code>evening</code></summary>
<ul>
<li>at evening</li>
<li>in the next evening</li>
<li>next evening</li>
<li>in the evening</li>
</ul>
</details><details>
<summary><code>lunchtime</code></summary>
<ul>
<li>at lunch</li>
<li>at lunchtime</li>
<li>next lunch</li>
<li>at the next lunchtime</li>
<li>next lunchtime</li>
<li>at the lunchtime</li>
</ul>
</details><details>
<summary><code>aoc begin</code></summary>
<ul>
<li>aoc</li>
<li>next aoc</li>
<li>begin of aoc</li>
<li>begin of the aoc</li>
<li>advent of code begin</li>
<li>advent of code</li>
<li>next advent of code</li>
<li>begin of advent of code</li>
<li>begin of the advent of code</li>
</ul>
</details><details>
<summary><code>aoc end</code></summary>
<ul>
<li>end of aoc</li>
<li>end of the aoc</li>
<li>advent of code end</li>
<li>end of advent of code</li>
<li>end of the advent of code</li>
</ul>
</details><details>
<summary><code>end of year</code></summary>
<ul>
<li>the end of year</li>
<li>the end of the year</li>
<li>end of the year</li>
</ul>
</details><details>
<summary><code>infinity</code></summary>
<ul>
<li>inf</li>
<li>NekoFanatic</li>
</ul>
</details>
</details>