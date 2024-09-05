from tabulate import tabulate

# Example output values
P1, R1, F1_1 = 0.75, 0.80, 0.77
F1_system_1 = 0.78

P2, R2, F1_2 = 0.70, 0.85, 0.77
F1_system_2 = 0.79

# Table data
table_data = [
    ["Evaluation Type", "Precision", "Recall", "F1 Score"],
    ["Sentence Level (lang=zh)", P1, R1, F1_1],
    ["System Level (lang=en)", "-", "-", F1_system_1],
    ["Sentence Level (lang=others)", P2, R2, F1_2],
    ["System Level (lang=en)", "-", "-", F1_system_2],
]

# Print table
print(tabulate(table_data, headers="firstrow", floatfmt=".3f"))
