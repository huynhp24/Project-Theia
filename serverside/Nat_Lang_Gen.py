import re
from collections import defaultdict
import textwrap
import copy

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

'''def location_stuff(labels):
    picMap = {"left": {"top": {"labels": [], "coordinates": {"left_coordinate": 0, "right_coordinate": .33, "top_coordinate": 1, "bottom_coordinate": .67}}},
                "middle": {"labels": [], "coordinates": {"left_coordinate": 0, "right_coordinate": .33, "top_coordinate": 1, "bottom_coordinate": .67}}},
                "bottom": {"labels": [], "coordinates": {"left_coordinate": 0, "right_coordinate": .33, "top_coordinate": 1, "bottom_coordinate": .67}}}}
'''

maxLevel = 0
oldest = ""
delete_list = defaultdict()
def oldestAncestor(labels, label, level):
        global oldest
        global maxLevel
        level += 1
        print(level)
        print("looking at " + label)
        parents = labels[label]['Parents']
        if(labels[label]['Confidence']>90):
            if (level > maxLevel):
                oldest = label
                print('deepest so far is :' + label)
                maxLevel = level
            for parent in parents:
                delete_list[parent]=""
                oldestAncestor(labels, parent, level)
         
def theCollapse(labels, label) :
    print("The quest for: " + label)
    global oldest
    oldest = ""
    level = 0
    global maxLevel
    maxLevel = -1
    oldestAncestor(labels, label, level)
    return oldest

def GenerateSummary(labels,textExtracted):
    summary=""
    finalLabels = defaultdict()
    # collapse into parent

    global delete_list
    delete_list = defaultdict()

    ref_labels = copy.deepcopy(labels)
    for label in ref_labels:
        collapsed = theCollapse(ref_labels, label)
        print(label + " <---- " + collapsed)
        labels[label]['Parents']=[collapsed]
    
    for label in delete_list:
        del labels[label]

    pretty_parents = defaultdict()
    for label in labels:
        if(len(labels[label]['Parents'])>0):
            pretty_parents[labels[label]['Parents'][0]]={'Children': []}

    pretty_loners = []

    for label in labels:
        if(len(labels[label]['Parents'])>0):
            pretty_parents[labels[label]['Parents'][0]]['Children'].append(label)
        else:
            pretty_loners.append(label)

    print(labels)
    print(pretty_parents)

    for label in labels:
        par_str = ""
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            labels[label]['prefix']='an'
        else:
            labels[label]['prefix']='a'

    '''for label in labels:
        parents = labels[label]['Parents']
        prefix = labels[label]['prefix']
        if(len(parents)>0):
            par_str=""
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
            summary += 'The image contains '+ prefix +' ' + label+'. '''
    for label in pretty_parents:
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='an'
        else:
            prefix='a'

        kids=' or '.join(pretty_parents[label]['Children'])

        summary+= "There is "+ prefix +" " + label+ " in the image. Some description of the " + label + ": " + kids+ ". "

    for label in pretty_loners:
        ch = pretty_loners[label][0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='an'
        else:
            prefix='a'
        
        pretty_loners[label]=prefix + ' ' + pretty_loners[label]

    loners = 'Some other things we saw: ' + ', '.join(pretty_loners)

    summary+=loners
        
    if textExtracted:
        text_str = ', '.join(textExtracted.split('\n'))
        summary += 'The image has text, which says: ' + text_str + '.'
    # sort into locations
    # location_stuff(labels)
    # append
    
    return summary

def PrettyPrint(summary):
    pretty = '\n\n\n\nA Summary for the Image :\n'
    w = 50
    pretty+=textwrap.fill(summary,w)
    print(pretty)

def Run(impLabels,text):
    lab, ext = LoadData(impLabels,text)
    summary = GenerateSummary(lab,ext)
    PrettyPrint(summary)
    return summary
