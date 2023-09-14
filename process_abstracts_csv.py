import pandas as pd
import config as cfg
import jov_templates as jovt
from difflib import SequenceMatcher
from xml.etree import ElementTree as ET
import os,sys
import numpy as np
from matplotlib import pyplot as plt

def similarity(s1,s2):
    """See https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher"""
    return SequenceMatcher(None,s1,s2).ratio()

def reduce_list(L,threshold=0.9,interactive=True):
    """Check to see if items in list are near-duplicates and replace one with the other."""
    N = len(L)
    L_new = []
    for idx1 in range(N):
        item1 = L[idx1]
        new_item = item1
        for idx2 in range(idx1+1,N):
            item2 = L[idx2]
            if item1==item2:
                continue
            sim = similarity(item1,item2)
            if sim>=threshold:
                if interactive:
                    print('1:%s'%item1)
                    print('2:%s'%item2)
                    response = int(input('Enter 0 to keep distinct items and 1 or 2 to if item 1 or item 2 are the correct replacement for the other: '))
                    if response==0:
                        new_item = item1
                    elif response==1:
                        new_item = item1
                    elif response==2:
                        new_item = item2
                    else:
                        sys.exit('Invalid response.')
                else:
                    new_item = item2
        L_new.append(new_item)
    assert len(L)==len(L_new)
    return L_new

def cleanup(s):
    rem = ['M.D.','Ph.D.','M.S.','O.D.','D.O.','D.Phil.','M.Phil.',',']
    for r in rem:
        s = s.replace(r,'')
        s = s.replace(r.replace('.',''),'')
    return s

def special_chars(text):
    text = text.replace('&','&amp')
    d = {}
    d['<'] = '&lt;'
    d['>'] = '&gt;'
    d["'"] = '&#39;'
    d["\""] = '&#34;'
    for c in d.keys():
        text = text.replace(c,d[c])
    return text

def checkna(dat):
    if pd.isna(dat):
        return ''
    else:
        return str(dat)

def xml_valid(s):
    try:
        x = ET.fromstring(s)
        return True
    except Exception as e:
        print('Invalid XML.')
        print(e)
        for idx,line in enumerate(s.split('\n')):
            print('%04d:%s'%(idx,line))
        return False

class Abstract:
    """Represents a single abstract. Has an AUTHORGROUP object, representing
    the authors and their affiliations, a STRING title, a STRING text, an INT number,
    an INT month, an INT year, an INT volume, an INT issue, an INT fpage, an INT
    lpage (the last two are equal to Abstract.number), and a STRING funding."""
    def __init__(self,pandas_series,affiliation_factory):
        self.affiliation_factory = affiliation_factory
        self.data = pandas_series
        self.title = checkna(self.data['article-title'])
        self.text = checkna(self.data['abstract'])
        self.text = special_chars(checkna(self.text))
        self.number = self.data['abstract_number']
        self.session_number = self.data['Session']
        self.session = cfg.sessions[self.session_number]
        self.funding = checkna(self.data['fn-group'])
        if len(self.funding.strip())==0:
            self.funding = 'Funding: None'
        else:
            self.funding = 'Funding: %s'%self.funding
        self.month = cfg.month
        self.year = cfg.year
        self.volume = cfg.volume
        self.issue = cfg.issue
        self.fpage = self.number
        self.lpage = self.number

        self.ag = AuthorGroup()
        for author_index in range(1,cfg.max_authors+1):
            surname = pandas_series['surname%d'%author_index]
            if pd.isna(surname):
                break
            surname = str(surname)
            if len(surname)==0:
                break
            
            given_names = str(pandas_series['given-names%d'%author_index])
            affiliation_key = pandas_series['aff%d'%author_index]
            if pd.isna(affiliation_key):
                affiliation_list = []
            else:
                affiliation_list = self.affiliation_factory.get_affiliation_list(affiliation_key)

                
            self.ag.add(surname,given_names,affiliation_list)

        doi = jovt.doi_template.replace('$ABSTRACT_NUMBER$','%d'%self.number)
        self.xml = jovt.root_template.replace('$DOI$',doi)
        self.xml = self.xml.replace('$ABSTRACT_NUMBER$','%d'%self.number)
        self.xml = self.xml.replace('$SESSION$',self.session)
        self.xml = self.xml.replace('$TITLE$',self.title)
        self.xml = self.xml.replace('$CONTRIBUTORS$',self.ag.get_contributors_xml())
        self.xml = self.xml.replace('$AFFILIATIONS$',self.ag.get_affiliations_xml())
        self.xml = self.xml.replace('$MONTH$','%d'%self.month)
        self.xml = self.xml.replace('$YEAR$','%d'%self.year)
        self.xml = self.xml.replace('$VOLUME$','%d'%self.volume)
        self.xml = self.xml.replace('$ISSUE$','%d'%self.issue)
        self.xml = self.xml.replace('$FPAGE$','%d'%self.fpage)
        self.xml = self.xml.replace('$LPAGE$','%d'%self.lpage)
        self.xml = self.xml.replace('$ABSTRACT$','%s'%self.text)
        self.xml = self.xml.replace('$FN_GROUP$','%s'%self.funding)
        assert self.xml.find('$')==-1
        #xml_valid(self.xml)
        
