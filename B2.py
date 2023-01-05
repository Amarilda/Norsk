import pandas as pd
import datetime as datetime
import datetime
import random
import sqlite3
from numpy import nan
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

conn = sqlite3.connect('norsk.db')

def bad_df():
    connection = sqlite3.connect('norsk.db')

    cursor = connection.cursor()
    sql = ('''
        with 
        B2 as (
                select * from verbs
                where verbs.Ending is not null or verbs.Irregular = "Y" 
        ),
        verb_bender as (select Verb, max(Date) last_date
                        from VerbBender
                        group by 1
                        ),
        imperfect as (
                select Verb, count(*) as total_count
                , sum(case when percent !=100 then 1 else 0 end) incorrect
                from VerbBender
                where VerbBender.Date > date('now', '-45 day')
                group by 1
        )

        select B2.*, last_date from B2

        left join verb_bender
        on B2.English = verb_bender.Verb

        where 
        last_date  < date('now', '-30 day') 
        or 
        English in (select Verb from imperfect where round(cast(incorrect as float)/total_count*100,2) > 59 )

        order by 8 desc
                ''')
    verbs = pd.read_sql_query(sql,connection)
    print(f'Todays mission is {len(verbs[verbs.Ending.notna()])} A2 verbs and {len(verbs[verbs.Irregular == "Y"])} irregular verbs')
    return verbs


def VerbBender():
    verbs = bad_df()
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
        conn = sqlite3.connect('norsk.db')
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
            
    conn = sqlite3.connect('norsk.db')
    query2 = "SELECT * FROM verbbender;"
    df = pd.read_sql_query(query2,conn)
    df['Date'] = pd.to_datetime(df['Date'])

    today = pd.to_datetime('today').normalize()
    df =df[(df['Date'] > today)].reset_index(drop = True)
    print(f'{today:%d/%m/%Y}')
    print(f'Todays precision is: {len(df[df.Percent== 100.0])/len(df):.0%}')
    print("Your summary:")
    print(df.Percent.value_counts())     