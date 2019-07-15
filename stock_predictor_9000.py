#
#   Created by Ameen Ahmed (es18626) for 'Introduction to Programming' final project
#    *** author cannot guarantee effectiveness of this stock prediction program ***
#              * however if a profit is made, the author requests 80% *
#
# ================================ IMPORTS ====================================#
# GUI
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

# Plotting (TkAgg backend required for integration with tkinter)
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

# Data attainment/processing
import quandl
import csv
import pandas as pd
import numpy as np
from datetime import datetime
from decimal import Decimal

# Machine learning
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression


# ============================= FUNCION DEFINITIONS =================================#


# =============================================================================
# Removes all widgets from screen and/or continues next frame of program
# =============================================================================
def clear_intro():

    intro_frame.destroy()
    buttonpressed.set(0)

def clear_pick_stock():

    pick_stock_frame.destroy()
    buttonpressed.set(0)

def clear_alg_desc():

    alg_desc_frame.destroy()
    buttonpressed.set(0)

# =============================================================================
# Retrieve the company's name from its stock ticker
# =============================================================================
def get_company(ticker):
    # Open CSV containing company names and their respective ticker
    with open('csv/stock_tickers.csv', 'r') as csvfile:
        company_name = []
        names_tickers = csv.reader(csvfile)
        # If user submitted ticker matches ticker in CSV file, return adjacent cell (company's name)
        for row in names_tickers:
            if row[0] == ticker:
                company_name.append(row[1])
                return str(company_name[0])

# =============================================================================
# Extracts company ticker from entry and requests appropriate data from quandl
# =============================================================================

def get_stock_data():
    # Get company name from entry
    stock_ticker = stock_entry.get().upper()
    # Request company name from quandl. Catch error if not found in database and prompt to try again
    try:
        quandl.get("WIKI/" + stock_ticker + ".11", start_date="2017-09-01")
    except:
        # Create error label if stock not found
        stock_error = Label(pick_stock_frame, text="Stock ticker not found!\nTry again.",fg = "red", font=("Helvetica Light", 10, "bold"))
        stock_error.grid(column=2, row=5)
    else:
        # Else return data retrieved from quandl
        buttonpressed.set(0)
        stock_data = quandl.get("WIKI/" + stock_ticker + ".11", start_date="2016-01-01" )

        return stock_data

# =============================================================================
# Return kernel choice from radio buttons then clear screen for next frame
# =============================================================================
def save_kernel_choice():

    if kernel_radio_choice.get() == 1:
        kernel_choice = "poly"
    if kernel_radio_choice.get() == 2:
        kernel_choice = "rbf"
    if kernel_radio_choice.get() == 3:
        kernel_choice = "linear"

    buttonpressed1.set(0)

    return kernel_choice

# =============================================================================
# Get and return day from entry, then clear screen for next frame
# =============================================================================
def get_selected_day():

    day_selected = day_select_entry.get()
    buttonpressed1.set(0)

    return day_selected


# ============================= PROGRAM FLOW =================================#

# Root window set up
root = Tk()
root.geometry("800x475")
root.title("Stock Predictor 9000")
root.resizable(False, False)

# Predefined variables image paths
quandl.ApiConfig.api_key = "h6MRet_NwMvaixuF8EoD"
logo_path = ImageTk.PhotoImage(Image.open("images/Logo.png"))
svr_img_path = ImageTk.PhotoImage(Image.open("images/SVRDesc.png"))
kernel_img_path = ImageTk.PhotoImage(Image.open("images/kernelDesc.png"))

# Variables used in wait_variable() to maintain chronology of program
buttonpressed = BooleanVar()
buttonpressed1 = BooleanVar()

# Empty lists for SVR algorithm
days_since_start = []
prediction_days = []


# =============================================================================
# First frame: logo + 'Start' button
# =============================================================================
intro_frame = Frame(root)
intro_frame.pack()

# 'Stock Predictor 9000' logo displayed at start
logo = Label(intro_frame, image = logo_path)
logo.grid(column = 2, row = 1)

