import pandas as pd
import Levenshtein as lev
import datetime as datetime
import datetime
import random
import sqlite3
from numpy import nan

def filing():
    connection = sqlite3.connect("norsk.db")
    cursor = connection.cursor()
    verbs = pd.read_csv("verbs.csv")
    df = pd.read_csv("VerbBender.csv")
    df = df[['Date', 'Verb', 'C1', 'Infinitive', 'C2', 'PresentTense', 'C3',
       'PastTense', 'C4', 'PastParticiple', 'Ending', 'Irregular', 'Percent']]
    df['Date'] = pd.to_datetime(df['Date'])
    e = random.randint(4,9)
    df = df[df.Date > datetime.datetime.now() - datetime.timedelta(days=e)]
    return df, verbs,e

def AlmostThere():
    df, verbs,e = filing()

    today = pd.to_datetime('today').normalize()
    df =df[(df['Date'] > today)].reset_index(drop = True)
    print(f'{len(df)} Todays damage, you over archiever')
    perfect10 =[]    
    for i in df.Verb.unique():
        if max(df.Percent[df.Verb == i]) == 100:
            perfect10.append(i)
    AlmostThere = []
    for i in range(0,df.shape[0]-1):
        for j in [2,4,6,8]:
            distance = lev.distance(df.iloc[:, j][i],df.iloc[:, j+1][i])
            ratio = lev.ratio(df.iloc[:, j][i],df.iloc[:, j+1][i])
            if distance <=5 and df.C1[i] not in AlmostThere:
                AlmostThere.append(df.C1[i])
    print(f'{len(AlmostThere)} almost there')
    verbs =verbs[verbs.Infinitive.isin(AlmostThere)&~verbs['English'].isin(perfect10)].reset_index(drop = True)
    if len(verbs) ==0:
        print(f'Well done, there are no AlmostThere. Take a breather and step up the challenge!')
    return df, verbs

def ThePerfect10():
    df = filing()[0]
    perfect10 =[]
    for i in df.Verb.unique():
        if max(df.Percent[df.Verb == i]) == 100:
            perfect10.append(i)
    return perfect10

def VBB():
    df, verbs,e = filing()
    perfect10 =ThePerfect10()
    verbs = verbs[((verbs['Ending'].notna()) | (verbs.Irregular == "Y")) & ~verbs['English'].isin(perfect10)].reset_index(drop = True)
    print(f'days {e}')
    print(f'Todays mission is {len(verbs[verbs.Ending.notna()])} A2 verbs and {len(verbs[verbs.Irregular == "Y"])} irregular verbs')
    return df, verbs

def VerbBender(x):
    df, verbs = x()
    dv = 0
    bins = []
    for num in range(0, len(verbs)):

        tenses = ['Infinitive','Present tense','Past tense','Past participle']

        print()
        print(f"{dv/len(verbs):.0%}")

        print(verbs['English'][num])
        
        counter = 0
        atbilde = []
        
        atbilde.append(datetime.datetime.now())
        atbilde.append(verbs['English'][num])
        
        for i in tenses:
            print(i)
            atbilde.append(verbs[i][num])

            answer= input()
            atbilde.append(answer)      

            if verbs[i][num] != answer:
                print(verbs[i][num])
                counter+= 1
        print(f"You got {(1 - counter/4):.2%}  correct")
        atbilde.append(verbs['Ending'][num])
        atbilde.append(verbs.Irregular [num])

        atbilde.append((1 - counter/4)*100)
        print(atbilde)

        #df2 = pd.read_csv("VerbBender.csv")
        #df2.loc[len(df2)] = atbilde 
        #df2.to_csv("VerbBender.csv", index = False) 
        '''pd.DataFrame(atbilde, columns = [['Date', 'Verb', 'C1', 'Infinitive', 'C2', 'PresentTense', 'C3',
       'PastTense', 'C4', 'PastParticiple', 'Ending', 'Irregular', 'Percent']])
        
        conn = sqlite3.connect('norsk.db')
        query = "SELECT * FROM verbbender;"

        df2 = pd.read_sql_query(query,conn)
        df2.loc[len(df2)] = atbilde
        df2.to_sql('VerbBender', connection, if_exists='append', index=False)'''
        
        
        conn = sqlite3.connect('norsk.db')
        print('Connected to database successfully.')

        cur = conn.cursor()
        cur.execute("insert into VerbBender(Date, 'Verb', 'C1', 'Infinitive', 'C2', 'PresentTense', 'C3','PastTense', 'C4', 'PastParticiple', 'Ending', 'Irregular', 'Percent') values(?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?,?)", atbilde)
        print('Records inserted successfully.')

        conn.commit()
        conn.close()
        
        bins.append((1 - counter/4)*100)

        dv +=1
    bins = pd.DataFrame(bins,columns=['bins'])
    print()
    if len(bins.bins) > 0:
        print("Your summary:")
        print(bins.bins.value_counts())

def Norwegian():
    VerbBender(VBB)
    VerbBender(AlmostThere)

Norwegian()