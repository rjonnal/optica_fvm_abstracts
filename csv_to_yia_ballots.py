import pandas as pd
import sys
import config as cfg

input_filename = sys.argv[1]

df = pd.read_csv(input_filename)

for idx,row in df.iterrows():
    if row['Is the presenting author eligible for the Young Investigator Award?'].find('Yes')>-1:
        print('## Optica Fall Vision Meeting YIA Scoring Sheet')
        print()
        print('Please use a scale of 1 - 5 where **1 is the highest score** and **5 is the lowest score**.\n\n**Use the entire scoring range, please!**')
        print()
        print()
        print('**Score (circle):\hspace{0.5in}1\hspace{0.5in}2\hspace{0.5in}3\hspace{0.5in}4\hspace{0.5in}5**')
        print()
        print()
        print('**Scorer initials:**')
        print()
        print()
        print('Author: %s, %s'%(row['surname1'],row['given-names1']))
        print()
        print('Session: %s'%(cfg.sessions[row['Session']]))
        print()
        print('Email: %s'%row['Email Address'])
        print()
        print('Institution: %s'%row['aff1'])
        print()
        print('Title: %s'%row['article-title'])
        print()
        print('Abstract: %s'%row['abstract'])
        print()
        print('Funding: %s'%row['fn-group'])
        print()
        print('\\newpage')