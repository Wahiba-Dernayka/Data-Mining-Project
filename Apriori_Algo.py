from itertools import combinations
from itertools import chain

# Function to generate non-empty subsets of a set (frozenset)
def generate_subsets(itemset):
    """Generate non-empty subsets of an itemset."""
    itemset = list(itemset)
    return chain.from_iterable(combinations(itemset, r) for r in range(1, len(itemset)))

# Function to generate candidate itemsets
def generate_candidates(itemsets, k):
    candidates = set()
    itemsets_list = list(itemsets)
    for i in range(len(itemsets_list)):
        for j in range(i + 1, len(itemsets_list)):
            union_set = itemsets_list[i].union(itemsets_list[j])
            if len(union_set) == k:
                candidates.add(frozenset(union_set))
    return candidates

# Function to calculate itemset support
def calculate_support(transactions, itemsets):
    total_transactions = len(transactions)
    support = {}
    for itemset in itemsets:
        count = sum(1 for transaction in transactions if itemset.issubset(transaction))
        support[itemset] = count / total_transactions
    return support

# Apriori algorithm to find frequent itemsets
def apriori(transactions, min_support):
    # Start with single itemsets
    items = set(item for transaction in transactions for item in transaction)
    current_itemsets = {frozenset([item]) for item in items}
    
    # Store frequent itemsets
    frequent_itemsets = {}
    support_data = {}
    
    # Iterate over itemsets of size k
    k = 1
    while current_itemsets:
        support = calculate_support(transactions, current_itemsets)
        
        # Filter itemsets that meet the minimum support
        current_frequent_itemsets = {itemset: sup for itemset, sup in support.items() if sup >= min_support}
        
        if not current_frequent_itemsets:
            break
        
        frequent_itemsets.update(current_frequent_itemsets)
        support_data.update(current_frequent_itemsets)
        
        # Generate candidates for the next size
        current_itemsets = generate_candidates(current_frequent_itemsets.keys(), k + 1)
        
        k += 1
    
    return frequent_itemsets, support_data

# Function to generate association rules
def generate_association_rules(frequent_itemsets, min_confidence, transactions):
    association_rules = []
    
    # Iterate over the frequent itemsets
    for itemset in frequent_itemsets:
        # Generate all subsets of the itemset (excluding the entire itemset itself)
        subsets = list(generate_subsets(itemset))
        
        # For each subset, calculate the confidence of the rule
        for subset in subsets:
            # Convert the subset to a frozenset
            subset_frozenset = frozenset(subset)
            
            # Calculate the remaining itemset (itemset - subset)
            remaining = itemset - subset_frozenset
            
            # Check if the remaining itemset is not empty
            if remaining:
                # Calculate the support of the itemset (A U B) and the subset (A)
                support_itemset = calculate_support(transactions, [itemset])[itemset]
                support_subset = calculate_support(transactions, [frozenset(subset_frozenset)])[frozenset(subset_frozenset)]
                
                # Calculate the confidence of the rule
                confidence = support_itemset / support_subset
                
                # If the confidence meets the threshold, add the rule
                if confidence >= min_confidence:
                    association_rules.append((frozenset(subset_frozenset), frozenset(remaining), confidence))
    
    return association_rules