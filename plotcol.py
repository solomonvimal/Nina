#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 21:53:46 2017

@author: svimal
"""


import matplotlib.pyplot as plt
import sys, os


#f="lake_46.6875_-97.0625"

path = os.getcwd() + "//"

os.chdir(path)
def plot_variable(f, column_no, var_name):

    column_no = int(column_no)
    with open(path+f,"r") as ff:
        data = ff.readlines()
    x = []
    try:
        for line in data:
            x.append(float(line.split(" ")[column_no-1]))
        plt.plot(x);plt.xlabel("time");plt.ylabel(var_name+ " of lake (m)");plt.title(var_name + " over time");plt.savefig(var_name+"_plot.png")
        plt.show()
        plt.clf()
    except:
        for line in data:
            x.append(float(line.split("\t")[column_no-1]))
        plt.plot(x);plt.xlabel("time");plt.ylabel(var_name+ " of lake (m)");plt.title(var_name + " over time");plt.savefig(var_name+"_plot.png")
        plt.show()
        plt.clf()        

if __name__ == "__main__":
    try:
        plot_variable(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Wrong command! \nCorrect usage is: $plotcol file_name column_number variable_name")
