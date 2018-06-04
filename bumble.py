# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:00:50 2018

@author: Fabien Gueret 4 Bumble

"""


# Dependencies

#Data management library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Statistical library
from scipy.stats import mannwhitneyu

###############################################
############ feed the beast ###################
###############################################

#### Open xl files and save data in Dataframes ####
dataset =  pd.read_excel('AB_Test_Results.xlsx',header = 2,index_col=0)
print(dataset.head())
print(dataset.describe())

##############################################
############ basic stats######################
##############################################

# Create a DataFrame with summary statistics
funcs = ["mean","std", "count","min","max"]
grouped_ds = pd.DataFrame(dataset.groupby(["VARIANT_NAME"])["REVENUE"].agg(funcs).astype(float))
print()
print(" Basic stats for dataset ")
print(grouped_ds)

# Create a DataFrame with summary statistics when Revenue is non zero
subdataset = dataset.loc[dataset["REVENUE"]>0.001]
sub_grouped_ds = pd.DataFrame(subdataset.groupby(["VARIANT_NAME"])["REVENUE"].agg(funcs).astype(float))
print()
print(" Basic stats for dataset without null revenue")
print(sub_grouped_ds)

#print(subdataset["REVENUE"].loc[subdataset["VARIANT_NAME"]="control"].values)

##############################################
############# Graphic analytics###############
##############################################

# Create histogram chart to visualise Revenue distribution excluding the null occurences 
colours = ['red','lime']
labels = [ 'control', 'variant']
n_bins = 25
x_cv = [subdataset["REVENUE"].loc[subdataset["VARIANT_NAME"]=="control"].values, 
subdataset["REVENUE"].loc[subdataset["VARIANT_NAME"]=="variant"].values]

plt.figure(num=1,figsize=(10,6))
plt.hist(x_cv,bins=n_bins,range=[0,200],  color=colours, label=labels, histtype='bar')
plt.xlabel("REVENUE")
plt.ylabel("Density")
plt.axis([0, 200, 0, 100])
plt.title('A/B Distribution non null')
plt.legend()
plt.show()

#############################
#######  Outliers ###########
#############################

# Rid of 99% outliers - 2.33 * stdev normal assumption
mean = sub_grouped_ds["mean"].values
std = sub_grouped_ds["std"].values
outliers_upper_limit = mean + 2.33 * std
print()
print("99% * Stdev * Normal Percentile")
print("control   variant")
print(outliers_upper_limit)

clean_ds = dataset.query('(VARIANT_NAME == "control" and REVENUE < ' + str( outliers_upper_limit[0])
                              +') or ( VARIANT_NAME == "variant" and REVENUE < ' +  str( outliers_upper_limit[0])+')' )

# Create a DataFrame with summary statistics
funcs = ["mean","std", "count","min","max"]
c_grouped_ds = pd.DataFrame(clean_ds.groupby(["VARIANT_NAME"])["REVENUE"].agg(funcs).astype(float))
print()
print(" Basic stats for dataset without outliers")
print(c_grouped_ds)

# Create a DataFrame with summary statistics when Revenue is non zero
sub_clean_ds = clean_ds.loc[clean_ds["REVENUE"]>0.001]
c_sub_grouped_ds = pd.DataFrame(sub_clean_ds.groupby(["VARIANT_NAME"])["REVENUE"].agg(funcs).astype(float))
print()
print(" Basic stats for dataset without outliers and non null revenue")
print(c_sub_grouped_ds)

# Create histogram chart to visualise Revenue distribution excluding the null occurences and outliers
colours = ['red','lime']
labels = [ 'control', 'variant']
n_bins = 25
c_x_cv = [sub_clean_ds["REVENUE"].loc[sub_clean_ds["VARIANT_NAME"]=="control"].values, 
        sub_clean_ds["REVENUE"].loc[sub_clean_ds["VARIANT_NAME"]=="variant"].values]

plt.figure(num=2,figsize=(10,6))
plt.hist(c_x_cv,bins=n_bins,range=[0,200],  color=colours, label=labels, histtype='bar')
plt.xlabel("REVENUE")
plt.ylabel("Density")
plt.axis([0, 75, 0, 100])
plt.title('A/B Distribution non null no 99% outliers')
plt.legend()
plt.show()

########################################
###### A/B Testing on Revenue###########
########################################

# Mann Whitney Wilcoxon

#full dataset
c = dataset["REVENUE"].loc[dataset["VARIANT_NAME"]=="control"].values
v = dataset["REVENUE"].loc[dataset["VARIANT_NAME"]=="variant"].values
stat, pvalue = mannwhitneyu(c, v, use_continuity=True, alternative="less")
print()
print("Mann Whitnet Wilcoxon")
print("Full DataSet")
print("U Statistic      p-Value")
print(stat, pvalue)

#non null dataset
c = subdataset["REVENUE"].loc[subdataset["VARIANT_NAME"]=="control"].values
v = subdataset["REVENUE"].loc[subdataset["VARIANT_NAME"]=="variant"].values
stat, pvalue = mannwhitneyu(c, v, use_continuity=True, alternative="less")
print()
print("Mann Whitnet Wilcoxon")
print("DataSet non null revenue")
print("U Statistic      p-Value")
print(stat, pvalue)

#full dataset excluding outliers
c = clean_ds["REVENUE"].loc[clean_ds["VARIANT_NAME"]=="control"].values
v = clean_ds["REVENUE"].loc[clean_ds["VARIANT_NAME"]=="variant"].values
stat, pvalue = mannwhitneyu(c, v, use_continuity=True, alternative="less")
print()
print("Mann Whitnet Wilcoxon")
print("Full DataSet excluding outliers")
print("U Statistic      p-Value")
print(stat, pvalue)

#non null dataset excluding outliers
c = sub_clean_ds["REVENUE"].loc[sub_clean_ds["VARIANT_NAME"]=="control"].values
v = sub_clean_ds["REVENUE"].loc[sub_clean_ds["VARIANT_NAME"]=="variant"].values
stat, pvalue = mannwhitneyu(c, v, use_continuity=True, alternative="less")
print()
print("Mann Whitnet Wilcoxon")
print("DataSet non null revenue excluding outliers")
print("U Statistic      p-Value")
print(stat, pvalue)




