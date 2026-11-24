# Project 1: load, clean, and plot the Titanic dataset.

# Use a non-interactive backend so figures are saved without opening a window.
import matplotlib

matplotlib.use("Agg")

# pandas stores the table and computes summary statistics.
import pandas as pd

# seaborn provides the Titanic dataset and the plotting functions.
import seaborn as sns

# pyplot sets titles, axis labels, and writes the figure files.
import matplotlib.pyplot as plt

# Path builds the folder where the figure files are saved.
from pathlib import Path


# Folder that contains this script. Output files are written next to it.
SCRIPT_DIR = Path(__file__).resolve().parent

# Folder for the PNG figures.
FIGURE_DIR = SCRIPT_DIR / "figures"

# Create the folder if it does not exist. Do nothing if it already exists.
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Apply a clean theme with a light grid.
sns.set_theme(style="whitegrid")

# Load the built-in Titanic table into a DataFrame.
# Columns used below include age, class, deck, sex, fare, and alive.
df = sns.load_dataset("titanic")

# Print the number of rows and columns before cleaning.
print("Shape before cleaning:", df.shape)

# Drop every row that has at least one empty cell.
# Deck and age are missing for many passengers, so the row count falls.
df = df.dropna().copy()

# Restart the row index at zero after the dropped rows.
df = df.reset_index(drop=True)

# Print the number of rows and columns after cleaning.
print("Shape after cleaning:", df.shape)

# Turn the alive column into labels used on the charts.
# "yes" means the passenger survived. "no" means the passenger died.
df["outcome"] = df["alive"].map({"yes": "Survived", "no": "Died"})

# Survived bars are blue. Died bars are orange.
COLORS = {"Survived": "#1f77b4", "Died": "#ff7f0e"}


def save_figure(filename):
    # Keep titles and axis labels inside the figure frame.
    plt.tight_layout()
    # Save the current figure as a PNG sharp enough for the report.
    plt.savefig(FIGURE_DIR / filename, dpi=150)
    # Close the figure so the next plot does not reuse its axes.
    plt.close()


# --- 1. Passenger age distribution (histogram) ---

# Open a figure that is 8 units wide and 5 units tall.
plt.figure(figsize=(8, 5))

# Draw the age values as a histogram with 20 bins.
# kde=True adds a smooth density curve over the bars.
sns.histplot(data=df, x="age", bins=20, kde=True, color="#4c78a8")

# Set the chart title.
plt.title("Age Distribution of Passengers")

# Label the horizontal axis with age.
plt.xlabel("Age")

# Label the vertical axis with the number of passengers.
plt.ylabel("Frequency")

# Save the histogram and close the figure.
save_figure("01_age_distribution.png")


# --- 2. Victims and survivors in each class ---

# Open a new figure for the class chart.
plt.figure(figsize=(8, 5))

# Count survivors and victims in each passenger class.
# hue draws a separate bar for Survived and Died inside each class.
sns.countplot(
    data=df,
    x="class",
    hue="outcome",
    hue_order=["Survived", "Died"],
    palette=COLORS,
)

# Set the chart title.
plt.title("Survival Count by Class")

# Label the horizontal axis with passenger class.
plt.xlabel("Passenger Class")

# Label the vertical axis with the passenger count.
plt.ylabel("Count")

# Set the legend title.
plt.legend(title="Outcome")

# Save the class chart and close the figure.
save_figure("02_survival_by_class.png")


# --- 3. Victims and survivors on each deck ---

# Open a new figure for the deck chart.
plt.figure(figsize=(8, 5))

# Count survivors and victims on each deck.
# order places the decks from A to G.
sns.countplot(
    data=df,
    x="deck",
    hue="outcome",
    hue_order=["Survived", "Died"],
    palette=COLORS,
    order=list("ABCDEFG"),
)

# Set the chart title.
plt.title("Survival Count by Deck")

# Label the horizontal axis with the deck letter.
plt.xlabel("Deck")

# Label the vertical axis with the passenger count.
plt.ylabel("Count")

# Set the legend title.
plt.legend(title="Outcome")

# Save the deck chart and close the figure.
save_figure("03_survival_by_deck.png")


# --- 4. Extra plot: victims and survivors by sex ---

# Open a new figure for the sex chart.
plt.figure(figsize=(8, 5))

# Compare survivors and victims for female and male passengers.
sns.countplot(
    data=df,
    x="sex",
    hue="outcome",
    hue_order=["Survived", "Died"],
    palette=COLORS,
)

# Set the chart title.
plt.title("Survival Count by Sex")

# Label the horizontal axis with sex.
plt.xlabel("Sex")

# Label the vertical axis with the passenger count.
plt.ylabel("Count")

# Set the legend title.
plt.legend(title="Outcome")

# Save the sex chart and close the figure.
save_figure("04_survival_by_sex.png")


# --- 5. Extra plot: fare distribution by class ---

# Open a new figure for the fare chart.
plt.figure(figsize=(8, 5))

# Summarize the ticket fare in each class with a box plot.
# The box is the interquartile range. The line inside the box is the median.
sns.boxplot(data=df, x="class", y="fare", color="#4c78a8")

# Set the chart title.
plt.title("Fare Distribution by Class")

# Label the horizontal axis with passenger class.
plt.xlabel("Passenger Class")

# Label the vertical axis with the ticket fare.
plt.ylabel("Fare")

# Save the fare chart and close the figure.
save_figure("05_fare_by_class.png")


# Print the survivor and victim counts for each class.
print("Counts by class:")
print(pd.crosstab(df["class"], df["outcome"]))

# Print the survivor and victim counts for each deck.
print("Counts by deck:")
print(pd.crosstab(df["deck"], df["outcome"]))

# Print the survivor and victim counts for each sex.
print("Counts by sex:")
print(pd.crosstab(df["sex"], df["outcome"]))

# Print the age summary: count, mean, median, minimum, and maximum.
print("Age summary:")
print(df["age"].describe())

# Print the folder where the figures were saved.
print("Figures saved to:", FIGURE_DIR)
