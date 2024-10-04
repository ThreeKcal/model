def get_label(prediction):
    for i in prediction:
        label = i['label']

    return label

def get_score(prediction):
    for i in prediction:
        score = i['score']

    return score



