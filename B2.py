# cd '/Users/Edite/Documents/GitHub/Norsk'
# python a2.py

import pandas as pd
import datetime as datetime
import datetime
import random
import sqlite3
from numpy import nan
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

conn = sqlite3.connect('/Users/Edite/Documents/GitHub/Norsk/norsk.db')

def filing():
    #conn = sqlite3.connect('/Users/Edite/Documents/GitHub/Norsk/norsk.db')
    query = "SELECT * FROM verbs where Ending is not null or Irregular = 'Y';"
    verbs = pd.read_sql_query(query,conn)
    query2 = "SELECT * FROM verbbender;"
    df = pd.read_sql_query(query2,conn)
    df['Date'] = pd.to_datetime(df['Date'])
    e = random.randint(4,14)
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
    verbs = verbs[~verbs['English'].isin(perfect10)].reset_index(drop = True)
    print(f'Todays mission is {len(verbs[verbs.Ending.notna()])} A2 verbs and {len(verbs[verbs.Irregular == "Y"])} irregular verbs')
    return df, verbs

def VerbBender():
    #print(f"{Fore.GREEN}{Back.YELLOW}{Style.BRIGHT}Red Text")
    df, verbs = VBB()
    number = len(verbs)
    chance = 10
    bins = []

    while number > 0 and chance > 0:   
        print(number)
        num = random.randint(0, number-1)
        tenses = ['Infinitive','PresentTense','PastTense','PastParticiple']
        print()
        print(f"{Fore.GREEN}{Back.YELLOW}{Style.BRIGHT}{verbs['English'][num]}")

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
                print(f"{Fore.GREEN}{Back.RED}{Style.BRIGHT}{verbs[i][num]}")
                counter+= 1   
        print(f'__________________________{(1 - counter/4):.2%}__________________________')
        atbilde.append(verbs['Ending'][num])
        atbilde.append(verbs.Irregular [num])
        atbilde.append((1 - counter/4)*100)
        conn = sqlite3.connect('/Users/Edite/Documents/GitHub/Norsk/norsk.db')
        cur = conn.cursor()
        cur.execute("insert into VerbBender(Date, 'Verb', 'C1', 'Infinitive', 'C2', 'PresentTense', 'C3','PastTense', 'C4', 'PastParticiple', 'Ending', 'Irregular', 'Percent') values(?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?,?)", atbilde)
        conn.commit()
        conn.close()
        score = (1 - counter/4)*100.0
        bins.append(score)

        if score == 100.0:
            verbs = verbs.drop(num).reset_index(drop = True)
            number -= 1
        if score != 100.0:
            chance-=1
            print(f'You have {chance} tries left')
            
    conn = sqlite3.connect('/Users/Edite/Documents/GitHub/Norsk/norsk.db')
    query2 = "SELECT * FROM verbbender;"
    df = pd.read_sql_query(query2,conn)
    df['Date'] = pd.to_datetime(df['Date'])

    today = pd.to_datetime('today').normalize()
    df =df[(df['Date'] > today)].reset_index(drop = True)
    print(f'{today:%d/%m/%Y}')
    print(f'Todays precision is: {len(df[df.Percent== 100.0])/len(df):.0%}')
    print("Your summary:")
    print(df.Percent.value_counts())     