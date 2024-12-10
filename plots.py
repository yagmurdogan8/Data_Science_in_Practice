import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
csv_file_path = "labeled_reports.csv"
data = pd.read_csv(csv_file_path)

# Normalize column names (strip spaces and convert to lowercase)
data.columns = data.columns.str.strip().str.lower()

# Dynamically identify violence-related columns
violence_types = [col for col in data.columns if "violence" in col or "famine" in col]

# Map "yes"/"no" to integers for violence type columns
for col in violence_types:
    data[col] = data[col].str.strip().str.lower().replace({"yes": 1, "no": 0}).fillna(0).astype(int)

# Compute the total counts of "Yes" for each violence type
violence_counts = data[violence_types].sum()

# Debugging - Confirm computed counts
print("Violence counts:")
print(violence_counts)

# Plot: Distribution of violence types
plt.figure(figsize=(8, 6))
sns.barplot(
    x=violence_counts.index.str.replace(": yes/no", "", regex=False), 
    y=violence_counts.values,
    palette=sns.color_palette("viridis", len(violence_types))
)
plt.title("Distribution of Violence Types in Situation Reports")
plt.xlabel("Type of Violence")
plt.ylabel("Number of Reports")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# Plot 2: Conflicts by perpetrator
if "perpetrator" in data.columns:
    plt.figure(figsize=(10, 8))
    sns.countplot(
        y=data["perpetrator"], 
        order=data["perpetrator"].value_counts().index,
        palette="coolwarm"
    )
    plt.title("Conflicts by Perpetrator")
    plt.xlabel("Number of Reports")
    plt.ylabel("Perpetrator")
    plt.tight_layout()
    plt.show()

# Plot 3: Conflicts by place
if "place" in data.columns:
    plt.figure(figsize=(10, 8))
    sns.countplot(
        y=data["place"], 
        order=data["place"].value_counts().index,
        palette="cividis"
    )
    plt.title("Conflicts by Place")
    plt.xlabel("Number of Reports")
    plt.ylabel("Place")
    plt.tight_layout()
    plt.show()