# When user clicks 'Start', run clear_intro which destroys all widgets in intro_frame for the next
start_button = Button(intro_frame, text = "Start", command=clear_intro, padx = 6, pady = 6)
start_button.grid(column = 2, row = 5)

# Waits for buttonpressed to be reset (in clear_intro) before entering next frame
start_button.wait_variable(buttonpressed)


# =============================================================================
# Second frame: select and display stock
# =============================================================================
pick_stock_frame = Frame(root)
pick_stock_frame.pack()

# "PICK YOUR STOCK" text
pick_stock_label = Label(pick_stock_frame, text = "PICK YOUR STOCK", fg = "#727070", font=("Helvetica Light", 60, "bold"))
pick_stock_label.grid(column = 2, row = 1)

# Input instructions above entry
instructions_label = Label(pick_stock_frame, text = "enter the stock ticker for the company you'd like (for example, Google = 'GOOG')", fg = "grey", font=("Helvetica Light", 15, "bold"))
instructions_label.grid(column = 2, row = 2)

# Entry for stock ticker
stock_entry = Entry(pick_stock_frame)
stock_entry.grid(column = 2, row = 3)

# When user clicks 'Enter', run get_stock_data which gets stock data
enter_button = Button(pick_stock_frame, text = "Enter", command=get_stock_data)
enter_button.grid(column = 2, row = 4)

# Waits for buttonpressed to be reset (in clear_intro) before creating stock graph
enter_button.wait_variable(buttonpressed)

# Get stock data from quandl
stock_graph = get_stock_data()

# Display stock data
stock_fig = Figure(figsize=(7, 2.8))

# Get stock ticker from entry and pass to get_company() for company name
ticker = stock_entry.get().upper()
company_name = get_company(ticker)
# Date (X) is stored as a pandas dataframe index from quandl; this line converts that to list
X = stock_graph.index.tolist()
# Set close column as Y
Y = stock_graph["Adj. Close"]

# Create matplotlib plot of stock selected
plot_frame_2 = stock_fig.add_subplot(111)
plot_frame_2.plot(X, Y)
plot_frame_2.set_title(company_name, fontsize=16)
plot_frame_2.set_ylabel("Adj. Close ($)", fontsize=8)
stock_fig.autofmt_xdate()

# Embedded plot into GUI
plot_frame_2_canvas = FigureCanvasTkAgg(stock_fig, master=pick_stock_frame)
plot_frame_2_canvas.get_tk_widget().grid(column = 2, row = 5)
plot_frame_2_canvas.draw()

# When user clicks 'Continue', run clear_pick_stock() which proceeds to next frame
continue_button = Button(pick_stock_frame, text = "Continue", command=clear_pick_stock, padx = 6, pady = 6)
continue_button.grid(column = 2, row = 8)

# Waits for buttonpressed to be reset (in pick_stock_frame) before entering next frame
continue_button.wait_variable(buttonpressed)

# =============================================================================
# Third frame: Show SVR algorithm description
# =============================================================================
alg_desc_frame = Frame(root)
alg_desc_frame.pack()

# "THE SVR ALGORITHM" text
alg_label = Label(alg_desc_frame, text = "THE SVR ALGORITHM", fg = "#727070", font=("Helvetica Light", 60 , "bold"))
alg_label.grid(column = 1, row = 1, columnspan = 3)

# Display SVR description image
svr_desc_img = Label(alg_desc_frame, image = svr_img_path)
svr_desc_img.grid(column = 1, row = 2, columnspan = 3)

# When user clicks 'Continue', run continue_frame which simply changes buttonpressed for next frame
continue_alg_button = Button(alg_desc_frame, text = "Continue", padx = 6, pady = 6, command = clear_alg_desc)
continue_alg_button.grid(column = 2, row = 10)

# Waits for buttonpressed to be reset (in clear_alg_desc) before entering next frame
continue_alg_button.wait_variable(buttonpressed)

