import os
import matplotlib.pyplot as plt
import numpy as np

# Use current directory or set an explicit path
directory = os.path.dirname(__file__)
score_files = [f for f in os.listdir(directory) if f.endswith("_logic_score.txt")]

# Define model groups for side-by-side comparison
model_groups = {
    "Llama 3.2 3B": ["llama_3.2_3b", "llama_3.2_3b_z3"],
    "Gemma 3 4B": ["gemma_3_4b", "gemma_3_4b_z3"],
    "DeepSeek R1 8B": ["deepseek_r1_distill_llama_8b", "deepseek_r1_distill_llama_8b_z3"],
    "Llama 3.1 8B": ["llama_3.1_8b", "llama_3.1_8b_z3"],
    "DeepSeek V3_chat": ["deepseek_v3_full"],
    "DeepSeek R1": ["deepseek_r1_full"]
}

# Parse scores
score_dict = {}
for file in score_files:
    path = os.path.join(directory, file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if "Score:" in first_line and "/" in first_line:
                score_str = first_line.split("Score:")[1].strip()
                numerator = int(score_str.split("/")[0])
                label = file.replace("_logic_score.txt", "")
                score_dict[label] = numerator
            else:
                print(f"Unexpected format in file {file}: {first_line}")
    except Exception as e:
        print(f"Skipping {file}: {e}")

# Prepare data for grouped bar chart
group_names = list(model_groups.keys())
base_scores = []
z3_scores = []

for group_name, models in model_groups.items():
    if len(models) == 2:
        base_scores.append(score_dict.get(models[0], 0))
        z3_scores.append(score_dict.get(models[1], 0))
    else:
        # For groups without z3 variants, we'll handle them specially
        base_scores.append(score_dict.get(models[0], 0))
        z3_scores.append(score_dict.get(models[1], 0) if len(models) > 1 else 0)

# Set up the bar chart
x = np.arange(len(group_names))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 7))

# Create grouped bars
bars1 = ax.bar(x - width/2, base_scores, width, label='Base Model', color='skyblue', alpha=0.8)
bars2 = ax.bar(x + width/2, z3_scores, width, label='Z3 Variant', color='lightcoral', alpha=0.8)

# Add value labels on bars
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:  # Only add label if there's a score
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=9)

add_value_labels(bars1)
add_value_labels(bars2)

# Customize the chart
ax.set_xlabel('Model Groups')
ax.set_ylabel('Score (out of 20)')
ax.set_title('Model Logic Scores: Base vs Z3 Variants')
ax.set_xticks(x)
ax.set_xticklabels(group_names, rotation=45, ha='right')
ax.set_ylim(0, 32)  # Slightly higher to accommodate labels
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# Save and show
plot_file = os.path.join(directory, "model_logic_scores_grouped.png")
plt.savefig(plot_file, dpi=300, bbox_inches='tight')
plt.show()

# Print summary
print("\nScore Summary:")
print("-" * 50)
for group_name, models in model_groups.items():
    base_score = score_dict.get(models[0], 0)
    z3_score = score_dict.get(models[1], 0) if len(models) > 1 else 0
    print(f"{group_name}:")
    print(f"  Base: {base_score}/20")
    if len(models) > 1 and models[1].endswith('_z3'):
        print(f"  Z3:   {z3_score}/20")
        diff = z3_score - base_score
        print(f"  Diff: {diff:+d}")
    else:
        print(f"  Alt:  {z3_score}/20")
    print()