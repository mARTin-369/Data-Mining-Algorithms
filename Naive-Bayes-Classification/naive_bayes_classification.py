def getBayesianClassification(probability_classes, attri_condit_probs):
    bayesian_classification = []
    for class_prob in probability_classes:
        probablity = probability_classes[class_prob]['probability']
        for attri_prob in attri_condit_probs:
            probablity = probablity*attri_condit_probs[attri_prob][class_prob]['probability']
        bayesian_classification.append({ class_prob: probablity })
    return bayesian_classification

def getAttributeProbabilities(predict, sample, classes, probability_classes, data, attributes):
    count = { attri:{ c: 0 for c in classes} for attri in attributes}
    for row in data:
        for att in attributes:
            if sample[att] == row[att]:
                count[att][row[predict]] = count[att][row[predict]] + 1
    att_count = { att: { c: { 'probability': count[att][c]/probability_classes[c]['count'], 'count': count[att][c] } for c in classes } for att in attributes }
    return att_count

def getClassProbability(predict, data, classes):
    count = { x: 0 for x in classes }
    for row in data:
        count[row[predict]] = count[row[predict]] + 1
    class_count = { x: { 'probability': count[x]/len(data), 'count': count[x] } for x in count }
    return class_count
        

def getClasses(data, predict):
    classes = set([ x for x in [ row[predict] for row in data]])
    return classes

def getFileSample(file_name):
    predict = ''
    sample = {}
    with open(file_name) as file:
        lines = file.readlines()

        # Read column names
        predict = list(lines[0].split())[0]
        lines.pop(0)

        # Read row data
        for line in lines:
            att, value = list(line.split())
            sample[att] = value
              
    return predict, sample

def getFileData(file_name):
    file_data = []
    header = []
    with open(file_name) as file:
        lines = file.readlines()

        # Read column names
        header.extend(list(lines[0].split()))
        lines.pop(0)

        # Read row data
        for line in lines:
            data = {}
            row = list(line.split())
            for i in range(len(header)):
                if row[i].isnumeric():
                    data[header[i]] = float(row[i])
                else:
                    data[header[i]] = row[i]
            file_data.append(data)  
    return file_data, header

def main():
    data_file = 'play_tennis.txt'
    sample_file = 'sample2.txt'
    data, attributes = getFileData(data_file)
    predict, sample = getFileSample(sample_file)
    attributes.remove(predict)
    # print(attributes)
    classes = getClasses(data, predict)
    # print(classes)
    probability_classes = getClassProbability(predict, data, classes)
    # print(probability_classes)
    attri_condit_probs = getAttributeProbabilities(predict, sample, classes, probability_classes, data, attributes)
    # print(attri_condit_probs)
    bayesian_classification = getBayesianClassification(probability_classes, attri_condit_probs)
    print("Naive Bayes Classification: ", bayesian_classification)

if __name__ == "__main__":
    main()