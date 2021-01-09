import pandas as pd
from datetime import datetime
import random
import requests

verbs = pd.read_excel("verbs.xlsx")
df = pd.read_excel("VerbBender.xlsx")

#Filter out A2 level verbs
#verbs = verbs[(verbs[14].notna())| (verbs.A2 == "Y")].reset_index(drop = True)
verbs = verbs[(verbs[14].notna())].reset_index(drop = True)

def VerbBender():
    
    for num in range(0, len(verbs)):

        tenses = ['Infinitive','Present tense','Past tense','Past participle']
        print(verbs['English'][num])
        print(verbs[14][num])

        counter = 0
        atbilde = []
        
        atbilde.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
        atbilde.append(verbs['English'][num])
        
        for i in tenses:
            print(i)
            answer= input()
            atbilde.append(answer)

            if verbs[i][num] != answer:
                print(verbs[i][num])
                counter+= 1
        print("You got "+str((1 - counter/4)*100)+"% correct")
        atbilde.append((1 - counter/4)*100)
        df.loc[len(df)] = atbilde
        df.to_excel("VerbBender.xlsx", index = False)  
        
# You think you have a free will? 
VerbBender()