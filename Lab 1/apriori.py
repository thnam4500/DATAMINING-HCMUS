import pandas as pd
import numpy as np
from itertools import combinations
from collections import OrderedDict

df = pd.read_csv('churn.txt')
changes_col = { 'Day Mins':[75,275],
            'Eve Mins':[100,300],
            'Night Mins':[100,325],
            'Intl Mins':[5,16],
            'Day Calls':[60,125],
            'Eve Calls':[60,125],
            'Night Calls':[60,125],
            'Intl Calls':[2,10],
            'Account Length':[50,175],
            'VMail Message':[0,20],
            'CustServ Calls':[0,4]
            }

temp = df.copy()
for key,range_medium in changes_col.items():

    transactions = df[key]<range_medium[0]
    temp.loc[transactions, key] = 'low'

    transactions = df[key]>range_medium[1]
    temp.loc[transactions, key] = 'high'

    transactions = (df[key]<=range_medium[1]) & (df[key]>=range_medium[0])
    temp.loc[transactions, key] = 'medium'
df = temp

min_confidence = 0.8
min_supp = 0.8
cols = list(df.columns)
cols.remove("Day Charge")
cols.remove("Eve Charge")
cols.remove("Night Charge")
cols.remove("Intl Charge")
cols.remove("Phone")

def frequency(df,target_list):
    for value in target_list:
        df = df[df[value[0]]==value[1]]
    return len(df)

def combine_pre(F,target):
    positions = [x for x in range(0,len(target))]
    comb = combinations(positions,len(target)-1)
    for set_item in comb:
        list_item = [target[x] for x in set_item]
        if(list_item not in F[len(target)-1]):
            return False
    return True

def init(df):
    F1 = []
    n = len(df)
    for col in cols:
        status = list(np.unique(df[col]))
        for x in status:
            list_item = []
            if frequency(df,[[col,x]])/n>=min_supp:
                list_item = [[col,x]]
                F1.append(list_item)
    return F1

def generate_popular(df,F,size):
    n = len(F[size-1])
    if n <= 1:
        return
    F_size = []
    for i in range(n-1):
        for j in range(i+1,n):
            if(F[size-1][i][0:-1]==F[size-1][j][0:-1] and F[size-1][i][-1][0]!=F[size-1][j][-1][0]):
                candidate = F[size-1][i][:]
                candidate.append(F[size-1][j][-1])
                k = frequency(df,candidate)/len(df)
                if(combine_pre(F,candidate)==False):       # Tỉa nhánh
                    continue
                if k>=min_supp:                     # Lọc bằng min_supp
                    F_size.append(candidate)
                
    F.append(F_size)
    generate_popular(df,F,size+1)






def apriori(df):
    F = [[],init(df)]
    generate_popular(df,F,2)
    return F


F = apriori(df)

rules = []

def candidate_gen(f_k,h):
    premise = []
    consequence = []
    origin_h = h[:]
    origin_f_k=f_k[:]
    print(h)
    for i in range(len(h)):
        for j in range(i+1,len(h)):
            if h[i][:-1]==h[j][:-1]:
                temp_consequence = h[i][:]
                temp_consequence.append(h[j][-1])
        
    return premise,consequence


def ap_gen_rules(f_k,H,count_premise):
    if(len(f_k)>1 and len(H)!=0):
        premises, consequences = candidate_gen(f_k,H)
        for premise, consequence in zip(premises,consequences):
            if count_premise/frequency(df,consequence)<min_confidence:
                premises.remove(premise)
                consequences.remove(consequence)
            else:
                rules.append([premise,consequence])
        
        ap_gen_rules(f_k,consequences,count_premise)


def genRules(F):
    for i in range(2,len(F)):
        for f_k in F[i]:
            origin_f_k=f_k[:]
            f_k_count = frequency(df,f_k)
            H = []
            for i in range(len(f_k)):
                h=[]
                h.append(f_k[i])
                f_k.remove(f_k[i])
                f_pre = frequency(df,h)
                if f_k_count/f_pre>=min_confidence:  
                    rules.append([f_k,h])
                    H.append(h)
                    print(f_k_count/f_pre)
                f_k=origin_f_k[:]
            ap_gen_rules(f_k,H,f_k_count)

genRules(F)

print(rules)

