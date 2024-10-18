# Equity_Return_Curve_Calculator

# Trading Return Recorder

A graphical application to record and analyze your trading returns. The application supports two modes of calculating returns, provides multi-language support (English and Chinese), theme switching between light and dark modes, and features data persistence and a one-click history clearing function.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Start Window](#start-window)
  - [Standard Mode](#standard-mode)
  - [Risk Mode](#risk-mode)
- [Data Persistence](#data-persistence)
- [Clearing History](#clearing-history)
- [Dependencies](#dependencies)
- [Notes](#notes)
- [License](#license)

---

## Features

- **Two Calculation Modes**:
  - **Standard Cumulative Return**: Calculate returns based on standard cumulative percentage gains and losses.
  - **Risk-Based Return**: Calculate returns based on initial capital and fixed risk amount per trade, inputting risk-reward ratios with risk set to 1.

- **Multi-Language Support**:
  - **English**
  - **中文**

- **Theme Switching**:
  - **Light Theme**
  - **Dark Theme**

- **Data Persistence**:
  - Automatically saves trading data; data is loaded upon restarting the application.

- **One-Click History Clearing**:
  - Clear all trading data and records with a single click.

---

## Installation

### **Prerequisites**

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **Pip**: Python package manager.

### **Required Python Packages**

Install the following packages using `pip`:

```bash
pip install PyQt6 numpy matplotlib
```
### **Download the Source Code**

Clone the repository or download the source code files and place them in the same directory:

- `data_processing.py`
- `translations.py`
- `gui.py`
- `main.py`

---

## Running the Application

Navigate to the directory containing the source code files and run:

```bash
python main.py
```
---

## Usage

### **Start Window**

Upon launching the application, the **Start Window** appears, allowing you to set initial preferences:

- **Calculation Method**:
  - **Standard Cumulative Return**
  - **Risk-Based Return with Initial Capital and Fixed Risk Amount**

- **Language**:
  - **中文**
  - **English**

- **Theme**:
  - **淺色 / Light**
  - **深色 / Dark**

Select your preferences and click **"Next / 下一步"** to proceed.

### **Standard Mode**

In **Standard Mode**, you can record your trades based on standard cumulative percentage returns.

#### **Interface Overview**

- **Left Panel**: Trade records list.
- **Center Panel**: Cumulative return chart.
- **Right Panel**:
  - **Input Field**: Enter the return rate (%) for each trade.
  - **Indicators**:
    - Total Return
    - Max Drawdown
    - Longest Profit Streak
    - Longest Loss Streak
  - **Coordinate Display**: Shows the coordinates when hovering over the chart.

#### **How to Use**

1. **Input Return Rate**: Enter the return rate (as a percentage) for each trade in the input field on the right panel.
   - **Example**: Enter `5` for a 5% gain, or `-3` for a 3% loss.
2. **Submit**: Click the **"Submit"** button or press **Enter** to record the trade.
3. **View Updates**:
   - The trade is added to the **Trade Records** list.
   - The **Cumulative Return Chart** updates to reflect the new data.
   - The **Indicators** update to show the new metrics.

### **Risk Mode**

In **Risk Mode**, you calculate returns based on initial capital and a fixed risk amount per trade, inputting the risk-reward ratio with risk set to 1.

#### **Initial Setup**

- Upon selecting Risk Mode, you are prompted to enter:
  - **Initial Capital Amount**
  - **Fixed Risk Amount per Trade**

#### **Interface Overview**

- **Left Panel**: Trade records list showing the risk-reward ratio for each trade.
- **Center Panel**: Capital curve chart.
- **Right Panel**:
  - **Input Field**: Enter the risk-reward ratio for each trade (enter `0` for a losing trade).
  - **Indicators**:
    - Current Capital
    - Max Drawdown
    - Longest Profit Streak
    - Longest Loss Streak
  - **Coordinate Display**: Shows the coordinates when hovering over the chart.

#### **How to Use**

1. **Input Risk-Reward Ratio**:
   - **Winning Trade**: Enter a positive number representing the risk-reward ratio (e.g., `1.5` for a 1.5x return).
   - **Losing Trade**: Enter `0`.
2. **Submit**: Click the **"Submit"** button or press **Enter** to record the trade.
3. **View Updates**:
   - The trade is added to the **Trade Records** list.
   - The **Capital Curve Chart** updates to reflect the new data.
   - The **Indicators** update to show the new metrics.

---

## Data Persistence

- **Automatic Saving**: Trading data is automatically saved when the application is closed.
- **Data Files**:
  - **Standard Mode**: `standard_data.json`
  - **Risk Mode**: `risk_data.json`
- **Data Loading**: Upon starting the application, data is automatically loaded, and the previous state is restored.

---

## Clearing History

To clear all trading data and reset the application:

1. **Access the Menu**:
   - Click on **"Settings"** in the menu bar.
2. **Select "Clear History"**:
   - Choose **"Clear History"** from the dropdown.
3. **Confirm Action**:
   - A confirmation dialog will appear.
   - Click **"Yes"** to confirm and clear all data.
4. **Result**:
   - All trading records are deleted.
   - The application resets to its initial state.

**Note**: This action is irreversible. All data will be permanently deleted.

---

## Dependencies

- **Python 3.x**
- **PyQt6**
- **NumPy**
- **Matplotlib**

Ensure all dependencies are installed to prevent any runtime errors.

---

## Notes

- **Input Validation**:
  - Always enter valid numerical values in the input fields.
  - The application will prompt you if the input is invalid.

- **Language and Theme Switching**:
  - You can switch languages and themes at any time via the **"Settings"** menu.
  - The interface updates immediately to reflect the changes.

- **Data Files**:
  - The data files (`standard_data.json` and `risk_data.json`) are stored in the same directory as the application.
  - Ensure you have write permissions to this directory.

- **Multiple Users or Accounts**:
  - Currently, the application does not support multiple users or accounts.
  - All data is stored globally for the application.

---

## License

This project is licensed under the **MIT License**.

---


