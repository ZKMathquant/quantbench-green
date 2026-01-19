import matplotlib.pyplot as plt
import numpy as np

def plot_drawdown(prices, name="drawdown.png"):
    returns = prices.pct_change().dropna()
    cumulative = (1 + returns).cumprod()
    drawdown = cumulative / cumulative.cummax() - 1

    drawdown.plot(title="Max Drawdown")
    plt.savefig(name)
    plt.close()
