"""
FP-Growth Association Rule Mining & Benchmark Comparison
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import sys
import time
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from association.apriori_analysis import load_transactions, run_apriori_analysis, DATASET_PATH

def run_fpgrowth_analysis(min_support=0.05, min_confidence=0.3, metric="confidence", filepath=DATASET_PATH):
    """
    Executes FP-Growth algorithm on skill transaction data.
    Builds FP-Tree structure and extracts frequent itemsets without candidate generation.
    """
    transactions = load_transactions(filepath)
    
    start_time = time.time()
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Run FP-Growth
    frequent_itemsets = fpgrowth(df_encoded, min_support=min_support, use_colnames=True)
    execution_time = time.time() - start_time
    
    rules_list = []
    if not frequent_itemsets.empty:
        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_confidence)
        rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
        rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
        
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
        "algorithm": "FP-Growth",
        "num_transactions": len(transactions),
        "execution_time_seconds": round(execution_time, 5),
        "frequent_itemsets_count": len(frequent_itemsets),
        "rules_count": len(rules_list),
        "frequent_itemsets": frequent_list,
        "rules": rules_list
    }

def compare_apriori_and_fpgrowth(min_support=0.08, min_confidence=0.3):
    """
    Direct benchmark comparing Apriori and FP-Growth performance.
    """
    apriori_res = run_apriori_analysis(min_support=min_support, min_confidence=min_confidence)
    fpgrowth_res = run_fpgrowth_analysis(min_support=min_support, min_confidence=min_confidence)
    
    ap_time = max(apriori_res["execution_time_seconds"], 0.0001)
    fp_time = max(fpgrowth_res["execution_time_seconds"], 0.0001)
    speedup = round(ap_time / fp_time, 2)
    
    comparison = {
        "apriori": {
            "algorithm": "Apriori",
            "execution_time": apriori_res["execution_time_seconds"],
            "frequent_itemsets": apriori_res["frequent_itemsets_count"],
            "rules_count": apriori_res["rules_count"],
            "complexity": "O(2^|I|) candidate itemset generation passes"
        },
        "fpgrowth": {
            "algorithm": "FP-Growth",
            "execution_time": fpgrowth_res["execution_time_seconds"],
            "frequent_itemsets": fpgrowth_res["frequent_itemsets_count"],
            "rules_count": fpgrowth_res["rules_count"],
            "complexity": "O(N) database scans, FP-Tree memory structure"
        },
        "speedup_ratio": f"{speedup}x",
        "key_insight": (
            "FP-Growth is significantly more efficient than Apriori because it constructs "
            "a compact Frequent Pattern Tree (FP-Tree) and mines frequent patterns by recursive "
            "conditional tree traversal, completely avoiding costly multi-pass candidate generation (Apriori candidate generation)."
        ),
        "sample_top_rules": fpgrowth_res["rules"][:10]
    }
    return comparison

if __name__ == "__main__":
    comp = compare_apriori_and_fpgrowth(min_support=0.05, min_confidence=0.3)
    print("=== Apriori vs FP-Growth Benchmark ===")
    print(f"Apriori Time: {comp['apriori']['execution_time']}s | FP-Growth Time: {comp['fpgrowth']['execution_time']}s")
    print(f"Speedup: {comp['speedup_ratio']}")
    print(f"Insight: {comp['key_insight']}")
