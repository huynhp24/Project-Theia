import json
def list_of_labels(data):
    confident_labels = []
    for label in data['Labels']:
        for instance in label['Instances']:
            if instance['Confidence'] > 0:
                confident_labels.append(label['Name'])
    a_dict = {}
    for item in confident_labels:
        if item not in a_dict.keys():
            d = {item: 1}
        else:
            new_val = a_dict[item] + 1
            d = {item: new_val}
        a_dict.update(d)
    total_keys = len(a_dict.keys())
    string = ""
    i = 1
    for entry in a_dict.keys():
        if i == total_keys and i > 1:
            string = string + "and "
        elif i == 1:
            string = ""
        if a_dict[entry] > 1:
            string = string + str(a_dict[entry]) + " " + entry + "s "
        else:
            string = string + str(a_dict[entry]) + " " + entry + " "
        i = i + 1
    if len(string) > 0:
        return string
    else:
        return None
def get_main_subject(data):
    largest_area = 0
    largest_subject = None
    for label in data['Labels']:
        for instance in label['Instances']:
            width = instance['BoundingBox']['Width']
            height = instance['BoundingBox']['Height']
            area = width * height
            if area > largest_area:
                largest_area = area
                largest_subject = label['Name']
    return largest_subject
def get_image_context(data):
    min_confidence = 75
    subjects = []
    for label in data['Labels']:
        if (len(label['Instances']) == 0) and (label['Confidence'] > min_confidence):
            subjects.append(label['Name'])
        if len(subjects) == 3:
            break
    if len(subjects) > 0:
        string = ""
        for item in subjects:
            if len(string) == 0:
                string = item
            else:
                string = string + " or " + item
        return string
    else:
        return None
def generate_nat_string(json_data):
    # data = json.dumps(json_data)
    data = json_data
    labels = list_of_labels(data=data)
    main_subject = get_main_subject(data=data)
    context = get_image_context(data=data)
    if (labels and main_subject and context) is not None:
        string = "This is probably an image of " + context + ". The main subject appears to be a " + main_subject + ". The image contains " + labels
    elif (main_subject and labels) is None:
        string = "We're not sure what's in the image, but it appears to be an image of " + context
    else:
        string = "We ran into an unexpected image scenario, but the image label dump is:" + context + main_subject + labels
    return string