# =============================================================================
# Fourth frame: kernel choice + num days to predict
# =============================================================================
svr_params_frame = Frame(root)
svr_params_frame.pack()

# Tkinter variable for extracting radio buttons
kernel_radio_choice = IntVar()

# "SELECT A KERNEL" text
kernel_label = Label(svr_params_frame, text="SELECT A KERNEL", fg="#727070", font=("Helvetica Light", 60, "bold"))
kernel_label.grid(column=1, row=1, columnspan=3)

# Display kernel description image
kernel_desc_img = Label(svr_params_frame, image = kernel_img_path)
kernel_desc_img.grid(column = 1, row = 2, columnspan = 3)

# Show radio buttons for each of the kernels. When one is selected, change buttonpressed to continue
poly_radio = Radiobutton(svr_params_frame, variable=kernel_radio_choice, value=1, command=lambda: buttonpressed.set(0))
poly_radio.grid(column=1, row=3)
rbf_radio = Radiobutton(svr_params_frame, variable=kernel_radio_choice, value=2, command=lambda: buttonpressed.set(0))
rbf_radio.grid(column=2, row=3)
lin_radio = Radiobutton(svr_params_frame, variable=kernel_radio_choice, value=3, command=lambda: buttonpressed.set(0))
lin_radio.grid(column=3, row=3)

# This wait_variable could be attached to either of the 3 radio buttons
poly_radio.wait_variable(buttonpressed)

# "NUMBER OF DAYS TO PREDICT" text
num_days_instructions = Label(svr_params_frame, text="NUMBER OF DAYS TO PREDICT", fg="#727070", font=("Helvetica Light", 10))
num_days_instructions.grid(column=2, row=6)

# Entry for number of days to predict using algorithm
num_days_entry = Entry(svr_params_frame, width=3)
num_days_entry.grid(column = 2, row = 7)

# When user clicks 'Select', run save_kernel_choice which does as implied, then changes buttonpressed1 for next frame
select_kernel_button = Button(svr_params_frame, text="Select", padx=6, pady=6, command=save_kernel_choice)
select_kernel_button.grid(column=2, row=8)

# Waits for buttonpressed1 to be reset (in save_kernel_choice) before entering next frame
select_kernel_button.wait_variable(buttonpressed1)

# Get kernel choice and number of days to predict
num_days = int(num_days_entry.get())
kernel = save_kernel_choice()

# Destroys current frame
svr_params_frame.destroy()


# =============================================================================
# Fifth frame: Show results, predictions, then allow user to specify day
# =============================================================================
svr_results_frame = Frame(root)
svr_results_frame.pack()

# "RESULTS" text
svr_results_frame_label = Label(svr_results_frame, text="RESULTS", fg="#727070", font=("Helvetica Light", 60, "bold"))
svr_results_frame_label.grid(column=1, row=1, columnspan = 2)

# "FIT ON TO DATA" text
fit_graph_label = Label(svr_results_frame, text="FIT ON TO DATA", fg="#727070", font=("Helvetica Light", 20, "bold"))
fit_graph_label.grid(column=1, row=2)

# "PREDICTIONS FOR NEXT X DAYS" text
pred_graph_label = Label(svr_results_frame, text="PREDICTIONS FOR NEXT {} DAYS".format(num_days), fg="#727070", font=("Helvetica Light", 20, "bold"))
pred_graph_label.grid(column=2, row=2)


# Create list of number of days since the start_date of the stock data, then reshape it to a Nx1 matrix to fit to SVR algorithm)
for date in X:
    days_since_start.append((date-X[0]).days)
days_since_start = np.reshape(days_since_start, (len(days_since_start), 1))

# Get list of prices since the start_date of the stock data
close_price = stock_graph["Adj. Close"].tolist()

# Create first SVR algorithm and fit it to size of stock data
svr_fit_to_data = SVR(kernel=kernel, gamma=0.001, degree=3)
svr_fit_to_data.fit(days_since_start, close_price)

# Create list of number of days from 1-num_days, then reshape it to a Nx1 matrix to fit to SVR algorithm)
for x in range(num_days):
    prediction_days.append(x)
