import re
from collections import defaultdict
import textwrap

###Change from Static to Arguments Later###
rek_log = './rekog.txt'
text_ex_log = './textEx.txt'

###Constants###
LABEL_SECTION = 'Label: '
PIC_TITLE = 'Detected labels for '
END_LABEL = '----------'

###Variables###
title = ""
summary = ""
labels = defaultdict()
global textExtracted
textExtracted=""

def parseRekLog():
    with open(rek_log, "r") as f:
        in_label = False
        titled = False
        newLabel = ""
        log_string = f.readlines()
        for index,line in enumerate(log_string):
            if(titled == False):
                match = re.search(PIC_TITLE, line)
                if match:
                    titled=True
                    title = line.split(PIC_TITLE)[-1]
            else:
                if(in_label == False):
                    match = re.search(LABEL_SECTION, line)
                    if match:
                        newLabel = line.split(LABEL_SECTION)[-1].split('\n')[0]
                        print('NEW LABEL: ',newLabel)
                        in_label = True
                        labels[newLabel] = dict()
                else:
                    match = re.search(END_LABEL, line)
                    if match:
                        in_label = False
                        newLabel = ""
                        continue
                    newVal = line.split(':')
                    if (newVal[0] == 'Confidence'):
                        labels[newLabel][newVal[0]] = float(newVal[1])
                    elif (newVal[0] == 'Parents'):
                        labels[newLabel][newVal[0]] = []
                        j = 1
                        future_line = log_string[index+j]
                        match = re.search(END_LABEL,future_line)
                        while(match == False):
                            print('added', log_string[index+j])
                            labels[newLabel][newVal[0]].append(log_string[index+j])
                            j+=1
                            match = re.search(END_LABEL,log_string[index+j])
    
    print(title,':',labels)

def TestData():
    global title
    title = 'coffeeText.JPG'

    labels['Beverage']={'Confidence': 99.90109252929688, 'Parents': []}
    labels['Cup']={'Confidence': 99.90109252929688, 'Parents': []}
    labels['Latte']={'Confidence': 99.90109252929688, 'Parents': ['Coffee Cup','Beverage','Cup']}
    labels['Drink']={'Confidence': 99.90109252929688, 'Parents': []}
    labels['Coffee Cup']={'Confidence': 99.90109252929688, 'Parents': ['Cup']}
    labels['Milk']={'Confidence': 89.26606750488281, 'Parents': ['Beverage']}

    global textExtracted
    textExtracted="I\nIT'S\nMONDAY\nbut keep\nSmiling\nino"

def GenerateSummary():
    global summary

    finalLabels = defaultdict()
    for label in labels:
        parents = labels[label]['Parents']
        par_str = ""
        if(len(parents)>0):
            for ind,parent in enumerate(parents):
                #if finalLabels[parent]:
                par_str+=parent
                if ind+1 < len(parents):
                    if ind+2 == len(parents):
                        par_str+=', and/or '
                    else:
                        par_str+= ', '
            finalLabels[label] = par_str
            ch = label[0]
            if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
                prefix='an'
            else:
                prefix='a'
            
            if(labels[label]['Confidence']<90):
                summary += 'The '+finalLabels[label]+' in the picture is not confirmed, but may be described as '+prefix + ' ' + label+'. '
            else:
                summary += 'The '+finalLabels[label]+' in the picture can be described as '+prefix + ' ' + label+'. '

    if textExtracted:
        text_str = ', '.join(textExtracted.split('\n'))
        summary += 'The image has text, which says, \"' + text_str + '\".'

def PrettyPrint():
    print('\n\n\n\nA Summary for the Image '+title+'\n')
    w = 50
    print(textwrap.fill(summary,w))
    print('')

def RunTest():
    TestData()
    GenerateSummary()
    PrettyPrint()

def RunFullTest():
    parseRekLog()
    GenerateSummary()
    PrettyPrint()

RunTest()