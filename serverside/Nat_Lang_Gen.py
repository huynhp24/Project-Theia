import re
from collections import defaultdict
import textwrap
import copy

###Constants###
LABEL_SECTION = 'Label: '
PIC_TITLE = 'Detected labels for '
END_LABEL = '----------'

###Variables###
maxLevel = 0
oldest = ""
delete_list = defaultdict()

def LoadData(impLabels,text):

    print(impLabels)
    labels=defaultdict()
    textExtracted=" "
    for label in impLabels['Labels']:
        parents=[]
        instances=[]
        if(len(label['Parents'])>0):
            for parent in label['Parents']:
                parents.append(parent['Name'])
        if(len(label['Instances'])>0):
            for instance in label['Instances']:
                instances.append(instance['Name'])
        labels[label['Name']]={'Confidence': label['Confidence'], 'Parents': parents, 'Instances': label['Instances']}
    print(text)
    for reading in text['TextDetections']:
        if('ParentId' not in reading):
            textExtracted+=reading["DetectedText"] + " "
    textExtracted=textExtracted[1:-1] 
    return labels, textExtracted

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
    if(labels[label]['Confidence']>90):
        oldestAncestor(labels, label, level)
    else:
        delete_list[label]=""
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
        if(len(collapsed)>0):
            labels[label]['Parents']=[collapsed]
    
    for label in delete_list:
        print('DELETING: ' + label)
        del labels[label]

    pretty_parents = defaultdict()
    for label in labels:
        if(len(labels[label]['Parents'])>0):
            pretty_parents[labels[label]['Parents'][0]]={'Children': []}
        if(len(labels[label]['Instances'])>0):
            pretty_parents[labels[label]['Instances'][0]]={'Instances': []}

    pretty_loners = []

    for label in labels:
        if(len(labels[label]['Parents'])>0):
            pretty_parents[labels[label]['Parents'][0]]['Children'].append(label)
        else:
            pretty_loners.append(label)

    print(labels)
    print(pretty_parents)

    '''for label in labels:
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            labels[label]['prefix']='an'
        else:
            labels[label]['prefix']='a'

            summary += 'The image contains '+ labels[label]['prefix'] +' ' + label+'. '''

    for label in pretty_parents:
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='an'
        else:
            prefix='a'

        if(len(pretty_parents[label]['Instances'])>0):
            prefix = str(len(pretty_parents[label]['Instances']))

        kids=' or '.join(pretty_parents[label]['Children'])

        summary+= "There is "+ prefix +" " + label+ " in the image. Some description of the " + label + ": " + kids+ ". "

    for label in pretty_loners:
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='an'
        else:
            prefix='a'
        
        label=prefix + ' ' + label

    if(len(pretty_loners)>0):
        last = pretty_loners.pop()
        if(len(pretty_loners)>1):
            loners = 'Some other things we saw: ' + ', '.join(pretty_loners[:-1]) + ' and '+ last + ". "
        else:
            loners = 'Another thing we saw: ' + last + ". "

        summary+=loners
        
    if textExtracted:
        text_str = ', '.join(textExtracted.split('\n'))
        summary += 'The image has text, which says, ' + text_str + '.'
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
