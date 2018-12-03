import numpy as np
import random

def output(uid):
    random.seed(5)
    #summary_exp_user2 was imported from Yodelee's Transactions API from test user two at 22:28:32, 10/21/2018
    summary_exp_user2 = {'Check Payment': 59.0,
                         'Automotive/Fuel': 880.08,
                         'Other Expenses': 3103.0,
                         'Restaurants': 160.0,
                         'Entertainment/Recreation': 808.56,
                         'Travel': 909.0,
                         'Service Charges/Fees': 180.0,
                         'Groceries': 200.0,
                         'Electronics/General Merchandise': 10444.88,
                         'Home Improvement': 20000.0,
                         'Cable/Satellite/Telecom': 1600.0}
    #summary_exp_user3 was imported from Yodelee's Transactions API from test user three at 22:31:16, 10/21/2018
    summary_exp_user3 = {'Check Payment': 59.0,
                         'Automotive/Fuel': 880.08,
                         'Other Expenses': 3103.0,
                         'Restaurants': 160.0,
                         'Entertainment/Recreation': 808.56,
                         'Travel': 909.0,
                         'Service Charges/Fees': 80.0,
                         'Electronics/General Merchandise': 10444.88,
                         'Home Improvement': 20000.0,
                         'Cable/Satellite/Telecom': 1600.0}
    final_dispinc_user4 = 7222.83
    total_salary_user4 = 24376.11
    #summary_exp_user4 was imported from Yodelee's Transactions API from test user four at 18:29:37, 10/21/2018
    summary_exp_user4 = {'Entertainment/Recreation': 1141.64,
                         'Groceries': 340.01,
                         'Pets/Pet Care': 198.76,
                         'Electronics/General Merchandise': 881.49,
                         'Home Improvement': 908.47,
                         'Cable/Satellite/Telecom': 1715.57,
                         'Services/Supplies': 693.19,
                         'Other Expenses': 870.44,
                         'Personal/Family': 1536.68,
                         'Restaurants': 719.52,
                         'Travel': 3033.01,
                         'Service Charges/Fees': 337.33}
    optimal = {'Entertainment/Recreation': 8.0,
               'Home Improvement': 6.0,
               'Cable/Satellite/Telecom': 9.0,
               'Restaurants': 4.0,
               'Travel': 15.0}
    expense_total = sum(summary_exp_user4.values())

    proportions = []
    for x in summary_exp_user4.values():
        proportions.append(x*100/expense_total)

    keys = summary_exp_user4.keys()
    percents = dict(zip(keys, proportions))

    baseline_deposit = 0.04
    deviations_from_optimal = []
    for i in optimal.keys():
        if ((percents[i] - optimal[i])/optimal[i]) > 0: #if individual is spending more than the optimal amount
            deviations_from_optimal.append((percents[i] - optimal[i])/optimal[i]) #account for percentage over optimal individual is going
    deviations = deviations_from_optimal

    deviationsdic = {}
    j = 0
    for i in optimal.keys():
        deviationsdic[i] = deviations[j]
        j += 1


    deviation = sum(deviations) #accumulation of all deviations
    deposit_final = (baseline_deposit*total_salary_user4)+(deviation*100)

    deposit_final = deposit_final//100*100
    devdic = deviationsdic

    avgs={}
    for x in devdic:
        avgs[x]=(np.mean(summary_exp_user3[x]+summary_exp_user2[x]))/2
    avgdic = avgs

    changes={}
    for x in devdic.keys():
        if devdic[x]>0.5:
            changes[x]=((avgdic[x]+summary_exp_user4[x])/2*round(random.uniform(0.9, 1.1), 10)/4)//100*100
        if devdic[x]<0.2:
            changes[x]=-1
    finadv = changes

    ret={}
    for x in finadv.keys():
        if(finadv[x]<=0):
            ret[x]=("If you mantaign you're current spending on "+ x+", you will be in good shape. Approximately average allocation to this spending category")
        else:
            ret[x]=("If you spend "+ str(finadv[x])+" less on "+ x+ " a week, you will be able to save more. Your neighbors tend to spend significantly less on this spending category")
    return [deposit_final, ret] 
    # return the (deposit, finalinfo)
