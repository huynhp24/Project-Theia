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
                instances.append(instance)
        labels[label['Name']]={'Confidence': label['Confidence'], 'Parents': parents, 'Instances': label['Instances']}
    print(text)
    for reading in text['TextDetections']:
        if('ParentId' not in reading): # i can piggy back on the label??
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

def location(labels, label):
    location =[]
    for instance in labels[label]['Instances']:
        if("BoundingBox" in instance):
            theBox = defaultdict()
            theBox["left"] = instance["BoundingBox"]["Left"]
            theBox["top"] = instance["BoundingBox"]["Top"]
            theBox["right"] = instance["BoundingBox"]["Left"] + instance["BoundingBox"]["Width"]
            theBox["bottom"] = instance["BoundingBox"]["Top"] + instance["BoundingBox"]["Height"]

            if(theBox["left"]<.33):
                if(theBox["top"]<.33):
                    if(theBox["bottom"]<.33):
                        if(theBox["right"]<.33):
                            location.append("in the top left corner")
                        elif(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("along the top left")
                        elif(theBox["right"]>=.66):
                            location.append("across the top")
                    if(theBox["bottom"]>=.33 and theBox["bottom"]<.66):
                        if(theBox["right"]<.33):
                            location.append("in the upper left hand side")
                        elif(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("in the center left area")
                        elif(theBox["right"]>=.66):
                            location.append("across the upper middle")
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]<.33):
                            location.append("along the left side")
                        elif(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("on the left side")
                        elif(theBox["right"]>=.66):
                            location.append("across the whole image")
                if(theBox["top"]>=.33 and theBox["top"]<.66):
                    if(theBox["bottom"]>=.33 and theBox["bottom"]<.66):
                        if(theBox["right"]<.33):
                            location.append("in the very middle of the left")
                        elif(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("through the middle left area")
                        elif(theBox["right"]>=.66):
                            location.append("horizontally across the middle")
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]<.33):
                            location.append("along the left side")
                        elif(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("in the lower left side")
                        elif(theBox["right"]>=.66):
                            location.append("across the lower middle")
                if(theBox["top"]>=.66):
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]<.33):
                            location.append("in the lower left corner")
                        elif(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("on the lower left")
                        elif(theBox["right"]>=.66):
                            location.append("across the bottom")
            elif(theBox["left"]>=.33 and theBox["left"]<.66):
                if(theBox["top"]<.33):
                    if(theBox["bottom"]<.33):
                        if(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("at the top middle")
                        elif(theBox["right"]>=.66):
                            location.append("at the top right side")
                    if(theBox["bottom"]>=.33 and theBox["bottom"]<.66):
                        if(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("at the upper center")
                        elif(theBox["right"]>=.66):
                            location.append("in the upper right area")
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("vertically across the middle")
                        elif(theBox["right"]>=.66):
                            location.append("on the right side")
                if(theBox["top"]>=.33 and theBox["top"]<.66):
                    if(theBox["bottom"]>=.33 and theBox["bottom"]<.66):
                        if(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("in the very middle")
                        elif(theBox["right"]>=.66):
                            location.append("on the middle right")
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("at the bottom middle")
                        elif(theBox["right"]>=.66):
                            location.append("in the middle right area")
                if(theBox["top"]>=.66):
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]>=.33 and theBox["right"]<.66):
                            location.append("at the bottom center")
                        elif(theBox["right"]>=.66):
                            location.append("along center right")
            elif(theBox["left"]>=.66):
                if(theBox["top"]<.33):
                    if(theBox["bottom"]<.33):
                        if(theBox["right"]>=.66):
                            location.append("in the top right corner")
                    if(theBox["bottom"]>=.33 and theBox["bottom"]<.66):
                        if(theBox["right"]>=.66):
                            location.append("at the top right")
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]>=.66):
                            location.append("along the right side")
                if(theBox["top"]>=.33 and theBox["top"]<.66):
                    if(theBox["bottom"]>=.33 and theBox["bottom"]<.66):
                        if(theBox["right"]>=.66):
                            location.append("in the middle of the right side")
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]>=.66):
                            location.append("in the lower right")
                if(theBox["top"]>=.66):
                    if(theBox["bottom"]>=.66):
                        if(theBox["right"]>=.66):
                            location.append("in the bottom right corner")

            i= labels[label]['Instances'].index(instance)
            if i > len(location)-1:
                print("BAD BOX: ")
                print(theBox)
            else:
                print("GOOD BOX: " + location[i])
                print(theBox)
    return location

         
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
    # collapse into parent

    global delete_list
    delete_list = defaultdict()

    ref_labels = copy.deepcopy(labels)
    for label in ref_labels:
        collapsed = theCollapse(ref_labels, label)
        print(label + " <---- " + collapsed)
        if(len(collapsed)>0):
            labels[label]['Parents']=[collapsed]
            instances = ref_labels[label]['Instances']
            current_big = len(instances)
            for parent in ref_labels[label]['Parents']:
                if(len(ref_labels[parent]['Instances'])>current_big):
                    instances=[]
                    for instance in ref_labels[parent]['Instances']:
                        instances.append(instance)
            labels[label]["Instances"]=instances
    
    for label in delete_list:
        print('DELETING: ' + label)
        del labels[label]

    pretty_parents = defaultdict()
    for label in labels:
        if(len(labels[label]['Parents'])>0):
            if(labels[label]['Parents'][0] != label):
                pretty_parents[labels[label]['Parents'][0]]={'Children': []}
                pretty_parents[labels[label]['Parents'][0]]['Instances']=[] #labels[label]['Instances']]

    pretty_loners = defaultdict()

    for label in labels:
        if(len(labels[label]['Parents'])>0):
            if(labels[label]['Parents'][0] != label):
                pretty_parents[labels[label]['Parents'][0]]['Children'].append(label)
                for instance in labels[label]['Instances']:
                    pretty_parents[labels[label]['Parents'][0]]['Instances'].append(instance)      
            else:
                pretty_loners[label]={'Confidence': labels[label]['Confidence'], 'Instances': labels[label]['Instances']}
        else:
            pretty_loners[label]={'Confidence': labels[label]['Confidence'], 'Instances': labels[label]['Instances']}

    print(labels)
    print(pretty_parents)
    print(pretty_loners)

    for label in pretty_parents:
        print("pretty parent: " + label)
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='is an'
        else:
            prefix='is a'

        suffix = ''

        locs = ""
        if(len(pretty_parents[label]['Instances'])>1):
            loc = location(pretty_parents,label)
            if(len(loc)>0):
                if(len(set(loc))>4):
                    locs="They are located throughout the image. "
                else:
                    locs="Their locations: "
                    pretty_loc = []
                    for it in set(loc):
                        pretty_loc.append(it)
                    locs+= ' and '.join(pretty_loc)+'. '
            prefix = 'are ' + str(len(loc))
            suffix = 's'

        kids=' or '.join(pretty_parents[label]['Children'])

        summary+= "There "+ prefix +" " + label+ suffix+" in the image. "+ locs
        if(len(pretty_parents[label]['Children'])>0):
            summary+="Some description of the " + label + suffix+": " + kids+ ". "

    loner_list=[]

    for label in pretty_loners:
        print("pretty loner: " + label)
        ch = label[0]
        if(ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
            prefix='an'
        else:
            prefix='a'
        
        suffix = ''
        
        locs = ""
        if(len(pretty_loners[label]['Instances'])>1):
            loc = location(pretty_loners,label)
            if(len(loc)>0):
                if(len(set(loc))>4):
                    locs=" (located throughout the image"
                else:
                    locs=" (their locations: "
                    pretty_loc = []
                    for it in set(loc):
                        pretty_loc.append(it)
                    locs+= ' and '.join(pretty_loc)
            locs+=') '
            prefix = str(len(pretty_loners[label]['Instances']))
            suffix = 's'
        
        loner_list.append(prefix +" " + label+ suffix+ locs)

    if(len(pretty_loners)>0):
        if(len(loner_list)>1):
            loners = 'Some other things we saw: ' + ', '.join(loner_list[:-1]) + ' and '+ loner_list[-1] + ". "
        else:
            loners = 'Another thing we saw: ' + loner_list[0] + ". "

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
