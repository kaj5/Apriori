## Krutarth Joshi
##########################################
############## How To Run ################
## python apriori.py (with default arguments)
## python apriori.py dataSet.csv minimum_support minimum_confidence

## Optional:
## Run: python apriori.py -h => To get more information on how to run the program

import argparse
import csv
import itertools

def get_data(datafile):
    with open(datafile, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    return data

def clean_data(data):
    x = []
    for i in data:
        i = list(filter(None, i))
        i = [(x,) for x in i]
        x.append(i)
    
    return x

def print_input_transactions(data):
    print("=================================================================")
    print("Input Transactions: ")
    for i in range(len(data)):
        item = data[i]
        item = [j for t in item for j in t] 
        itemNumber = str(i + 1) + "."
        print(itemNumber, item)

def initialized_counter(data, n = None):
    x = []
    for i in data:
        if n is None:
            z = []
            for j in i:
                k = [j, 1]
                z.append(k)
            x.append(z)
        else:
            i = tuple(i)
            k = [i, 1]
            x.append(k)

    return x

def get_candidate_itemset(dataSet, n = None):
    x = {}

    if n is None:
        for i in dataSet:
            for j, k in i:
                x[j] = x.get(j,0) + k
    else:
        for i, j in dataSet:
            x[i] = x.get(i, 0) + j

    return x

def get_frequent_rejected_items(candidateItemSet, totalDataSetCount):
    frequent = []
    rejected = []
    frequentItemsetWithSupport = []

    for key, value in candidateItemSet.items():
        calculateSupport = value/totalDataSetCount

        if calculateSupport >= args['minimumSupport']:
            item = [key, calculateSupport]
            frequent.append(key)
            frequentItemsetWithSupport.append(item)
        else:
            rejected.append(key)

    print_frequent_item_with_support(frequentItemsetWithSupport)
    return frequent, rejected, frequentItemsetWithSupport

def find_frequent_set(frequent, rejected, dataset, lengthOfCombinations):
    combination = itertools.combinations(frequent, lengthOfCombinations)
    combination = initialized_counter(combination, 1)
    combinationCount = 0
    subsetItemList = []
    while combinationCount < len(combination):
        combinationItem = combination[combinationCount]
        datasetCounter = 0
        while datasetCounter < len(dataset):
            datasetItem = dataset[datasetCounter]
            issubset = all(x in datasetItem for x in combinationItem[0])

            if(issubset):
                subsetItemList.append(combinationItem)

            datasetCounter += 1

        combinationCount += 1

    frequentItemSet = get_candidate_itemset(subsetItemList, 1)
    newFrequent, newRejected, newFrequentItemsetWithSupport = get_frequent_rejected_items(frequentItemSet, len(dataset))
    
    return newFrequent, newRejected, newFrequentItemsetWithSupport

def print_frequent_item_with_support(itemset):
    if len(itemset) == 0:
        return

    print("=================================================================")

    print("Frequent Itemsets -> Support:")
    for item in itemset:
        itemCopy = item.copy()
        if(len(itemCopy[0]) == 1):
            print(str(itemCopy[0][0]) + " -> " + str(round(itemCopy[1], 3)))
        else:
            itemCopy[0] = [y for x in itemCopy[0] for y in x]

            print (', '.join(str(p) for p in itemCopy[0]), " -> ", str(round(itemCopy[1], 3)))

def association_rules(frequentItemsetwithSupport, frequentItemSet):
    print("=================================================================")
    for i in frequentItemSet:
        count = len(i)-1
        i = list(i)
        for j in range(count, 0, -1):
            combinations = itertools.combinations(i, j)
            
            if j == 1:
                combinations = [item for sublist in combinations for item in sublist]
            
            for k in combinations:
                y = i.copy()
                
                if j == 1:
                    x = k
                    y.remove(k)
                else:
                    x = tuple(k)
                    y = remove_item_from_itemset(y, k)

                y = list_to_tuple(y)

                supportForX = allFrequentItemsetWithSupport[x]
                supportForY = allFrequentItemsetWithSupport[tuple(i)]

                confidence = (supportForY/supportForX)

                print_association_rules(x, y, confidence)

def print_association_rules(item1, item2, confidence):
    if len(item1) == 1:
        strItem1 = ', '.join(str(p) for p in item1)
    else:
        item1 = [y for x in item1 for y in x]
        strItem1 = ', '.join(str(p) for p in item1)

    if len(item2) == 1: 
        strItem2 = ', '.join(str(p) for p in item2)
    else:
        item2 = [y for x in item2 for y in x]
        strItem2 = ', '.join(str(p) for p in item2)

    ruleStatus = ""
    if confidence >= args['minimumConfidence']:
        ruleStatus = "Rule Selected"
    else:
        ruleStatus = "Rule Rejected"
        
    print("Rule: (" + strItem1 + ") -> (" + strItem2 + ")")
    print("Confidence: " + str(round(confidence, 3)))
    print("Minimum Confidence: " + str(args['minimumConfidence']))
    print("Rule Status: " + ruleStatus)
    print("=================================================================")

def remove_item_from_itemset(itemset, combination):
    for j in combination:
        itemset.remove(j)

    return itemset

def list_to_tuple(lst):
    if len(lst) == 1:
        for i in lst:
            return i
    else:
        return tuple(lst)

def parse_args():
    parser=argparse.ArgumentParser(description="Applying Apriori Algorithm to print out all the association rules")
    parser.add_argument("datafile", nargs="?", help="A .csv dataset for the algorithm", default="amazonDataSet.csv")
    parser.add_argument("minimumSupport", nargs="?", help="Minimum support (for example, 0.5)", type=float, default=0.5)
    parser.add_argument("minimumConfidence", nargs="?", help="Minimum confidence (for example, 0.7)", type=float, default=0.7)
    options = parser.parse_args()

    args = vars(options)

    return args

def add_items_to_support_list(supportList):
    for elem in supportList:
        allFrequentItemsetWithSupport[elem[0]] = elem[1]

    return None

args = parse_args()

datafile = clean_data(get_data(args['datafile']))

print_input_transactions(datafile)

y = initialized_counter(datafile)
candidateItemSet = get_candidate_itemset(y)

totalDataSetCount = len(datafile)
frequent, rejected, frequentItemsetWithSupport = get_frequent_rejected_items(candidateItemSet, totalDataSetCount)

allFrequentItemsetWithSupport = {}
add_items_to_support_list(frequentItemsetWithSupport)

for i in range(1, len(frequentItemsetWithSupport) + 1):
    newFrequent, newRejected, newFrequentItemsetWithSupport = find_frequent_set(frequent, rejected, datafile, i + 1)
    
    if len(newFrequent) == 0 or newFrequent is None:
        break
    
    add_items_to_support_list(newFrequentItemsetWithSupport)
    association_rules(allFrequentItemsetWithSupport, newFrequent)

    frequentItemsetWithSupport = newFrequentItemsetWithSupport