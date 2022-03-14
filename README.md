<br />
<div align="center">
  <h1 align="center">datetimeparser</h1>

  <p align="center">
    A python parser library made for parsing english language into datetime objects
    <br />
    <i> made with ❤️ by <a href="https://aridevelopment.de/">aridevelopment.de</a></i>
    <br />
    <br />
    <a href="https://github.com/aridevelopment-de/datetimeparser/issues">Report an issue</a>
    ·
    <a href="https://github.com/aridevelopment-de/datetimeparser/issues">Request a new feature</a>
  </p>
</div>


## About The Project

Datetimeparser is a python library capable of parsing the english language into datetime objects.  
It was created due to the lack of such library and need for it. We knew that there was [dateutil](https://github.com/dateutil/dateutil/) but we wanted a more powerful parsing library.  
Datetimeparser can even parse complex grammar and sentence structure.

## Latest Change

<!-- LATESTCOMMIT:START -->

[<img width="380px" height="200px" src="https://opengraph.githubassets.com/f190b6068f9654abdb7eedc4fa32c35b84c074c332fe3b81b5b54e0b5d7847ba/aridevelopment-de/datetimeparser/commit/c0f7b2bd845b24a2ba570ecb06636752a8d69f8b" />][commitUrl]

[commitUrl]: https://github.com/aridevelopment-de/datetimeparser/commit/c0f7b2bd845b24a2ba570ecb06636752a8d69f8b
<!-- LATESTCOMMIT:END -->

## Examples

Below you can find some examples of how datetimeparser can be used.

```python
from datetimeparser import parse

print(parse("next 3 years and 2 months"))
# 2025-04-06 11:43:28

print(parse("begin of advent of code 2022"))
# 2022-12-01 06:00:00

print(parse("in 1 Year 2 months 3 weeks 4 days 5 hours 6 minutes 7 seconds"))
# 2023-05-01 17:59:52

print(parse("10 days and 2 hours after 3 months before christmas 2020"))
# 2020-10-05 02:00:00
```

## Installation

Use pip to install the library:
```shell
$ pip install python-datetimeparser
```

## Contributing

If you want to contribute to datetimeparser, please use feature branches. If possible, name them after an already opened issue (e.g. feature/131).  
We highly appreciate everyone who wants to help our project!

## List of Constants

<details>
<summary>All Normal-Constants</summary>
<details>
<summary><code>christmas</code></summary>
<ul>
<li>xmas</li>
</ul>
</details><details>
<summary><code>silvester</code></summary>
<ul>
<li>new years eve</li>
</ul>
</details><details>
<summary><code>eastern</code></summary>
<ul>
<li>easter</li>
</ul>
</details><details>
<summary><code>nicholas</code></summary>
<ul>
<li>nicholas day</li>
</ul>
</details><details>
<summary><code>halloween</code></summary>
<ul>

</ul>
</details><details>
<summary><code>april fools day</code></summary>
<ul>
<li>april fool day</li>
</ul>
</details><details>
<summary><code>thanksgiving</code></summary>
<ul>

</ul>
</details><details>
<summary><code>saint patrick's day</code></summary>
<ul>
<li>saint patricks day</li>
<li>st. patrick's day</li>
<li>saint pt. day</li>
<li>st patrick's day</li>
<li>st patricks day</li>
</ul>
</details><details>
<summary><code>valentines day</code></summary>
<ul>
<li>valentine</li>
<li>valentine day</li>
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
<li>begin of summer</li>
<li>begin of the summer</li>
</ul>
</details><details>
<summary><code>winter begin</code></summary>
<ul>
<li>winter</li>
<li>begin of winter</li>
<li>begin of the winter</li>
</ul>
</details><details>
<summary><code>spring begin</code></summary>
<ul>
<li>spring</li>
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
</ul>
</details><details>
<summary><code>evening</code></summary>
<ul>
<li>at evening</li>
</ul>
</details><details>
<summary><code>lunchtime</code></summary>
<ul>
<li>lunch</li>
</ul>
</details><details>
<summary><code>aoc begin</code></summary>
<ul>
<li>aoc</li>
<li>begin of aoc</li>
<li>begin of the aoc</li>
<li>advent of code begin</li>
<li>advent of code</li>
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
<summary><code>begin of year</code></summary>
<ul>
<li>the begin of year</li>
<li>the begin of the year</li>
<li>begin of the year</li>
</ul>
</details><details>
<summary><code>infinity</code></summary>
<ul>
<li>inf</li>
</ul>
</details><details>
<summary><code>today</code></summary>
<ul>

</ul>
</details><details>
<summary><code>tomorrow</code></summary>
<ul>

</ul>
</details><details>
<summary><code>yesterday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>now</code></summary>
<ul>
<li>at the moment</li>
<li>current time</li>
<li>current time now</li>
</ul>
</details>
</details>
<br />

<details>
<summary>All Day-Constants</summary>
<details>
<summary><code>morning</code></summary>
<ul>

</ul>
</details><details>
<summary><code>afternoon</code></summary>
<ul>

</ul>
</details><details>
<summary><code>evening</code></summary>
<ul>

</ul>
</details><details>
<summary><code>night</code></summary>
<ul>

</ul>
</details><details>
<summary><code>morning night</code></summary>
<ul>

</ul>
</details><details>
<summary><code>daylight change</code></summary>
<ul>
<li>daylight saving</li>
<li>daylight saving time</li>
</ul>
</details><details>
<summary><code>midnight</code></summary>
<ul>

</ul>
</details><details>
<summary><code>midday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>dawn</code></summary>
<ul>

</ul>
</details><details>
<summary><code>dusk</code></summary>
<ul>

</ul>
</details><details>
<summary><code>sunrise</code></summary>
<ul>

</ul>
</details><details>
<summary><code>sunset</code></summary>
<ul>

</ul>
</details><details>
<summary><code>lunch</code></summary>
<ul>
<li>lunchtime</li>
</ul>
</details><details>
<summary><code>dinner</code></summary>
<ul>
<li>dinnertime</li>
</ul>
</details><details>
<summary><code>breakfast</code></summary>
<ul>

</ul>
</details>
</details>
<br />

<details>
<summary>All Weekday-Constants</summary>
<details>
<summary><code>monday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>tuesday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>wednesday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>thursday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>friday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>saturday</code></summary>
<ul>

</ul>
</details><details>
<summary><code>sunday</code></summary>
<ul>

</ul>
</details>
</details>
<br />

<details>
<summary>All Month-Constants</summary>
<details>
<summary><code>january</code></summary>
<ul>
<li>jan</li>
</ul>
</details><details>
<summary><code>february</code></summary>
<ul>
<li>feb</li>
</ul>
</details><details>
<summary><code>march</code></summary>
<ul>
<li>mar</li>
</ul>
</details><details>
<summary><code>april</code></summary>
<ul>
<li>apr</li>
</ul>
</details><details>
<summary><code>may</code></summary>
<ul>

</ul>
</details><details>
<summary><code>june</code></summary>
<ul>
<li>jun</li>
</ul>
</details><details>
<summary><code>july</code></summary>
<ul>
<li>jul</li>
</ul>
</details><details>
<summary><code>august</code></summary>
<ul>
<li>aug</li>
</ul>
</details><details>
<summary><code>september</code></summary>
<ul>
<li>sep</li>
</ul>
</details><details>
<summary><code>october</code></summary>
<ul>
<li>oct</li>
</ul>
</details><details>
<summary><code>november</code></summary>
<ul>
<li>nov</li>
</ul>
</details><details>
<summary><code>december</code></summary>
<ul>
<li>dec</li>
</ul>
</details>
</details>
<br />

<details>
<summary>All Datetime-Constants</summary>
<details>
<summary><code>seconds</code></summary>
<ul>
<li>second</li>
<li>sec</li>
<li>secs</li>
</ul>
</details><details>
<summary><code>minutes</code></summary>
<ul>
<li>minute</li>
<li>min</li>
<li>mins</li>
</ul>
</details><details>
<summary><code>hours</code></summary>
<ul>
<li>hour</li>
</ul>
</details><details>
<summary><code>days</code></summary>
<ul>
<li>day</li>
</ul>
</details><details>
<summary><code>weeks</code></summary>
<ul>
<li>week</li>
</ul>
</details><details>
<summary><code>months</code></summary>
<ul>
<li>month</li>
</ul>
</details><details>
<summary><code>years</code></summary>
<ul>
<li>year</li>
</ul>
</details>
</details>
<br />

<details>
<summary>All Number-Constants</summary>
<details>
<summary><code>thirty one</code></summary>
<ul>
<li>thirtyone</li>
<li>thirty-one</li>
</ul>
</details><details>
<summary><code>thirty</code></summary>
<ul>

</ul>
</details><details>
<summary><code>twenty nine</code></summary>
<ul>
<li>twentynine</li>
<li>twenty-nine</li>
</ul>
</details><details>
<summary><code>twenty eight</code></summary>
<ul>
<li>twentyeight</li>
<li>twenty-eight</li>
</ul>
</details><details>
<summary><code>twenty seven</code></summary>
<ul>
<li>twentyseven</li>
<li>twenty-seven</li>
</ul>
</details><details>
<summary><code>twenty six</code></summary>
<ul>
<li>twentysix</li>
<li>twenty-six</li>
</ul>
</details><details>
<summary><code>twenty five</code></summary>
<ul>
<li>twentyfive</li>
<li>twenty-five</li>
</ul>
</details><details>
<summary><code>twenty four</code></summary>
<ul>
<li>twentyfour</li>
<li>twenty-four</li>
</ul>
</details><details>
<summary><code>twenty three</code></summary>
<ul>
<li>twentythree</li>
<li>twenty-three</li>
</ul>
</details><details>
<summary><code>twenty two</code></summary>
<ul>
<li>twentytwo</li>
<li>twenty-two</li>
</ul>
</details><details>
<summary><code>twenty one</code></summary>
<ul>
<li>twentyone</li>
<li>twenty-one</li>
</ul>
</details><details>
<summary><code>twenty</code></summary>
<ul>

</ul>
</details><details>
<summary><code>nineteen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>eighteen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>seventeen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>sixteen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>fifteen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>fourteen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>thirteen</code></summary>
<ul>

</ul>
</details><details>
<summary><code>twelve</code></summary>
<ul>

</ul>
</details><details>
<summary><code>eleven</code></summary>
<ul>

</ul>
</details><details>
<summary><code>ten</code></summary>
<ul>

</ul>
</details><details>
<summary><code>nine</code></summary>
<ul>

</ul>
</details><details>
<summary><code>eight</code></summary>
<ul>

</ul>
</details><details>
<summary><code>seven</code></summary>
<ul>

</ul>
</details><details>
<summary><code>six</code></summary>
<ul>

</ul>
</details><details>
<summary><code>five</code></summary>
<ul>

</ul>
</details><details>
<summary><code>four</code></summary>
<ul>

</ul>
</details><details>
<summary><code>three</code></summary>
<ul>

</ul>
</details><details>
<summary><code>two</code></summary>
<ul>

</ul>
</details><details>
<summary><code>one</code></summary>
<ul>

</ul>
</details>
</details>
<br />

<details>
<summary>All NumberCount-Constants</summary>
<details>
<summary><code>thirty first</code></summary>
<ul>
<li>31st</li>
<li>31.</li>
<li>thirthyfirst</li>
<li>thirty-first</li>
</ul>
</details><details>
<summary><code>thirtieth</code></summary>
<ul>
<li>30th</li>
<li>30.</li>
</ul>
</details><details>
<summary><code>twenty ninth</code></summary>
<ul>
<li>29th</li>
<li>29.</li>
<li>twentyninth</li>
<li>twenty-ninth</li>
</ul>
</details><details>
<summary><code>twenty eighth</code></summary>
<ul>
<li>28th</li>
<li>28.</li>
<li>twentyeighth</li>
<li>twenty-eighth</li>
</ul>
</details><details>
<summary><code>twenty seventh</code></summary>
<ul>
<li>27th</li>
<li>27.</li>
<li>twentyseventh</li>
<li>twenty-seventh</li>
</ul>
</details><details>
<summary><code>twenty sixth</code></summary>
<ul>
<li>26th</li>
<li>26.</li>
<li>twentysixth</li>
<li>twenty-sixth</li>
</ul>
</details><details>
<summary><code>twenty fifth</code></summary>
<ul>
<li>25th</li>
<li>25.</li>
<li>twentyfifth</li>
<li>twenty-fifth</li>
</ul>
</details><details>
<summary><code>twenty fourth</code></summary>
<ul>
<li>24th</li>
<li>24.</li>
<li>twentyfourth</li>
<li>twenty-fourth</li>
</ul>
</details><details>
<summary><code>twenty third</code></summary>
<ul>
<li>23rd</li>
<li>23.</li>
<li>twentythird</li>
<li>twenty-third</li>
</ul>
</details><details>
<summary><code>twenty second</code></summary>
<ul>
<li>22nd</li>
<li>22.</li>
<li>twentysecond</li>
<li>twenty-second</li>
</ul>
</details><details>
<summary><code>twenty first</code></summary>
<ul>
<li>21st</li>
<li>21.</li>
<li>twentyfirst</li>
<li>twenty-first</li>
</ul>
</details><details>
<summary><code>twentieth</code></summary>
<ul>
<li>20th</li>
<li>20.</li>
</ul>
</details><details>
<summary><code>nineteenth</code></summary>
<ul>
<li>19th</li>
<li>19.</li>
</ul>
</details><details>
<summary><code>eighteenth</code></summary>
<ul>
<li>18th</li>
<li>18.</li>
</ul>
</details><details>
<summary><code>seventeenth</code></summary>
<ul>
<li>17th</li>
<li>17.</li>
</ul>
</details><details>
<summary><code>sixteenth</code></summary>
<ul>
<li>16th</li>
<li>16.</li>
</ul>
</details><details>
<summary><code>fifteenth</code></summary>
<ul>
<li>15th</li>
<li>15.</li>
</ul>
</details><details>
<summary><code>fourteenth</code></summary>
<ul>
<li>14th</li>
<li>14.</li>
</ul>
</details><details>
<summary><code>thirteenth</code></summary>
<ul>
<li>13th</li>
<li>13.</li>
</ul>
</details><details>
<summary><code>twelfth</code></summary>
<ul>
<li>12th</li>
<li>12.</li>
</ul>
</details><details>
<summary><code>eleventh</code></summary>
<ul>
<li>11th</li>
<li>11.</li>
</ul>
</details><details>
<summary><code>tenth</code></summary>
<ul>
<li>10th</li>
<li>10.</li>
</ul>
</details><details>
<summary><code>ninth</code></summary>
<ul>
<li>9th</li>
<li>9.</li>
</ul>
</details><details>
<summary><code>eighth</code></summary>
<ul>
<li>8th</li>
<li>8.</li>
</ul>
</details><details>
<summary><code>seventh</code></summary>
<ul>
<li>7th</li>
<li>7.</li>
</ul>
</details><details>
<summary><code>sixth</code></summary>
<ul>
<li>6th</li>
<li>6.</li>
</ul>
</details><details>
<summary><code>fifth</code></summary>
<ul>
<li>5th</li>
<li>5.</li>
</ul>
</details><details>
<summary><code>fourth</code></summary>
<ul>
<li>4th</li>
<li>4.</li>
</ul>
</details><details>
<summary><code>third</code></summary>
<ul>
<li>3rd</li>
<li>3.</li>
</ul>
</details><details>
<summary><code>second</code></summary>
<ul>
<li>2nd</li>
<li>2.</li>
</ul>
</details><details>
<summary><code>first</code></summary>
<ul>
<li>1st</li>
<li>1.</li>
</ul>
</details>
</details>
<br />
