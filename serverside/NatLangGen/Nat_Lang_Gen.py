import re
from collections import defaultdict
import textwrap

###Change from Static to Arguments Later###
rek_log = './rekog.txt'
text_ex_log = './textEx.txt'

###Constants###
LABEL_SECTION = 'Label: '
PIC_TITLE = 'Detected imgData for '
END_LABEL = '----------'

###Variables###
title = ""
summary = ""
global imgData
imgData = defaultdict()
global textExtracted
textExtracted=""

def loadData(data):
    global imgData
    imgData = data


def TestData():
    global title
    title = 'coffeeText.JPG'

    imgData['Beverage']={'Confidence': 99.90109252929688, 'Parents': []}
    imgData['Cup']={'Confidence': 99.90109252929688, 'Parents': []}
    imgData['Latte']={'Confidence': 99.90109252929688, 'Parents': ['Coffee Cup','Beverage','Cup']}
    imgData['Drink']={'Confidence': 99.90109252929688, 'Parents': []}
    imgData['Coffee Cup']={'Confidence': 99.90109252929688, 'Parents': ['Cup']}
    imgData['Milk']={'Confidence': 89.26606750488281, 'Parents': ['Beverage']}

    global textExtracted
    textExtracted="I\nIT'S\nMONDAY\nbut keep\nSmiling\nino"

def GenerateSummary():
    global summary

    finalimgData = defaultdict()
    for label in imgData:
        parents = imgData[label]['Parents']
        par_str = ""
        if(len(parents)>0):
            for ind,parent in enumerate(parents):
                #if finalimgData[parent]:
                par_str+=parent
                if ind+1 < len(parents):
                    if ind+2 == len(parents):
                        par_str+=', and/or '
                    else:
                        par_str+= ', '
            finalimgData[label] = par_str
            ch = label[0]
            if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
                prefix='an'
            else:
                prefix='a'
            
            if(imgData[label]['Confidence']<90):
                summary += 'The '+finalimgData[label]+' in the picture is not confirmed, but may be described as '+prefix + ' ' + label+'. '
            else:
                summary += 'The '+finalimgData[label]+' in the picture can be described as '+prefix + ' ' + label+'. '

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
    return title,summary

def RunFull(data):
    loadData(data)
    GenerateSummary()
    PrettyPrint()
    return title,summary