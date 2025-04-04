from random import choices
import pandas as pd

enable_anti_martingale = False
enable_trades_csv = False

population = [0, 1]
weights = []

anti_martingale = input("enable anti-martingale? (y/n) " )

if anti_martingale.lower() == "y":
    enable_anti_martingale = True
    
winrate = float(input("give winrate as decimal "))
start_balance = float(input("give starting balance "))
initial_risk = float(input("give initial risk "))

if enable_anti_martingale:
    hops = int(input("how many wins until reset? "))
    to_skip = int(input("how many wins to skip before compounding takes effect? "))
    multiplier = float(input("give risk multiplier after winning trade "))

n_cycles = int(input("how many test cycles? "))
n_trades = int(input("how many trades per test cycle? "))
trades_csv = input("enable gathering of individual test cycles as csv-files? (y/n) ")

if trades_csv.lower() == "y":
    enable_trades_csv = True
    trades_csv_name = input("name for test cycle csv-files? ")

result_csv_name = input("name for result csv? ")

lossrate = 1 - winrate
weights.append(lossrate)
weights.append(winrate)

data_results= {
    "end_balance" : [],
    "max_drawdown" : [],
    "chicken_dinners/max_win_streak" : [],
    "max_loss_streak" : [],
    "wins" : [],
    "losses" : [],
    "winrate" : []
}

result_csv = pd.DataFrame(data=data_results)

if enable_trades_csv:
    increment = 0

while n_cycles > 0:
    
    n_cycles -= 1
    
    trades = choices(population, weights, k=n_trades)
    
    balance = start_balance
    pot = balance * initial_risk
    win_streak = 0
    loss_streak = 0
    
    chicken_dinners = 0
    
    max_loss_streak = 0
    max_drawdown = 0
    
    wins = 0
    total_trades = 0
    
    if enable_trades_csv:
        
        increment += 1
        filename = trades_csv_name + str(increment) + ".csv"
    
        data_trades= {
            "balance" : [],
            "result" : [],
            "win_amount" : [],
            "loss_amount" : [],
            "max_drawdown" : [], 
            "winrate" : [],
            "chicken_dinners/win_streak" : [],
            "loss_streak" : []
        }
        
        trades_csv = pd.DataFrame(data=data_trades)
    
    for trade in trades:
        
        total_trades += 1
        
        if trade == 0:
            
            loss_amount = pot
            balance = balance - loss_amount
            
            if balance < start_balance:
                drawdown = abs(start_balance - balance) 
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
                    
            #resets
            if enable_anti_martingale:
                pot = balance * initial_risk
            win_streak = 0
            loss_streak += 1
            if loss_streak > max_loss_streak:
                max_loss_streak = loss_streak
            
            if enable_trades_csv:
                winrate = wins / total_trades
                winrate = winrate * 100
                loss_trade = [round(balance), "loss", 0, round(loss_amount), round(max_drawdown), round(winrate, 1), chicken_dinners, loss_streak]
                trades_csv.loc[len(trades_csv)] = loss_trade
                
            if balance <= 0:
                break
        
        elif trade == 1:
            
            wins += 1
            win_streak += 1
            loss_streak = 0
            win_amount = pot
            balance = balance + win_amount
            
            if enable_anti_martingale:
                if win_streak == hops:
                    pot = balance * initial_risk
                    chicken_dinners += 1
                    win_streak = 0
                elif win_streak > to_skip:
                    pot = pot * multiplier
            else:
                if win_streak > chicken_dinners:
                    chicken_dinners = win_streak
            
            if enable_trades_csv:
                winrate = wins / total_trades
                winrate = winrate * 100
                win_trade = [round(balance), "win", round(win_amount), 0, round(max_drawdown), round(winrate, 1), chicken_dinners, 0]
                trades_csv.loc[len(trades_csv)] = win_trade
    
    if enable_trades_csv:        
        trades_csv.to_csv(filename)
    
    losses = total_trades - wins
    
    winrate = wins / total_trades
    winrate = winrate * 100
    
    new_cycle = [round(balance), round(max_drawdown), chicken_dinners, max_loss_streak, wins, losses, round(winrate, 1)]
    result_csv.loc[len(result_csv)] = new_cycle

filename = result_csv_name + ".csv"
result_csv.to_csv(filename)