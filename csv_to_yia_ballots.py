import pandas as pd
import sys
import config as cfg


try:
    session_df = pd.read_csv('sessions.csv')
    session_dict = {}
    for idx,row in session_df.iterrows():
        number = row['number']
        day = row['day']
        time = row['time']
        f = row['type']
        session_dict[number] = '%s session, %s at %s'%(f,day,time)
    
except Exception as e:
    sys.exit('Need a sessions.csv file.')

input_filename = sys.argv[1]

df = pd.read_csv(input_filename)

yia_df = []

for idx,row in df.iterrows():
    if row['Is the presenting author eligible for the Young Investigator Award?'].find('Yes')>-1:


        yia_df.append([row['surname1'],row['given-names1'],row['article-title']])
        
        coauthors = []
        for k in range(2,cfg.max_authors+1):
            gn = row['given-names%d'%k]
            sn = row['surname%d'%k]
            if not pd.isna(gn) and not pd.isna(sn):
                coauthors.append('%s %s'%(gn,sn))

        coauthor_string = ';'.join(coauthors)

        
        session = row['Session']
        
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
        print('Session: **%s**'%session_dict[session])
        print()
        print('Author: %s, %s'%(row['surname1'],row['given-names1']))
        print()
        print('Coauthors: %s'%(';'.join(coauthors)))
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

yia_df = pd.DataFrame(yia_df,columns=['surname','given-names','title'])
yia_df.to_csv('yia_abstracts.csv')
