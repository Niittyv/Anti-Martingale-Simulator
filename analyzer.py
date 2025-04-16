import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import base64
from io import BytesIO

def generate_base64():

    # Save the plot to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Encode plot to base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()  # Close the plot to free memory
    
    return img_base64


def generate_report(df, metadata):

    mti = str(metadata[['anti_martingale', 
                    'winrate', 
                    'start_balance', 
                    'initial_risk', 
                    'hops',
                    'wins_to_skip',
                    'risk_multiplier',
                    'test_cycles',
                    'trades_per_cycle']].iloc[0])
    
    mti = mti.split("Name")[0].strip()

    #drop first column
    #df = df.drop(df.columns[0], axis=1)
     
    total_trades = metadata['trades_per_cycle'].iloc[0]
    mean_winrate = round(np.mean(df['winrate']), 1)

    # creating seperate dataframes for winning and losing trades
    df_profitable = df[df['pnl'] >= 0]
    df_losing = df[df['pnl'] < 0]

    df['expectancy'] = df['pnl'] / total_trades
    df['expectancy%'] = df['pnl%'] / total_trades
    mean_excpectancy = round(np.mean(df['expectancy']), 1)
    mean_excpectancy_percentage = round(np.mean(df['expectancy%']), 1)

    max_pnl = round(np.max(df['pnl%']), 1)
    min_pnl = round(np.min(df['pnl%']), 1)
    max_dd = round(np.max(df['max_drawdown%']), 1) * (-1)
    mean_pnl = round(np.mean(df['pnl%']), 1)
    median_pnl = round(np.median(df['pnl%']), 1)
    mean_max_dd = round(np.mean(df['max_drawdown%']), 1) * (-1)
    median_max_dd = round(np.median(df['max_drawdown%']), 1) * (-1)


    corr = df.corr()
    plt.figure(figsize=(11,8))
    sns.heatmap(corr, cmap="Greens", annot=True)
    
    html1 = generate_base64()
    
    # Creates subplots for chicken dinner distribution
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    # Plots Boxplot for Data 1
    axs[0].boxplot(df['chicken_dinners/max_win_streak'])
    axs[0].set_title('all chicken dinners')
    axs[0].set_xlabel('Sample')
    axs[0].set_ylabel('chicken dinners')
    # Plots Boxplot for Data 2
    axs[1].boxplot(df_profitable['chicken_dinners/max_win_streak'])
    axs[1].set_title('profitable cycle chicken dinners')
    axs[1].set_xlabel('Sample')
    axs[1].set_ylabel('chicken dinners')
    # Plots Boxplot for Data 3
    axs[2].boxplot(df_losing['chicken_dinners/max_win_streak'])
    axs[2].set_title('losing cycle chicken dinners')
    axs[2].set_xlabel('Sample')
    axs[2].set_ylabel('chicken dinners')
    # Adjusts layout
    plt.tight_layout()
    
    html2 = generate_base64()

    # Creates subplots for all data distribution
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    # Plots Boxplot for Data 1
    axs[0].boxplot(df['pnl%'])
    axs[0].set_title('pnl% distribution')
    axs[0].set_xlabel('Sample')
    axs[0].set_ylabel('pnl%')
    # Plots Boxplot for Data 2
    axs[1].boxplot(df['max_drawdown%'])
    axs[1].set_title('max drawdown % distribution')
    axs[1].set_xlabel('Sample')
    axs[1].set_ylabel('Max drawdown%')
    # Plots Boxplot for Data 3
    axs[2].boxplot(df['winrate'])
    axs[2].set_title('winrate % distribution')
    axs[2].set_xlabel('Sample')
    axs[2].set_ylabel('Winrate%')
    # Adjusts layout
    plt.tight_layout()
    
    html3 = generate_base64()
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head><title>simulator results analysis</title></head>
    <body>
        <div class="bi">
            <div class="mdi">
                <h2>Metadata information</h2>
                <p>{mti}</p>
            </div>
            <div class="cm">
                <h2>Correlation matrix</h2>
                <img src="data:image/png;base64,{html1}" />
            </div>
            <div class="cdd">
                <h2>Chicken dinner distribution</h2> 
                <img src="data:image/png;base64,{html2}" />
            </div>
        </div>
        <div class="ada">
            <h2>Analysis of all data</h2>
            <section>
                <h3>mean winrate: {mean_winrate}%</h3>
                <h3>expected gain for a single trade: {mean_excpectancy}</h3>
                <h3>expected gain% for a single trade: {mean_excpectancy_percentage}%</h3>
            </section>
            <section>
                <h3>biggest gain: {max_pnl}%</h3>
                <h3>excpected PnL (average): {mean_pnl}%</h3>
                <h3>excpected PnL (median): {median_pnl}%</h3>
            </section>
            <section>
                <h3>biggest loss: {min_pnl}%</h3>
                <h3>biggest drawdown from starting balance: {max_dd}%</h3>
                <h3>average max drawdown from starting balance: {mean_max_dd}%</h3>
                <h3>median max drawdown from starting balance: {median_max_dd}%</h3>       
            </section>
            <div class="bp">
                <img src="data:image/png;base64,{html3}" />
            </div>
        </div>
    </body>
    </html>
    """

    # Save to HTML
    with open("report.html", "w") as f:
        f.write(html_template)

#for testing purpose
"""
df = pd.read_csv('results.csv')
metadata = pd.read_csv('results_metadata.csv')

generate_report(df, metadata)
"""