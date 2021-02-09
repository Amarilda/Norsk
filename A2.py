import pandas as pd
import Levenshtein as lev
import datetime as datetime
import datetime
import random
import sqlite3
from numpy import nan

def filing():
    conn = sqlite3.connect('norsk.db')
    query = "SELECT * FROM verbs;"
    verbs = pd.read_sql_query(query,conn)
    query2 = "SELECT * FROM verbbender;"
    df = pd.read_sql_query(query2,conn)
    df['Date'] = pd.to_datetime(df['Date'])
    e = random.randint(1,9)
    df = df[df.Date > datetime.datetime.now() - datetime.timedelta(days=e)]
    return df, verbs,e

def ThePerfect10():
    df = filing()[0]
    perfect10 =[]
    for i in df.Verb.unique():
        if float(max(df.Percent[df.Verb == i])) == 100.0:
            perfect10.append(i)
    return perfect10

def VBB():
    df, verbs,e = filing()
    perfect10 =ThePerfect10()
    verbs = verbs[((verbs['Ending'].notna()) | (verbs.Irregular == "Y")) & ~verbs['English'].isin(perfect10)].reset_index(drop = True)
    print(f'days {e}')
    print(f'Todays mission is {len(verbs[verbs.Ending.notna()])} A2 verbs and {len(verbs[verbs.Irregular == "Y"])} irregular verbs')
    return df, verbs

df, verbs = VBB()
number = len(verbs)

while number > 0:   
    print(number)
    
    bins = []

    num = random.randint(0, number-1)
    print(f'this is random number {num}')

    tenses = ['Infinitive','PresentTense','PastTense','PastParticiple']
    print()
    print(f"{1/len(verbs):.0%}")
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
    conn = sqlite3.connect('norsk.db')
    cur = conn.cursor()
    cur.execute("insert into VerbBender(Date, 'Verb', 'C1', 'Infinitive', 'C2', 'PresentTense', 'C3','PastTense', 'C4', 'PastParticiple', 'Ending', 'Irregular', 'Percent') values(?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?,?)", atbilde)
    conn.commit()
    conn.close()
    bins.append((1 - counter/4)*100.0)

    if ((1 - counter/4)*100) == 100.0:
        verbs = verbs.drop(num).reset_index(drop = True)
        number -= 1