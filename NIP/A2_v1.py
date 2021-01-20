import pandas as pd
from datetime import datetime
import datetime

start = datetime.datetime.now()

def VerbBender():

#Read the files
    verbs = pd.read_excel("verbs.xlsx")
    df = pd.read_excel("VerbBender.xlsx")

    print(datetime.datetime.now()-start)

    df2 = df[df.Date > datetime.datetime.now() - datetime.timedelta(days=5)]

#Select the perfect score
    perfect10 =[]

    for i in df2.Verb.unique():
        if max(df2.Percent[df2.Verb == i]) == 100:
            perfect10.append(i)

#Filter out verbs for training
    #verbs = verbs[(verbs[14].notna())| (verbs.A2 == "Y")].reset_index(drop = True)
    verbs = verbs[((verbs[14].notna()) | (verbs.A2 == "Y")) & ~verbs['English'].isin(perfect10)].reset_index(drop = True)
    dv = 0
    bins = []
 
    print()
    print(f'Todays mission is {len(verbs[verbs[14].notna()])} A2 verbs and {len(verbs.A2 == "Y")} irregular verbs')
    
    for num in range(0, len(verbs)):

        tenses = ['Infinitive','Present tense','Past tense','Past participle']

        print()
        print(f"{dv/len(verbs):.0%}")

        print(verbs['English'][num])
        
        if verbs['A2'][num] == "Y":
            print('Irregular Joe')
        else:
            print(verbs[14][num])
        
        counter = 0
        atbilde = []
        
        atbilde.append(datetime.datetime.now())
        atbilde.append(verbs['English'][num])

        
        if verbs['A2'][num] == "Y":
            print(verbs['Infinitive'][num])
        
        for i in tenses:
            print(i)
            answer= input()
            atbilde.append(answer)

            if verbs[i][num] != answer:
                print(verbs[i][num])
                counter+= 1
        print(f"You got {(1 - counter/4):.2%}  correct")

        atbilde.append((1 - counter/4)*100)
        df.loc[len(df)] = atbilde
        df.to_excel("VerbBender.xlsx", index = False) 

        bins.append((1 - counter/4)*100)

        dv +=1
    bins = pd.DataFrame(bins,columns=['bins'])
    print()
    print("Your summary:")
    print(bins.bins.value_counts())

# You think you have a free will? 
VerbBender()