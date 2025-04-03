from random import choices
import pandas as pd

population = [0, 1]
weights = []

winrate = float(input("give winrate as decimal"))
start_balance = float(input("give starting balance"))
initial_risk = float(input("give initial risk"))
hops = int(input("how many wins until reset?"))
multiplier = float(input("give risk percentage multiplier after winning trade"))
n_cycles = int(input("how many test cycles?"))
n_trades = int(input("how many trades per test cycle?"))
csv_name = input("name for result csv?")

lossrate = 1 - winrate
weights.append(lossrate)
weights.append(winrate)

data_results= {
    "end_balance" : [],
    "max_drawdown" : [],
    "chicken_dinners" : [],
    "max_loss_streak" : [],
    "wins" : [],
    "losses" : []
}

result_csv = pd.DataFrame(data=data_results)

increment = 0

while n_cycles > 0:
    
    n_cycles -= 1
    
    trades = choices(population, weights, k=n_trades)
    
    balance = start_balance
    win_streak = 0
    loss_streak = 0
    current_risk = initial_risk
    
    chicken_dinners = 0
    
    max_loss_streak = 0
    max_drawdown = 0
    
    increment += 1
    filename = "tradescsv" + str(increment) + ".csv"
    
    data_trades= {
        "balance" : [],
        "result" : [],
        "next_risk" : [],
        "win_amount" : [],
        "loss_amount" : [],
        "chicken_dinners" : [],
        "max_drawdown" : [], 
        "win_streak" : [],
        "loss_streak" : [],
    }
    
    trades_csv = pd.DataFrame(data=data_trades)
    
    for trade in trades:
        
        if trade == 0:
            loss_amount = current_risk * balance
            balance = balance - loss_amount
            
            if balance < start_balance:
                drawdown = abs(start_balance - balance) 
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
                    
            #resets
            current_risk = initial_risk
            win_streak = 0
            loss_streak += 1
            if loss_streak > max_loss_streak:
                max_loss_streak = loss_streak
                
            loss_trade = [balance, "loss", initial_risk, 0, loss_amount, chicken_dinners, max_drawdown, 0, loss_streak]
            trades_csv.loc[len(trades_csv)] = loss_trade
        
        elif trade == 1:
            win_streak += 1
            loss_streak = 0
            win_amount = current_risk * balance
            balance = balance + win_amount
            if win_streak == hops:
                current_risk = initial_risk
                chicken_dinners += 1
                win_streak = 0
            elif win_streak > 1:
                current_risk = current_risk * multiplier
            
            win_trade = [balance, "win", current_risk, win_amount, 0, chicken_dinners, max_drawdown, win_streak, 0]
            trades_csv.loc[len(trades_csv)] = win_trade
            
    trades_csv.to_csv(filename)
    
        