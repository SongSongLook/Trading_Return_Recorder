# plotting.py

import matplotlib.pyplot as plt

def create_plot():
    """創建初始的 matplotlib 圖形和軸"""
    figure = plt.Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.set_title("資產增長率曲線")
    ax.set_xlabel("交易次數")
    ax.set_ylabel("資產增長率（%）")
    return figure, ax

def update_plot(ax, cumulative_returns):
    """更新資產增長率曲線"""
    ax.clear()
    ax.set_title("資產增長率曲線")
    ax.set_xlabel("交易次數")
    ax.set_ylabel("資產增長率（%）")
    ax.plot(cumulative_returns * 100, marker='o')
