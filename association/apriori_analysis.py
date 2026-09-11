"""
Apriori Association Rule Mining Analysis
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import time
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "skill_transactions.csv")

def load_transactions(filepath=DATASET_PATH):
    """Load skill transactions from CSV and convert to list of lists."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Transactions dataset not found at {filepath}")
    df = pd.read_csv(filepath)
    transactions = [
        [s.strip() for s in row.split(",") if s.strip()] 
        for row in df["skills"].dropna()
    ]
    return transactions

def run_apriori_analysis(min_support=0.05, min_confidence=0.3, metric="confidence", filepath=DATASET_PATH):
    """
    Executes Apriori algorithm on skill transaction data.
    Measures execution time and generates frequent itemsets and association rules.
    """
    transactions = load_transactions(filepath)
    
    start_time = time.time()
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Run Apriori
    frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
    execution_time = time.time() - start_time
    
    rules_list = []
    if not frequent_itemsets.empty:
        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_confidence)
        rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
        rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
        
        # Sort by lift descending
        rules = rules.sort_values(by="lift", ascending=False)
        
        for _, r in rules.iterrows():
            rules_list.append({
                "antecedents": r["antecedents_str"],
                "consequents": r["consequents_str"],
                "support": round(float(r["support"]), 4),
                "confidence": round(float(r["confidence"]), 4),
                "lift": round(float(r["lift"]), 4),
                "leverage": round(float(r["leverage"]), 4) if "leverage" in r else 0.0,
                "conviction": round(float(r["conviction"]), 4) if "conviction" in r and not pd.isna(r["conviction"]) and r["conviction"] != float("inf") else 999.0
            })
            
    frequent_list = []
    for _, item in frequent_itemsets.iterrows():
        frequent_list.append({
            "itemset": ", ".join(list(item["itemsets"])),
            "length": len(item["itemsets"]),
            "support": round(float(item["support"]), 4)
        })
        
    return {
        "algorithm": "Apriori",
        "num_transactions": len(transactions),
        "execution_time_seconds": round(execution_time, 5),
        "frequent_itemsets_count": len(frequent_itemsets),
        "rules_count": len(rules_list),
        "frequent_itemsets": frequent_list,
        "rules": rules_list
    }

if __name__ == "__main__":
    res = run_apriori_analysis(min_support=0.08, min_confidence=0.4)
    print(f"Apriori Completed in {res['execution_time_seconds']}s")
    print(f"Found {res['frequent_itemsets_count']} itemsets and {res['rules_count']} rules.")
    for rule in res["rules"][:5]:
        print(f"  {rule['antecedents']} -> {rule['consequents']} (Supp: {rule['support']}, Conf: {rule['confidence']}, Lift: {rule['lift']})")
