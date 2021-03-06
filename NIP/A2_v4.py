import pandas as pd
import Levenshtein as lev
import datetime as datetime

df = pd.read_csv("VerbBender.csv")
today = pd.to_datetime('today').normalize()
df2 =df[(df.Percent != 100) & (pd.to_datetime(df['Date']) > today)].reset_index(drop = True)

AlmostThere = []
for i in range(0,df2.shape[0]-1):
    for j in [2,4,6,8]:
        distance = lev.distance(df2.iloc[:, j][i],df2.iloc[:, j+1][i])
        ratio = lev.ratio(df2.iloc[:, j][i],df2.iloc[:, j+1][i])
        if distance ==1 and df2.C1[i] not in AlmostThere:
            AlmostThere.append(df2.C1[i])

#Read the files
verbs = pd.read_csv("verbs.csv")
df = pd.read_csv("VerbBender.csv")
df['Date'] = pd.to_datetime(df['Date'])
df2 = df[pd.to_datetime(df['Date']) > today].reset_index(drop = True)

#Select the perfect score
perfect10 =[]

for i in df2.Verb.unique():
    if max(df2.Percent[df2.Verb == i]) == 100:
        perfect10.append(i)

#Filter out verbs for training
verbs = verbs[verbs.Infinitive.isin(AlmostThere) & ~verbs['English'].isin(perfect10)].reset_index(drop = True)
AlmostThere = verbs.Infinitive

while len(AlmostThere) !=0:
    dv = 0
    bins = []
 
    print()
    verbs = verbs[verbs.Infinitive.isin(AlmostThere)]
    print(f'Todays mission is {len(verbs[verbs.Ending.notna()])} A2 verbs and {len(verbs[verbs.A2 == "Y"])} irregular verbs')
    
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
        df.loc[len(df)] = atbilde 
        df.to_csv("VerbBender.csv", index = False) 

        bins.append((1 - counter/4)*100)

#This part is broken
        if (1 - counter/4) ==100 and verbs['Infinitive'][num] in AlmostThere:
            AlmostThere.remove(verbs['Infinitive'][num])
        print(AlmostThere)
        dv +=1

        if len(AlmostThere) == 0:
            bins = pd.DataFrame(bins,columns=['bins'])
            print()
            print("Your summary:")
            print(bins.bins.value_counts())
            print(f'{(len(bins[bins.bins == 100])/len(bins)):.2f}')
                    
    


    