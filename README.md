# Anti-Martingale-Simulator

With this simulator you can test your trading system's risk parameters with arbitary number of randomly generated trades and test cycles. The result statistics of test cycles are aggregated into a csv-file. The user has the option to output the list of trades from test cycles into csv-files.

The simulator comes with data analytics tools to help you gain deeper insight of your trading system's risk parameters. The program generates a simple HTML analysis report but you can use the analysis.ipynb notebook for more indepth analysis. Use this link to see the analysis.ipynb notebook with outputs:

https://nbviewer.org/github/Niittyv/Anti-Martingale-Simulator/blob/main/analysis.ipynb

The simulator is specifically designed to test the risk parameters of anti-martingale systems but regular risk management systems without compounding can also be tested.

### Some common terms that you will encounter using the simulator:

<strong>hops</strong>: how many wins in a row until compounding ends and the risk percentage is set to default.

<strong>chicken dinner / bankrun</strong>: when predetermined winstreak (hops) is reached, the compounded sum of profit is collected to the balance and the risk percentage for upcoming trades is set to default.

<strong>runner up</strong> (hops-1): when the winstreak ends right before chicken dinner is achieved.

### Example configuration

Run the following command on cmd:
```
Python main.py
```

enable anti-martingale? (y/n) - y
- if enabled, the risk will be compounded after each successive winning trade. If disabled, the risk will stay constant.

give winrate (eg. 50 for 50%) - 50
- value 50 means that the test cycles will average to 50% winrate.
  
give starting balance - 10000
- account balance in the start of a test cycle.

give initial risk percentage (eg. 10 for 10%) - 1
- risk percentage before compounding takes effect.
  
how many wins until reset? - 3
- keeps compounding after each successive win until winstreak of 3 is reached, after which risk percentage is reset.

how many wins to skip before compounding takes effect? (leave blank for no skips) - 1
- starts compounding only after second win in a streak

give risk multiplier after winning trade - 2
- multiplies the current pot by 2 after every consecutive win until chicken dinner is reached
  
how many test cycles? - 10000
- runs the simulated trading cycle 10000 times and aggregates the statistics into a csv-file

how many trades per test cycle? - 100
- simulates the results 100 trades for every test cycle
  
enable gathering of individual test cycles as csv-files? (y/n) - n
- if enabled, simulated trades for each test cycle will be written into csv-files. <strong>Be careful, if the number of test cycles is really high and this option is enabled, there will be a csv-file saved in your filesystem for each test cycle.</strong>

name for test cycle csv-files? (leave blank for 'test_cycle#.csv -
- leave blank for default naming
  
name for result csv? (leave blank for 'results.csv') -
- leave blank for default naming

want to generate html-report? (y/n) - y
- generates an analysis report of result.csv in a HTML-file format
