# Anti-Martingale-Simulator

With this simulator you can test your trading system's risk parameters with arbitary number of randomly generated trades and test cycles. The result statistics of test cycles are aggregated into a csv file. The user has the option to output the list of trades in test cycles into csv files.

The simulator comes with analytics tool to gain deeper insight of your trading system's risk parameters.

The simulator is specifically designed to test the risk parameters of anti-martingale systems but regular risk management systems without compounding can also be tested.

### Some common terms that you will encounter using the simulator:

<strong>hops</strong>: how many wins in a row until compounding ends and the risk percentage is set to default.

<strong>chicken dinner</strong>: when predetermined winstreak (hops) is reached, the compounded sum of profit is collected to the balance and the risk percentage for upcoming trades is set to default.

<strong>runner up</strong> (hops-1): when the winstreak ends right before chicken dinner is achieved.