prediction_days = np.reshape(prediction_days, (len(prediction_days), 1))

# Get list of last X stock prices (X being num_days)
close_price_pred = close_price[-num_days:]

# Create first SVR algorithm and fit it to size of predictions
svr_predictions = SVR(kernel=kernel,gamma=0.001, degree=3)
svr_predictions.fit(prediction_days, close_price_pred)

# Display SVR fit to data
fit_to_data_plot = Figure(figsize=(3.8, 2.5))
plot_frame_2a = fit_to_data_plot.add_subplot(111)
plot_frame_2a.plot(X, svr_fit_to_data.predict(days_since_start), color= 'blue', label= 'RBF model')
plot_frame_2a.scatter(X, close_price, color='black', label='Data', s=1)
plot_frame_2a.legend()
plot_frame_2a.set_ylabel("Adj. Close ($)", fontsize=8)
plot_frame_2a.set_xlabel("Date", fontsize=8)
# autofmt_xdate() makes the x-axis rotate, tight_layout() formats the labels
fit_to_data_plot.autofmt_xdate()
fit_to_data_plot.tight_layout()

# Embedded plot into GUI
plot_frame_2a_canvas = FigureCanvasTkAgg(fit_to_data_plot, master=svr_results_frame)
plot_frame_2a_canvas.get_tk_widget().grid(column=1, row=3)
plot_frame_2a_canvas.draw()

# Predictions of stock price
predictions_plot = Figure(figsize=(3.8, 2.5))
plot_frame_2a = predictions_plot.add_subplot(111)
plot_frame_2a.plot(prediction_days, svr_predictions.predict(prediction_days), color='blue')
plot_frame_2a.set_ylabel("Adj. Close ($)", fontsize=8)
plot_frame_2a.set_xlabel("Number of Days", fontsize=8)
plot_frame_2a_canvas = FigureCanvasTkAgg(predictions_plot, master=svr_results_frame)
plot_frame_2a_canvas.get_tk_widget().grid(column=2, row=3)
plot_frame_2a_canvas.draw()
# tight_layout() formats the labels
predictions_plot.tight_layout()

# "Select a Day (1-X)" text
day_select_label = Label(svr_results_frame, text = "Select a day (1-{})".format(num_days), fg = "#727070", font=("Helvetica Light", 15 , "bold"))
day_select_label.grid(column = 1, row = 4)

# Entry for specific day to show prediction
day_select_entry = Entry(svr_results_frame, width = 3)
day_select_entry.grid(column = 1, row = 5)

# When user clicks 'Select', save prediction day and change buttonpressed for next frame
enter_day_button = Button(svr_results_frame, text="Enter", padx=6, pady=6, command=get_selected_day)
enter_day_button.grid(column=1, row=6)

# Waits for buttonpressed1 to be reset (get_selected_day) before entering next frame
enter_day_button.wait_variable(buttonpressed1)

# Get day entry
day_selected = int(get_selected_day())
# Get specific SVR prediction for the day requested (-1 to account for list index), rounded to 2 dp
day_prediction = round(svr_predictions.predict(prediction_days)[day_selected-1],2)

# Destroy day selection to make room for result
day_select_label.destroy()
day_select_entry.destroy()
enter_day_button.destroy()

# Prediction result conveyed into readable sentence
result_text = "According to the algorithm, the adjusted close price of {} will be ${} in {} days.\nBuy/Sell appropriately!".format(company_name, day_prediction, day_selected)

# Prediction result text
prediction_result_label = Label(svr_results_frame, text = result_text, fg = "#727070", font=("Helvetica Light", 20 , "bold"), wraplength = 600, justify=CENTER)
prediction_result_label.grid(column = 1, row = 4, columnspan = 2, rowspan = 3)

# When user clicks 'quit', well... quit
quit_button = Button(svr_results_frame, text="Quit", padx=6, pady=6, command=lambda: quit())
quit_button.grid(column=1, row=7, columnspan = 2)

root.mainloop()


