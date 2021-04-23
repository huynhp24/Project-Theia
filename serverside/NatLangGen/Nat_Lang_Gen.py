import re
from collections import defaultdict
import textwrap

###Constants###
LABEL_SECTION = 'Label: '
PIC_TITLE = 'Detected labels for '
END_LABEL = '----------'

###Variables###

def LoadData(impLabels,text):
    '''
    labels['Beverage']={'Confidence': 99.90109252929688, 'Parents': []}
    labels['Cup']={'Confidence': 99.90109252929688, 'Parents': []}
    labels['Latte']={'Confidence': 99.90109252929688, 'Parents': ['Coffee Cup','Beverage','Cup']}
    labels['Drink']={'Confidence': 99.90109252929688, 'Parents': []}
    labels['Coffee Cup']={'Confidence': 99.90109252929688, 'Parents': ['Cup']}
    labels['Milk']={'Confidence': 89.26606750488281, 'Parents': ['Beverage']}
    '''
    print(impLabels)
    labels=defaultdict()
    textExtracted=" "
    for label in impLabels['Labels']:
        parents=[]
        if(len(label['Parents'])>0):
            for parent in label['Parents']:
                parents.append(parent['Name'])
        labels[label['Name']]={'Confidence': label['Confidence'], 'Parents': parents}
    print(text)
    for reading in text['TextDetections']:
        if('ParentId' not in reading):
            textExtracted+=reading["DetectedText"] + " "
    textExtracted=textExtracted[1:-1] 
    return labels, textExtracted

def GenerateSummary(labels,textExtracted):
    summary=""
    finalLabels = defaultdict()
    for label in labels:
        parents = labels[label]['Parents']
        par_str = ""
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='an'
        else:
            prefix='a'
            
        if(len(parents)>0):
            for ind,parent in enumerate(parents):
                par_str+=parent
                if ind+1 < len(parents):
                    if ind+2 == len(parents):
                        par_str+=', and/or '
                    else:
                        par_str+= ', '
            finalLabels[label] = par_str
            if(labels[label]['Confidence']<90):
                summary += 'The '+finalLabels[label]+' might be '+prefix + ' ' + label+'. '
            else:
                summary += 'The '+finalLabels[label]+' is '+prefix + ' ' + label+'. '
        else:
            summary += 'The image contains '+ prefix +' ' + label+'. '
    if textExtracted:
        text_str = ', '.join(textExtracted.split('\n'))
        summary += 'The image has text, which says, \"' + text_str + '\".'
    return summary

def PrettyPrint(summary):
    print('\n\n\n\nA Summary for the Image :\n')
    w = 50
    print(textwrap.fill(summary,w))
    print('')

def Run(impLabels,text):
    lab, ext = LoadData(impLabels,text)
    summary = GenerateSummary(lab,ext)
    PrettyPrint(summary)
