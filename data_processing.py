# data_processing.py

import numpy as np

def calculate_cumulative_returns(returns):
    """計算累計收益率"""
    cumulative_returns = np.cumprod([1 + r for r in returns]) - 1
    return cumulative_returns

def calculate_max_drawdown(cumulative_returns):
    """計算最大回撤"""
    drawdowns = cumulative_returns - np.maximum.accumulate(cumulative_returns)
    max_drawdown = drawdowns.min()
    return max_drawdown

def calculate_longest_profit_loss_streak(returns):
    """計算最長連續獲利和最長連續虧損"""
    longest_profit = 0
    longest_loss = 0
    current_profit = 0
    current_loss = 0

    for r in returns:
        if r > 0:
            current_profit += 1
            current_loss = 0
        elif r < 0:
            current_loss += 1
            current_profit = 0
        else:
            # 當收益率為0時，視為中斷連續性
            current_profit = 0
            current_loss = 0

        if current_profit > longest_profit:
            longest_profit = current_profit
        if current_loss > longest_loss:
            longest_loss = current_loss

    return longest_profit, longest_loss

def calculate_longest_streak(results):
    """計算最長連續獲利和虧損"""
    longest_profit = 0
    longest_loss = 0
    current_profit = 0
    current_loss = 0

    for r in results:
        if r > 0:
            current_profit += 1
            current_loss = 0
        elif r < 0:
            current_loss += 1
            current_profit = 0
        else:
            current_profit = 0
            current_loss = 0

        if current_profit > longest_profit:
            longest_profit = current_profit
        if current_loss > longest_loss:
            longest_loss = current_loss

    return longest_profit, longest_loss
