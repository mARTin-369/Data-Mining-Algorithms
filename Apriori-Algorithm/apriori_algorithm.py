from itertools import combinations

def getAssociationRules(itemsets, data, freq_item_set, mcon):
    mcon = mcon/100
    assoc_rules = {}
    for itemset in freq_item_set:
        items = set(itemset.split('^'))
        for n in range(1, int(len(items)/2 + 1)):
            for comb in combinations(items, n):
                combi = set(comb)
                complement_comb = items - combi
                # print(combi, complement_comb)
                iconf = freq_item_set[itemset]/getCount(itemsets, combi)
                jconf = freq_item_set[itemset]/getCount(itemsets, complement_comb)
                # print(f" {'^'.join(list(combi))} => {'^'.join(list(complement_comb))} : {iconf}")
                # print(f" {'^'.join(list(complement_comb))} => {'^'.join(list(combi))} : {jconf}")
                if iconf >= mcon:
                    assoc_rules[f"{'^'.join(list(combi))} => {'^'.join(list(complement_comb))}"] = iconf
                if jconf >= mcon:
                    assoc_rules[f"{'^'.join(list(complement_comb))} => {'^'.join(list(combi))}"] = jconf
    return assoc_rules

def removeInvalid(cand_items, prev_items, size):
    cand_items_cpy = list(cand_items)
    for cand_item in cand_items:
        c_items = cand_item.split('^')
        for comb in combinations(c_items, size):
            i = '^'.join(sorted(comb))
            if i not in prev_items:
                cand_items_cpy.remove(cand_item)
                break
    return cand_items_cpy

def getCombination(items, size):
    itemsets = set()
    for i in items:
        for j in items:
            set1 = set(i.split('^'))
            set2 = set(j.split('^'))
            union_set = sorted(list(set1.union(set2)))
            if len(union_set) == size:
                union_set = '^'.join(union_set)
                itemsets.add(union_set)
    return itemsets

def getCount(itemsets, items):
    # print(itemsets)
    # print(items, end = " ")
    count = 0
    for itemset in itemsets:
        i = 0
        for item in items:
            if item not in itemset:
                break
            i = i + 1
        if i == len(items):
            count = count + 1
    # print(count)
    return count

def getFrequentItemsets(data, msup):
    msup = len(data)*msup/100
    itemsets = [ data[transac] for transac in data ]
    # print(itemsets)
    items = set([ x for itemset in itemsets for x in itemset ])
    size = 1

    while True:
        cand_itemset = {}
        freq_itemset = {}

        for item in items:
            cand_itemset[item] = getCount(itemsets, set(item.split('^')))

        items = set()
        for item in cand_itemset:
            if cand_itemset[item] >= msup:
                items.add(item)
                freq_itemset[item] = cand_itemset[item]

        size = size + 1
        if size == len(data) or len(items) == 1:
            break

        cand_items = getCombination(items, size)
        items = removeInvalid(cand_items, items, size-1)
        # print(items)
    return itemsets, freq_itemset

def getFileData(file_name):
    file_data = {}
    with open(file_name) as file:
        lines = file.readlines()
        lines.pop(0)

        # Read row data
        for line in lines:
            transac = list(line.replace('\n','').split(','))
            transac_id, items = transac[0], transac[1:]
            file_data[transac_id] = items
    return file_data

def main():
    data_file = input("Enter dataset file name: ")
    msup = int(input("Enter minimum support: "))
    mcon = int(input("Enter minimum confidence: "))
    data = getFileData(data_file)
    # print(data)
    itemsets, freq_item_set = getFrequentItemsets(data, msup)
    assoc_rules = getAssociationRules(itemsets, data, freq_item_set, mcon)

    print("\nFrequent itemsets:")
    for itemset in freq_item_set:
        print(f"Itemset: {itemset}, Support: {freq_item_set[itemset]}")

    print("\nAssociation Rules:")
    for assoc_rule in assoc_rules:
        print(f"Rule: {assoc_rule}, Confidence: {assoc_rules[assoc_rule]}")

if __name__ == "__main__":
    main()