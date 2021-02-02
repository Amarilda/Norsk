import pandas as pd
import Levenshtein as lev
import datetime as datetime
import datetime
import random

def filing():
    verbs = pd.read_csv("verbs.csv")
    df = pd.read_csv("VerbBender.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    e = random.randint(1,9)
    print(f'days {e}')
    df = df[df.Date > datetime.datetime.now() - datetime.timedelta(days=e)]
    return df, verbs

def AlmostThere():
    df, verbs = filing()
    today = pd.to_datetime('today').normalize()
    df =df[(max(df.Percent) != 100) & (pd.to_datetime(df['Date']) > today)].reset_index(drop = True)
    
    AlmostThere = []
    for i in range(0,df.shape[0]-1):
        for j in [2,4,6,8]:
            distance = lev.distance(df.iloc[:, j][i],df.iloc[:, j+1][i])
            ratio = lev.ratio(df.iloc[:, j][i],df.iloc[:, j+1][i])
            if distance ==1 and df.C1[i] not in AlmostThere:
                AlmostThere.append(df.C1[i])
            if len(AlmostThere)== 0:
                print("Increase your levenstein")
    verbs =verbs[verbs.Infinitive.isin(AlmostThere)].reset_index(drop = True)
    return df, verbs

def ThePerfect10():
    df = filing()[0]
    perfect10 =[]
    for i in df.Verb.unique():
        if max(df.Percent[df.Verb == i]) == 100:
            perfect10.append(i)
    return perfect10

def VBB():
    df, verbs = filing()
    perfect10 =ThePerfect10()
    verbs = verbs[((verbs['Ending'].notna()) | (verbs.A2 == "Y")) & ~verbs['English'].isin(perfect10)].reset_index(drop = True)
    print(f'Todays mission is {len(verbs[verbs.Ending.notna()])} A2 verbs and {len(verbs[verbs.A2 == "Y"])} irregular verbs')
    return df, verbs

def VerbBender(x):
    df, verbs = x()
    dv = 0
    bins = []
    print(len(verbs))
    for num in range(0, len(verbs)):

        tenses = ['Infinitive','Present tense','Past tense','Past participle']

        print()
        print(f"{dv/len(verbs):.0%}")

        print(verbs['English'][num])
        
        if verbs['A2'][num] == "Y":
            print('Irregular Joe')
        else:
            print(verbs['Ending'][num])
        
        counter = 0
        atbilde = []
        
        atbilde.append(datetime.datetime.now())
        atbilde.append(verbs['English'][num])
        
        if verbs['A2'][num] == "Y":
            print(verbs['Infinitive'][num])
        
        for i in tenses:
            print(i)
            atbilde.append(verbs[i][num])

            answer= input()
            atbilde.append(answer)      

            if verbs[i][num] != answer:
                print(verbs[i][num])
                counter+= 1
        print(f"You got {(1 - counter/4):.2%}  correct")

        atbilde.append((1 - counter/4)*100)

        df2 = pd.read_csv("VerbBender.csv")
        df2.loc[len(df2)] = atbilde 
        df2.to_csv("VerbBender.csv", index = False) 

        bins.append((1 - counter/4)*100)

        dv +=1
    bins = pd.DataFrame(bins,columns=['bins'])
    print()
    print("Your summary:")
    print(bins.bins.value_counts())

def Norwegian():
    VerbBender(VBB)
    VerbBender(AlmostThere)

Norwegian()