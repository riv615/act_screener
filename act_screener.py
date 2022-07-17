"""Gets stock data from Yahoo Finance, stores it in csv format, and displays it on a chart."""
import tkinter as tk
from datetime import datetime
import os
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
def do_chart(name, currency):
    """Displays data about the given stock."""
    file = ".\\" + name
    c_name = GET_COLUMN.get()
    df_csv = pd.read_csv(file, index_col='Date', usecols=['Date', c_name])
    df_csv[c_name].plot()
    plt.title(file)
    plt.ylabel(c_name+', '+currency)
    plt.show()
#------------------------------------------------------------------------------
def obtain_data():
    """Gets data of the given stock."""
    if USE_PROXY.get()==1:
        pr_addr = 'http://' + IP_ADDRESS.get() + ':' + IP_PORT.get()
        print("Try obtain data with proxy...")
    else:
        pr_addr = ''
        print("Try obtain data without proxy...")
    os.environ['http_proxy'] = pr_addr
    os.environ['https_proxy'] = pr_addr
    f_name = FILE_NAME.get()
    a_name = STOCK_NAME.get()
    i_name = tk.StringVar()
    i_val = GET_INTERVAL.get()
    if i_val == 'One Day':
        i_name = '1d'
    elif i_val == 'Five Days':
        i_name = '5d'
    elif i_val == 'One Month':
        i_name = '1mo'
    else:
        i_name = '1wk'
    try:
        act_ticker = yf.Ticker(a_name)
        act_cur = act_ticker.info['currency']
        data2 = yf.download(a_name, interval=i_name, start=START_P.get(), end=END_P.get())
        data2.to_csv(f_name)
        do_chart(f_name, act_cur)
    except (ConnectionError, ConnectionRefusedError, TimeoutError):
        if act_cur is None:
            print("Read ticker error.")
        if data2 is None:
            print("Data download error.")
        return
#------------------------------------------------------------------------------
def is_proxy():
    """Enables or disables some fields."""
    if USE_PROXY.get() == 1:
        IP_ADDRESS.config(state='normal')
        IP_PORT.config(state='normal')
    else:
        IP_ADDRESS.config(state='disabled')
        IP_PORT.config(state='disabled')
#------------------------------------------------------------------------------
appWin = tk.Tk()
appWin.title('Stock Screener')
appWin.config(bg='#CCCCCC')
W = 460  # window width
H = 400  # window height
x = (appWin.winfo_screenwidth() / 2) - (W / 2)
y = (appWin.winfo_screenheight() / 2) - (H / 2)
appWin.geometry('%dx%d+%d+%d' % (W, H, x, y))
appWin.resizable(False, False)
plt.style.use('ggplot')  # beautiful chart
plt.rcParams['figure.figsize'] = (10, 4)

STOCK_NAME = tk.StringVar()
STOCK_NAME.set("AAPL")
FILE_NAME = tk.StringVar()
FILE_NAME.set("Apple.csv")

START_P = tk.StringVar()
START_P.set("2021-01-01")
END_P = tk.StringVar()
END_P.set(datetime.now().date())

GET_COLUMN = tk.StringVar()
actColumn = ('Open', 'High', 'Low', 'Close', 'Adj Close')
GET_COLUMN.set(actColumn[4])

GET_INTERVAL = tk.StringVar()
actInterval = ('One Day', 'Five Days', 'One Week', 'One Month') #1d,5d,1wk,1mo
GET_INTERVAL.set(actInterval[0])

USE_PROXY = tk.IntVar()
USE_PROXY.set(1)
ipAddress = tk.StringVar()
ipAddress.set("10.0.0.1")
ipPort = tk.StringVar()
ipPort.set("1080")

frame1 = tk.Frame(appWin, bd=1, relief=tk.SOLID, height=202, width=420, padx=10, pady=10)
tk.Label(frame1, text="Stock name", font=('Verdana', 12)).place(x=5, y=4)
tk.Label(frame1, text="File name", font=('Verdana', 12)).place(x=5, y=39)
tk.Label(frame1, text="Period", font=('Verdana', 12)).place(x=5, y=74)
tk.Label(frame1, text="Draw data", font=('Verdana', 12)).place(x=5, y=110)
tk.Label(frame1, text="Interval", font=('Verdana', 12)).place(x=5, y=150)
tk.Entry(frame1, textvariable=STOCK_NAME, font=('Verdana', 12)).place(x=120, y=5, w=150)
tk.Entry(frame1, textvariable=FILE_NAME, font=('Verdana', 12)).place(x=120, y=40, w=150)
tk.Entry(frame1, textvariable=START_P, font=('Verdana', 12)).place(x=120, y=75, w=120)
tk.Entry(frame1, textvariable=END_P, font=('Verdana', 12)).place(x=265, y=75, w=120)
regColumn = tk.OptionMenu(frame1, GET_COLUMN, *actColumn)
regColumn.config(font=('Verdana', 12))
regColumn.place(x=118, y=106)
regInterval = tk.OptionMenu(frame1, GET_INTERVAL, *actInterval)
regInterval.config(font=('Verdana', 12))
regInterval.place(x=118, y=144)
tk.Button(appWin, text='Get data and draw a chart', font=('Verdana', 12),
       command = obtain_data).place(x=100, y=347, w=260)
frame1.place(x=20, y=20)

frame2 = tk.Frame(appWin, bd=1, relief=tk.SOLID, height=85, width=420, padx=10, pady=10)
tk.Label(frame2, text="IP Address", font=('Verdana', 12)).place(x=5, y=36)
tk.Label(frame2, text="Port", font=('Verdana', 12)).place(x=264, y=36)
IP_ADDRESS = tk.Entry(frame2, textvariable=ipAddress, state='disabled', font=('Verdana', 12))
IP_ADDRESS.place(x=120, y=37, w=120)
IP_PORT = tk.Entry(frame2, textvariable=ipPort, state='disabled', font=('Verdana', 12))
IP_PORT.place(x=320, y=37, w=65)
tk.Checkbutton(frame2, text="Use HTTP proxy for connect", variable=USE_PROXY,
            font=('Verdana', 12), command=is_proxy).place(x=5, y=2)
is_proxy()
frame2.place(x=20, y=240)

appWin.bind('<Return>', lambda event=None: obtain_data())
appWin.bind('<Escape>', lambda event=None: appWin.destroy())
appWin.mainloop()
