import os
import matplotlib.pyplot as plt

# Use current directory
directory = os.path.dirname(__file__)
score_files = [f for f in os.listdir(directory) if f.endswith("_math_score.txt")]

scores = []
labels = []

for file in sorted(score_files):
    path = os.path.join(directory, file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            # Expect format: "Score: 17/20"
            if "Score:" in first_line and "/" in first_line:
                score_str = first_line.split("Score:")[1].strip()
                parts = score_str.split("/")
                numerator = int(parts[0])
                denominator = int(parts[1])
                percentage_score = (numerator / denominator) * 100  # Now correctly scaled
                scores.append(percentage_score)
                label = file.replace("_math_score.txt", "")
                labels.append(label)
            else:
                print(f"Unexpected format in file {file}: {first_line}")
    except Exception as e:
        print(f"Skipping {file}: {e}")

# Sort by score (ascending)
sorted_pairs = sorted(zip(scores, labels))
sorted_scores, sorted_labels = zip(*sorted_pairs)

# Plot
plt.figure(figsize=(10, 6))
plt.bar(sorted_labels, sorted_scores, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Score (%)")
plt.title("Model Math Scores (Sorted by Percentage)")
plt.ylim(0, 100)
plt.tight_layout()

# Save and show plot
plot_file = os.path.join(directory, "math_model_scores_out_of_100.png")
plt.savefig(plot_file)
plt.show()
