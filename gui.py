# gui.py

import sys
import data_processing
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.ticker import FormatStrFormatter, MaxNLocator, FuncFormatter
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QMessageBox, QComboBox, QDialog
)
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from translations import translations

# 定義主題樣式表
light_style = """
QWidget {
    background-color: #ffffff;
    color: #000000;
}
"""

dark_style = """
QWidget {
    background-color: #2e2e2e;
    color: #ffffff;
}
"""

class StartWindow(QWidget):
    """開始界面，讓用戶選擇計算方式、語言和主題"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("選擇設置")
        self.setGeometry(100, 100, 400, 250)
        layout = QVBoxLayout()

        # 計算方式選擇
        self.calc_label = QLabel("請選擇報酬率計算方式：")
        self.calc_combo_box = QComboBox()
        self.calc_combo_box.addItems(["標準累計收益率", "基於初始資金和固定風險金額"])

        # 語言選擇
        self.lang_label = QLabel("請選擇語言 / Language:")
        self.lang_combo_box = QComboBox()
        self.lang_combo_box.addItems(["中文", "English"])

        # 主題選擇
        self.theme_label = QLabel("請選擇主題 / Theme:")
        self.theme_combo_box = QComboBox()
        self.theme_combo_box.addItems(["淺色 / Light", "深色 / Dark"])

        # 下一步按鈕
        self.next_button = QPushButton("下一步 / Next")
        self.next_button.clicked.connect(self.next_step)

        layout.addWidget(self.calc_label)
        layout.addWidget(self.calc_combo_box)
        layout.addWidget(self.lang_label)
        layout.addWidget(self.lang_combo_box)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo_box)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

        # 保存用戶選擇
        self.selected_option = None
        self.selected_language = '中文'
        self.selected_theme = '淺色'

    def next_step(self):
        self.selected_option = self.calc_combo_box.currentIndex()
        self.selected_language = self.lang_combo_box.currentText()
        self.selected_theme = self.theme_combo_box.currentText()
        self.close()

class StandardTradingApp(QMainWindow):
    """標準累計收益率計算方式"""
    def __init__(self, language='中文', theme='淺色'):
        super().__init__()
        self.language = language
        self.theme = theme
        self.trans = translations[self.language]
        self.setWindowTitle(self.trans['standard_mode'])

        # 應用主題
        if self.theme in ['淺色 / Light', '淺色']:
            self.setStyleSheet(light_style)
        elif self.theme in ['深色 / Dark', '深色']:
            self.setStyleSheet(dark_style)

        self.setGeometry(100, 100, 1000, 600)

        # 初始化數據列表
        self.returns = []

        # 加載數據
        self.load_data()

        # 創建主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # 創建主佈局
        self.main_layout = QHBoxLayout(self.main_widget)

        # 左側：交易記錄列表
        self.left_layout = QVBoxLayout()
        self.data_label = QLabel(self.trans['trade_record'])
        self.data_list = QListWidget()
        self.left_layout.addWidget(self.data_label)
        self.left_layout.addWidget(self.data_list)

        # 中間：繪圖區域
        self.center_layout = QVBoxLayout()
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(self.trans['chart_title_standard'])
        self.ax.set_xlabel(self.trans['x_label'])
        self.ax.set_ylabel(self.trans['y_label_standard'])
        self.center_layout.addWidget(self.canvas)

        # 右側：輸入和指標顯示
        self.right_layout = QVBoxLayout()
        self.input_label = QLabel(self.trans['input_label'])
        self.input_edit = QLineEdit()
        self.submit_button = QPushButton(self.trans['submit'])
        self.submit_button.clicked.connect(self.submit_return)
        self.input_edit.returnPressed.connect(self.submit_return)  # 支持按 Enter 鍵提交

        self.total_return_label = QLabel(self.trans['total_return'].format(0.00))
        self.max_drawdown_label = QLabel(self.trans['max_drawdown'].format(0.00))
        self.longest_profit_label = QLabel(self.trans['longest_profit'].format(0))
        self.longest_loss_label = QLabel(self.trans['longest_loss'].format(0))

        # 添加用於顯示坐標的標籤
        self.coord_label = QLabel(self.trans['coordinate'].format('', ''))

        self.right_layout.addWidget(self.input_label)
        self.right_layout.addWidget(self.input_edit)
        self.right_layout.addWidget(self.submit_button)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.total_return_label)
        self.right_layout.addWidget(self.max_drawdown_label)
        self.right_layout.addWidget(self.longest_profit_label)
        self.right_layout.addWidget(self.longest_loss_label)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.coord_label)
        self.right_layout.addStretch()

        # 將佈局添加到主佈局
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.center_layout, 3)
        self.main_layout.addLayout(self.right_layout, 1)

        # 連接鼠標移動事件
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

        # 創建菜單
        self.create_menus()

    def create_menus(self):
        menubar = self.menuBar()
        menubar.clear()

        # 設置菜單
        settings_menu = menubar.addMenu(self.trans['settings'])

        # 語言子菜單
        language_menu = settings_menu.addMenu(self.trans['language'])
        lang_action_cn = QAction('中文', self)
        lang_action_en = QAction('English', self)
        lang_action_cn.triggered.connect(lambda: self.change_language('中文'))
        lang_action_en.triggered.connect(lambda: self.change_language('English'))
        language_menu.addAction(lang_action_cn)
        language_menu.addAction(lang_action_en)

        # 主題子菜單
        theme_menu = settings_menu.addMenu(self.trans['theme'])
        theme_action_light = QAction(self.trans['light_theme'], self)
        theme_action_dark = QAction(self.trans['dark_theme'], self)
        theme_action_light.triggered.connect(lambda: self.change_theme('淺色'))
        theme_action_dark.triggered.connect(lambda: self.change_theme('深色'))
        theme_menu.addAction(theme_action_light)
        theme_menu.addAction(theme_action_dark)

        # 添加「清除歷史記錄」菜單項
        clear_action = QAction(self.trans['clear_history'], self)
        clear_action.triggered.connect(self.clear_data)
        settings_menu.addAction(clear_action)

    def clear_data(self):
        # 提示用戶確認
        reply = QMessageBox.question(self, self.trans['clear_history'], 
                                     self.trans['confirm_clear_history'], 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 清空交易記錄
            self.returns = []
            # 刪除數據文件
            try:
                data_file = 'standard_data.json'
                if os.path.exists(data_file):
                    os.remove(data_file)
            except Exception as e:
                QMessageBox.warning(self, self.trans['input_error'], str(e))
            # 重置界面
            self.update_data_list()
            self.update_metrics()
            self.update_plot()

    def change_language(self, language):
        self.language = language
        self.trans = translations[self.language]
        self.update_texts()

    def change_theme(self, theme):
        self.theme = theme
        if self.theme in ['淺色 / Light', '淺色']:
            self.setStyleSheet(light_style)
        elif self.theme in ['深色 / Dark', '深色']:
            self.setStyleSheet(dark_style)

    def update_texts(self):
        # 更新界面中所有的文本
        self.setWindowTitle(self.trans['standard_mode'])
        self.input_label.setText(self.trans['input_label'])
        self.submit_button.setText(self.trans['submit'])
        self.data_label.setText(self.trans['trade_record'])
        self.coord_label.setText(self.trans['coordinate'].format('', ''))
        self.ax.set_title(self.trans['chart_title_standard'])
        self.ax.set_xlabel(self.trans['x_label'])
        self.ax.set_ylabel(self.trans['y_label_standard'])
        self.update_metrics()
        self.update_data_list()
        self.create_menus()
        self.canvas.draw()

    def submit_return(self):
        try:
            # 獲取並轉換輸入的報酬率
            return_rate = float(self.input_edit.text()) / 100
            self.returns.append(return_rate)
            self.input_edit.clear()

            # 更新數據列表
            self.update_data_list()

            # 更新指標
            self.update_metrics()

            # 更新圖表
            self.update_plot()
        except ValueError:
            QMessageBox.warning(self, self.trans['input_error'], self.trans['input_error_message'])

    def update_data_list(self):
        self.data_list.clear()
        for idx, r in enumerate(self.returns, 1):
            percent_return = r * 100
            self.data_list.addItem(self.trans['trade_item'].format(idx, percent_return))

    def update_metrics(self):
        if self.returns:
            # 計算累計收益率
            cumulative_returns = data_processing.calculate_cumulative_returns(self.returns)
            total_return = cumulative_returns[-1] * 100

            # 計算最大回撤
            max_drawdown = data_processing.calculate_max_drawdown(cumulative_returns) * 100

            # 計算最長連續獲利和最長連續虧損
            longest_profit, longest_loss = data_processing.calculate_longest_profit_loss_streak(self.returns)
        else:
            total_return = 0.00
            max_drawdown = 0.00
            longest_profit = 0
            longest_loss = 0

        # 更新顯示標籤
        self.total_return_label.setText(self.trans['total_return'].format(total_return))
        self.max_drawdown_label.setText(self.trans['max_drawdown'].format(max_drawdown))
        self.longest_profit_label.setText(self.trans['longest_profit'].format(longest_profit))
        self.longest_loss_label.setText(self.trans['longest_loss'].format(longest_loss))

    def update_plot(self):
        # 清除之前的繪圖
        self.ax.clear()
        self.ax.set_title(self.trans['chart_title_standard'])
        self.ax.set_xlabel(self.trans['x_label'])
        self.ax.set_ylabel(self.trans['y_label_standard'])

        if self.returns:
            # 計算資產增長率曲線
            cumulative_returns = data_processing.calculate_cumulative_returns(self.returns)
            x_data = np.arange(1, len(cumulative_returns) + 1)
            y_data = cumulative_returns * 100

            # 繪制曲線
            self.ax.plot(x_data, y_data, marker='o')

            # 設置 x 軸刻度為整數
            self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            self.ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x)}'))

            # 設置 y 軸刻度格式為小數點後兩位
            self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        else:
            # 如果沒有數據，繪制空圖
            self.ax.plot([], [])

        # 重繪圖表
        self.canvas.draw()

    def on_mouse_move(self, event):
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                # 格式化坐標顯示
                x_formatted = int(round(x))
                y_formatted = f"{y:.2f}"
                self.coord_label.setText(self.trans['coordinate'].format(x_formatted, y_formatted))
            else:
                self.coord_label.setText(self.trans['coordinate'].format('', ''))
        else:
            self.coord_label.setText(self.trans['coordinate'].format('', ''))

    # 添加數據保存和加載方法
    def load_data(self):
        """加載保存的數據"""
        try:
            with open('standard_data.json', 'r') as f:
                data = json.load(f)
                self.returns = data.get('returns', [])
        except FileNotFoundError:
            # 文件不存在，首次運行
            pass
        except Exception as e:
            QMessageBox.warning(self, self.trans['input_error'], str(e))

    def save_data(self):
        """保存當前數據"""
        data = {
            'returns': self.returns
        }
        try:
            with open('standard_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            QMessageBox.warning(self, self.trans['input_error'], str(e))

    def closeEvent(self, event):
        """窗口關閉事件"""
        self.save_data()
        event.accept()

class RiskBasedTradingApp(QMainWindow):
    """基於初始資金和固定風險金額的計算方式"""
    def __init__(self, initial_capital, risk_per_trade, language='中文', theme='淺色'):
        super().__init__()
        self.language = language
        self.theme = theme
        self.trans = translations[self.language]
        self.setWindowTitle(self.trans['risk_mode'])

        # 應用主題
        if self.theme in ['淺色 / Light', '淺色']:
            self.setStyleSheet(light_style)
        elif self.theme in ['深色 / Dark', '深色']:
            self.setStyleSheet(dark_style)

        self.setGeometry(100, 100, 1000, 600)

        # 初始化數據列表
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.returns = []

        # 加載數據
        self.load_data()

        # 創建主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # 創建主佈局
        self.main_layout = QHBoxLayout(self.main_widget)

        # 左側：交易記錄列表
        self.left_layout = QVBoxLayout()
        self.data_label = QLabel(self.trans['trade_record'])
        self.data_list = QListWidget()
        self.left_layout.addWidget(self.data_label)
        self.left_layout.addWidget(self.data_list)

        # 中間：繪圖區域
        self.center_layout = QVBoxLayout()
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(self.trans['chart_title_risk'])
        self.ax.set_xlabel(self.trans['x_label'])
        self.ax.set_ylabel(self.trans['y_label_risk'])
        self.center_layout.addWidget(self.canvas)

        # 右側：輸入和指標顯示
        self.right_layout = QVBoxLayout()
        self.input_label = QLabel(self.trans['input_label_rr'])
        self.input_edit = QLineEdit()
        self.submit_button = QPushButton(self.trans['submit'])
        self.submit_button.clicked.connect(self.submit_return)
        self.input_edit.returnPressed.connect(self.submit_return)  # 支持按 Enter 鍵提交

        self.total_return_label = QLabel(self.trans['current_capital'].format(self.initial_capital))
        self.max_drawdown_label = QLabel(self.trans['max_drawdown'].format(0.00))
        self.longest_profit_label = QLabel(self.trans['longest_profit'].format(0))
        self.longest_loss_label = QLabel(self.trans['longest_loss'].format(0))

        # 添加用於顯示坐標的標籤
        self.coord_label = QLabel(self.trans['coordinate'].format('', ''))

        self.right_layout.addWidget(self.input_label)
        self.right_layout.addWidget(self.input_edit)
        self.right_layout.addWidget(self.submit_button)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.total_return_label)
        self.right_layout.addWidget(self.max_drawdown_label)
        self.right_layout.addWidget(self.longest_profit_label)
        self.right_layout.addWidget(self.longest_loss_label)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.coord_label)
        self.right_layout.addStretch()

        # 將佈局添加到主佈局
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.center_layout, 3)
        self.main_layout.addLayout(self.right_layout, 1)

        # 連接鼠標移動事件
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

        # 創建菜單
        self.create_menus()

    def create_menus(self):
        # ...（與 StandardTradingApp 中的 create_menus 方法相同）
        menubar = self.menuBar()
        menubar.clear()

        # 設置菜單
        settings_menu = menubar.addMenu(self.trans['settings'])

        # 語言子菜單
        language_menu = settings_menu.addMenu(self.trans['language'])
        lang_action_cn = QAction('中文', self)
        lang_action_en = QAction('English', self)
        lang_action_cn.triggered.connect(lambda: self.change_language('中文'))
        lang_action_en.triggered.connect(lambda: self.change_language('English'))
        language_menu.addAction(lang_action_cn)
        language_menu.addAction(lang_action_en)

        # 主題子菜單
        theme_menu = settings_menu.addMenu(self.trans['theme'])
        theme_action_light = QAction(self.trans['light_theme'], self)
        theme_action_dark = QAction(self.trans['dark_theme'], self)
        theme_action_light.triggered.connect(lambda: self.change_theme('淺色'))
        theme_action_dark.triggered.connect(lambda: self.change_theme('深色'))
        theme_menu.addAction(theme_action_light)
        theme_menu.addAction(theme_action_dark)

        # 添加「清除歷史記錄」菜單項
        clear_action = QAction(self.trans['clear_history'], self)
        clear_action.triggered.connect(self.clear_data)
        settings_menu.addAction(clear_action)

    def clear_data(self):
        # 提示用戶確認
        reply = QMessageBox.question(self, self.trans['clear_history'], 
                                     self.trans['confirm_clear_history'], 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 清空交易記錄
            self.returns = []
            # 刪除數據文件
            try:
                data_file = 'risk_data.json'
                if os.path.exists(data_file):
                    os.remove(data_file)
            except Exception as e:
                QMessageBox.warning(self, self.trans['input_error'], str(e))
            # 重置界面
            self.update_data_list()
            self.update_metrics()
            self.update_plot()

    def change_language(self, language):
        self.language = language
        self.trans = translations[self.language]
        self.update_texts()

    def change_theme(self, theme):
        self.theme = theme
        if self.theme in ['淺色 / Light', '淺色']:
            self.setStyleSheet(light_style)
        elif self.theme in ['深色 / Dark', '深色']:
            self.setStyleSheet(dark_style)

    def update_texts(self):
        # 更新界面中所有的文本
        self.setWindowTitle(self.trans['risk_mode'])
        self.input_label.setText(self.trans['input_label_rr'])
        self.submit_button.setText(self.trans['submit'])
        self.data_label.setText(self.trans['trade_record'])
        self.coord_label.setText(self.trans['coordinate'].format('', ''))
        self.ax.set_title(self.trans['chart_title_risk'])
        self.ax.set_xlabel(self.trans['x_label'])
        self.ax.set_ylabel(self.trans['y_label_risk'])
        self.update_metrics()
        self.update_data_list()
        self.create_menus()
        self.canvas.draw()

    def submit_return(self):
        try:
            # 獲取並轉換輸入的風險回報比
            rr_ratio = float(self.input_edit.text())
            if rr_ratio < 0:
                QMessageBox.warning(self, self.trans['input_error'], self.trans['negative_rr_error'])
                return
            self.returns.append(rr_ratio)
            self.input_edit.clear()

            # 更新數據列表
            self.update_data_list()

            # 更新指標
            self.update_metrics()

            # 更新圖表
            self.update_plot()
        except ValueError:
            QMessageBox.warning(self, self.trans['input_error'], self.trans['input_error_message'])

    def update_data_list(self):
        self.data_list.clear()
        for idx, rr in enumerate(self.returns, 1):
            self.data_list.addItem(self.trans['trade_item_rr'].format(idx, rr))

    def update_metrics(self):
        if self.returns:
            # 計算每筆交易的盈虧金額
            profits_losses = []
            for rr in self.returns:
                if rr == 0:
                    # 虧損交易
                    profit = -self.risk_per_trade
                else:
                    # 盈利交易
                    profit = (rr - 1) * self.risk_per_trade
                profits_losses.append(profit)

            # 計算資金曲線
            capital_curve = [self.initial_capital]
            for pl in profits_losses:
                new_capital = capital_curve[-1] + pl
                capital_curve.append(new_capital)
            capital_curve = np.array(capital_curve[1:])
            current_capital = capital_curve[-1]

            # 計算最大回撤
            drawdowns = capital_curve - np.maximum.accumulate(capital_curve)
            max_drawdown = drawdowns.min()

            # 計算最長連續獲利和最長連續虧損
            results = [1 if pl > 0 else -1 for pl in profits_losses]
            longest_profit, longest_loss = data_processing.calculate_longest_streak(results)
        else:
            current_capital = self.initial_capital
            max_drawdown = 0.00
            longest_profit = 0
            longest_loss = 0

        # 更新顯示標籤
        self.total_return_label.setText(self.trans['current_capital'].format(current_capital))
        self.max_drawdown_label.setText(self.trans['max_drawdown'].format(max_drawdown))
        self.longest_profit_label.setText(self.trans['longest_profit'].format(longest_profit))
        self.longest_loss_label.setText(self.trans['longest_loss'].format(longest_loss))

    def update_plot(self):
        # 清除之前的繪圖
        self.ax.clear()
        self.ax.set_title(self.trans['chart_title_risk'])
        self.ax.set_xlabel(self.trans['x_label'])
        self.ax.set_ylabel(self.trans['y_label_risk'])

        if self.returns:
            # 計算每筆交易的盈虧金額
            profits_losses = []
            for rr in self.returns:
                if rr == 0:
                    # 虧損交易
                    profit = -self.risk_per_trade
                else:
                    # 盈利交易
                    profit = (rr - 1) * self.risk_per_trade
                profits_losses.append(profit)

            # 計算資金曲線
            capital_curve = [self.initial_capital]
            for pl in profits_losses:
                new_capital = capital_curve[-1] + pl
                capital_curve.append(new_capital)
            capital_curve = np.array(capital_curve[1:])
            x_data = np.arange(1, len(capital_curve) + 1)
            y_data = capital_curve

            # 繪制曲線
            self.ax.plot(x_data, y_data, marker='o')

            # 設置 x 軸刻度為整數
            self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            self.ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x)}'))

            # 設置 y 軸刻度格式為兩位小數
            self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        else:
            # 如果沒有數據，繪制空圖
            self.ax.plot([], [])

        # 重繪圖表
        self.canvas.draw()

    def on_mouse_move(self, event):
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                # 格式化坐標顯示
                x_formatted = int(round(x))
                y_formatted = f"{y:.2f}"
                self.coord_label.setText(self.trans['coordinate'].format(x_formatted, y_formatted))
            else:
                self.coord_label.setText(self.trans['coordinate'].format('', ''))
        else:
            self.coord_label.setText(self.trans['coordinate'].format('', ''))

    def load_data(self):
        """加載保存的數據"""
        try:
            with open('risk_data.json', 'r') as f:
                data = json.load(f)
                self.initial_capital = data.get('initial_capital', self.initial_capital)
                self.risk_per_trade = data.get('risk_per_trade', self.risk_per_trade)
                self.returns = data.get('returns', [])
        except FileNotFoundError:
            # 文件不存在，首次運行
            pass
        except Exception as e:
            QMessageBox.warning(self, self.trans['input_error'], str(e))

    def save_data(self):
        """保存當前數據"""
        data = {
            'initial_capital': self.initial_capital,
            'risk_per_trade': self.risk_per_trade,
            'returns': self.returns
        }
        try:
            with open('risk_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            QMessageBox.warning(self, self.trans['input_error'], str(e))

    def closeEvent(self, event):
        """窗口關閉事件"""
        self.save_data()
        event.accept()

class InitialSettingsDialog(QDialog):
    """用於輸入初始資金和固定風險金額的對話框"""
    def __init__(self, language='中文', theme='淺色'):
        super().__init__()
        self.language = language
        self.theme = theme
        self.trans = translations[self.language]
        self.setWindowTitle(self.trans['settings'])
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        self.capital_label = QLabel(self.trans['capital_input'])
        self.capital_edit = QLineEdit()
        self.risk_label = QLabel(self.trans['risk_input'])
        self.risk_edit = QLineEdit()
        self.ok_button = QPushButton(self.trans['submit'])
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.capital_label)
        layout.addWidget(self.capital_edit)
        layout.addWidget(self.risk_label)
        layout.addWidget(self.risk_edit)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        # 應用主題
        if self.theme in ['淺色 / Light', '淺色']:
            self.setStyleSheet(light_style)
        elif self.theme in ['深色 / Dark', '深色']:
            self.setStyleSheet(dark_style)

    def get_values(self):
        try:
            capital = float(self.capital_edit.text())
            risk = float(self.risk_edit.text())
            return capital, risk
        except ValueError:
            QMessageBox.warning(self, self.trans['input_error'], self.trans['input_error_message'])
            return None, None
