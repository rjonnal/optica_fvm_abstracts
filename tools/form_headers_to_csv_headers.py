input_fields = ['category',
'Day',
'session',
'Order',
'Timestamp',
'Email Address',
'First author: Surname',
'First author: Given name(s)',
'First author: Institutional affiliation',
'Abstract Title (120 character limit)',
'Abstract Text (1500 character limit)',
'Funding Acknowledgements',
'Presentation Preference',
'Is the presenting author eligible for the Young Investigator Award?',
'Author 2: Surname',
'Author 2: Given name(s)',
'Author 2: Institutional affiliation',
'Author 3: Surname',
'Author 3: Given name(s)',
'Author 3: Institutional affiliation',
'Author 4: Surname',
'Author 4: Given name(s)',
'Author 4: Institutional affiliation',
'Author 5: Surname',
'Author 5: Given name(s)',
'Author 5: Institutional affiliation',
'Do you have additional authors to add?',
'Author 6: Surname',
'Author 6: Given name(s)',
'Author 6: Institutional affiliation',
'Author 7: Surname',
'Author 7: Given name(s)',
'Author 7: Institutional affiliation',
'Author 8: Surname',
'Author 8: Given name(s)',
'Author 8: Institutional affiliation',
'Author 9: Surname',
'Author 9: Given name(s)',
'Author 9: Institutional affiliation',
'Author 10: Surname',
'Author 10: Given name(s)',
'Author 10: Institutional affiliation',
'Do you have additional authors to add?.1',
'Author 11: Surname',
'Author 11: Given name(s)',
'Author 11: Institutional affiliation',
'Author 12: Surname',
'Author 12: Given name(s)',
'Author 12: Institutional affiliation',
'Author 13: Surname',
'Author 13: Given name(s)',
'Author 13: Institutional affiliation',
'Author 14: Surname',
'Author 14: Given name(s)',
'Author 14: Institutional affiliation',
'Author 15: Surname',
'Author 15: Given name(s)',
'Author 15: Institutional affiliation']

output_fields = []

for item in input_fields:
    if item.find('Abstract Title')>-1:
        output = 'article-title'
    elif item.find('Abstract Text')>-1:
        output = 'abstract'
    elif item.lower().find('author')>-1:
        if item[:5]=='First':
            author_index = 1
        elif item[:6]=='Author':
            index_string = item[7:item.find(':')]
            author_index = int(index_string)
        if item.find('Given name(s)')>-1:
            output = 'given-names%d'%author_index
        elif item.find('Surname')>-1:
            output = 'surname%d'%author_index
        elif item.find('Institutional affiliation')>-1:
            output = 'aff%d'%author_index
        else:
            output = item
    else:
        output = item

    output_fields.append(output)

for a,b in zip(input_fields,output_fields):
    print("'%s':'%s',"%(a,b))
