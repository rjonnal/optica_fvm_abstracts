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


        # This is where we would implement some fuzzy matching to collapse multiple
        # instances of the same institution into a single instance, to provide consistency
        # among the abstracts.
        if True:
            all_affiliations = []
            for k in self.dictionary.keys():
                all_affiliations = all_affiliations+self.dictionary[k]
            all_affiliations = list(set(all_affiliations))
            similarities = []
            n_affil = len(all_affiliations)
            replacements = {}
            for aff1_idx in range(n_affil):
                for aff2_idx in range(aff1_idx+1,n_affil):
                    aff1 = all_affiliations[aff1_idx]
                    aff2 = all_affiliations[aff2_idx]
                    if not aff1==aff2:
                        sim = similarity(aff1.lower(),aff2.lower())
                        if sim>0.95:
                            print('Replacing\n%s\nwith\n%s\nin affiliations.'%(aff2,aff1))
                            replacements[aff2] = aff1
                        similarities.append(sim)
            #plt.hist(similarities,100)
            #plt.show()
            for k in self.dictionary.keys():
                temp = []
                for item in self.dictionary[k]:
                    if item in replacements.keys():
                        temp.append(replacements[item])
                    else:
                        temp.append(item)
                self.dictionary[k] = temp

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
    
