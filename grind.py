import Levenshtein as lev
import pandas as pd

df = pd.read_csv("VerbBender.csv")

today = pd.to_datetime('today').normalize()

df2 =df[(df.Percent != 100) & (pd.to_datetime(df['Date']) > today)].reset_index(drop = True)

AlmostThere =[]

for i in range(0,df2.shape[0]-1):
    for j in [2,4,6,8]:
        distance = lev.distance(df2.iloc[:, j][i],df2.iloc[:, j+1][i])
        ratio = lev.ratio(df2.iloc[:, j][i],df2.iloc[:, j+1][i])
        if distance ==1:
            print(df2.C1[i], df2.iloc[:, j][i],df2.iloc[:, j+1][i])
            AlmostThere.append(df2.C1[i])

for i in AlmostThere:
	print(i)