class AuthorGroup:
    """Represents a group of authors and their affiliations."""

    def __init__(self):
        self.authors = []
        self.affiliations = []
        self.links = []
        
    def add(self,surname,given_names,affiliation_list):
        author = (cleanup(surname),cleanup(given_names))
        self.authors.append(author)
        
        for affiliation in affiliation_list:
            if not affiliation in self.affiliations:
                self.affiliations.append(affiliation)
            self.links.append((author,self.affiliations.index(affiliation)))

    def __str__(self):
        out = ''
        for author in self.authors:
            out = out + '%s, %s '%(author[0],author[1])
            author_links = [str(l[1]+1) for l in self.links if l[0]==author]
            out = out + '%s'%(', '.join(author_links))
            out = out + '\n'
        for idx,affiliation in enumerate(self.affiliations):
            out = out + '%d: %s\n'%(idx+1,affiliation)
        return out
            
    def get_contributors_xml(self):
        out = ''
        for author in self.authors:
            contrib = jovt.contrib_template.replace('$SURNAME$',author[0]).replace('$GIVEN_NAME$',author[1]) + '\n'
            author_links = [str(l[1]+1) for l in self.links if l[0]==author]
            aff_block = ''
            for author_link in author_links:
                aff_block = aff_block + jovt.contrib_aff_template.replace('$AFFILIATION_NUMBER$',author_link) + '\n'
            contrib = contrib.replace('$CONTRIB_AFFS$',aff_block)
            out = out + contrib + '\n'
            
        return out+'\n'
    
    def get_affiliations_xml(self):
        # This is where we would implement some fuzzy matching to collapse multiple
        # instances of the same institution into a single instance, to provide consistency
        # among the abstracts.
        if True:
            self.affiliations = reduce_list(self.affiliations)
        out = ''
        for idx,affiliation in enumerate(self.affiliations):
            at = jovt.aff_template.replace('$AFFILIATION_NUMBER$','%d'%(idx+1))
            at = at.replace('$INSTITUTION$',affiliation)
            out = out + at + '\n'
        return out

        

class AffiliationFactory:
    """This class digests all of the affiliations in the DataFrame. It uses the
    exact text of the affiliation column as a unique key to return a list of
    affiliation objects. This behavior is motivated by the fact that some affiliation
    entries consist of multiple affiliations, and we may need to split those into two
    separate affiliations.
    IMPORTANT: This class assumes that multiple affiliations listed for a single author
    are separated by semicolons. PLEASE FIX NON-COMPLIANT ENTRIES IN THE CSV.
    """
    
    def __init__(self,pandas_dataframe):
        self.dictionary = {}
        
        for idx,row in pandas_dataframe.iterrows():
            for aff_idx in range(1,cfg.max_authors+1):
                dat = row['aff%d'%aff_idx]
                if not pd.isna(dat):
                    if len(dat)>0:
                        self.dictionary[dat] = [token.strip() for token in dat.split(';')]



    def __str__(self):
        out = ''
        for k in self.dictionary.keys():
            out = out + '%s -> %s\n'%(k,self.dictionary[k])
        return out

    def get_affiliation_list(self,key):
        return self.dictionary[key]



if __name__=='__main__':
    df = pd.read_csv('abstracts_2022.csv')
    affiliation_factory = AffiliationFactory(df)

    output_folder = cfg.output_folder
    os.makedirs(output_folder,exist_ok=True)
    
    for idx,row in df.iterrows():
        abstract = Abstract(row,affiliation_factory)
        out_fn = '%s/abstract_%03d.xml'%(output_folder,abstract.number)
        out_string = abstract.xml.strip()
    
        with open(out_fn,'w') as fid:
            fid.write(out_string)
    
