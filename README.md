# iStock by Unicorn
 
### Roster: 
- PM: Ivan Chen
- dev1: Emaan Asif
- dev2: Jake Liu
- dev3: Jalen Chen

### Description:
iStock provides users with an interactive visualization of the development of different securities over time. It offers a dynamic bar chart race feature through which users select stocks for a fun way to see which stock will win at the end of the chosen timeframe. It also offers a simple comparison feature to give the user a breakdown, including Open, High, Low, Close, and Volume (OHLCV) data, of selected stocks.

#### Visit our live site at [45.55.142.125](http://45.55.142.125)

### FEATURE SPOTLIGHT
* Interact our [Bar Chart](http://45.55.142.125/barChart), where your can adjust the stock symbols and time period to compare and view their market caps. The chart scales as it runs over the chosen interval.

### KNOWN BUGS/ISSUES
* Our Bar Chart runs in intervals of three, so if you chose a time period not divisible by three, it will stop a bit earlier. i.e., If your start date is 01/01/2023 and end date is 01/01/2024, a span of eleven months, it will stop nine months after the start date, in Oct 2023 (labeled at the bottom right of the chart) 

### Install Guide:
1. Clone the repository:
`git clone git@github.com:starstrime/p4_unicorn.git`
2. Navigate into directory: `cd p4_unicorn`
3. Create virtual environment: `python3 -m venv venv`
4. Activate virutal environment:
* macOS/Linux: `. venv/bin/activate`
* Windows: `venv/Scripts/activate`
5. Install dependencies:
`pip install -r requirements.txt`

### Launch Codes:
To serve the app locally, navigate into the `p4_unicorn` directory and run:
* `cd app`
* `python3 __init__.py`

To serve the app remotely, navigate to our live site [45.55.142.125](http://45.55.142.125)

