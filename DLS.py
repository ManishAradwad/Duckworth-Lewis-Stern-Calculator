# Data Analytics Assignment 1
# Author: Manish Aradwad / 19494 / MTech AI

from scipy import optimize
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def DLS():
    x0 = 250 * np.ones(11)
    x0[10] = 0.1
    result = optimize.minimize(fun = error_func, x0 = x0, args = (data))
    Z = result.x[:10]
    L = result.x[10]
    errors = np.zeros(10)

    for w in range(1,11):
        temp = data[data['Wickets.in.Hand'] == w]
        overs_rem = 50 - temp['Over']
        runs = temp['Innings.Total.Runs'] - temp['Total.Runs']
        pred_runs = Z[w-1] * np.subtract(1, np.exp(np.multiply(-L/Z[w-1], overs_rem)))
        errors[w-1] = np.sqrt(np.sum(np.square(np.subtract(runs, pred_runs))) / len(data))

    return Z, L, errors

def error_func(Z, data):
    L=Z[10]
    error=0

    for w in range(1,11):
        temp = data[data['Wickets.in.Hand'] == w]
        overs_rem = 50 - temp['Over']
        runs = temp['Innings.Total.Runs'] - temp['Total.Runs']
        pred_runs = Z[w-1] * np.subtract(1, np.exp(np.multiply(-L/Z[w-1], overs_rem)))
        error += np.sqrt(np.sum(np.square(np.subtract(runs, pred_runs))) / len(data))
    
    return error

def func(Z, L, w, u):
  return Z[w-1] * (1 - np.exp(-L*u/Z[w-1]))

def display(Z, L):
    for w in range(1, 11):
        x = range(0, 51)
        y = np.array([func(Z, L, w, u) for u in range(0, 51)])

        plt.plot(x, y, label=str(w))
        plt.text(x[-5],y[-5],w)
        plt.xlabel("Overs Remaining")
        plt.ylabel("Runs")
    
    plt.show()

if __name__ == "__main__":

    data = pd.read_csv('./04_cricket_1999to2011.csv')
    data = data[data['Innings']==1]

    # Data Preprocessing required for Total.Runs column
    for i in tqdm(range(len(data))):
        if data.iloc[i]['Over'] == 1:
            data.iloc[i]['Total.Runs'] = data.iloc[i]['Runs']
        else:
            data.iloc[i]['Total.Runs'] = data.iloc[i]['Runs'] + data.iloc[i-1]['Total.Runs']

    data = data[['Over', 'Total.Runs', 'Innings.Total.Runs', 'Wickets.in.Hand']] # Getting the required columns

    Z0, L, errors = DLS()
    display(Z0, L)

    print('Z0\t\tL\t\terrors\n')
    for i in range(10):
        print(f'{Z0[i]:.2f}\t\t{L:.5f}\t{errors[i]:.2f}')

    # Getting the score using DLS for given resources remaining
    wkt = 7
    overs = 25
    print(f"\nTarget when {wkt} wickets in hand and {overs} overs remaining are: {int(np.ceil(func(Z0, L, wkt, overs)))}\n")