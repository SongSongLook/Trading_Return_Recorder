# main.py

import sys
from PyQt6.QtWidgets import QApplication, QDialog
from gui import StartWindow, StandardTradingApp, RiskBasedTradingApp, InitialSettingsDialog
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 顯示開始界面
    start_window = StartWindow()
    start_window.show()
    app.exec()

    # 根據用戶選擇，啓動相應的界面
    language = start_window.selected_language
    theme = start_window.selected_theme

    if start_window.selected_option == 0:
        # 標準累計收益率
        window = StandardTradingApp(language, theme)
    elif start_window.selected_option == 1:
        # 基於初始資金和固定風險金額
        data_file_exists = os.path.exists('risk_data.json')
        if data_file_exists:
            # 如果數據文件存在，直接加載數據
            window = RiskBasedTradingApp(0, 0, language, theme)
        else:
            # 彈出對話框，輸入初始資金和風險金額
            dialog = InitialSettingsDialog(language, theme)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                initial_capital, risk_per_trade = dialog.get_values()
                if initial_capital is not None and risk_per_trade is not None:
                    window = RiskBasedTradingApp(initial_capital, risk_per_trade, language, theme)
                else:
                    sys.exit()
            else:
                sys.exit()
    else:
        sys.exit()

    window.show()
    sys.exit(app.exec())
