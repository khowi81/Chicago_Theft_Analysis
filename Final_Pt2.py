import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the dataset
file_path = r"C:\Users\khowi\Desktop\CS322\Final_Project\Crimes_-_2001_to_Present_20241113.csv"
df = pd.read_csv(file_path)

# Step 2: Select relevant columns
columns_needed = ['Date', 'Primary Type', 'Location Description', 'Ward', 'Community Area']
df = df[columns_needed]

# Step 3: Filter by time range (2013–2023)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Coerce invalid dates to NaT
df = df.dropna(subset=['Date'])  # Drop rows with invalid or missing dates
df = df[(df['Date'].dt.year >= 2013) & (df['Date'].dt.year <= 2023)]

# Step 4: Focus on Theft and Motor Vehicle Theft
filtered_crimes = df[df['Primary Type'].str.contains('Theft|Motor Vehicle Theft', case=False, na=False)]
filtered_crimes = filtered_crimes[
    filtered_crimes['Location Description'].str.contains(
        'Sidewalk|Alley|Street|Retail|CTA', case=False, na=False
    )
]

# Handle missing values
filtered_crimes['Ward'] = filtered_crimes['Ward'].fillna(-1)
filtered_crimes['Community Area'] = filtered_crimes['Community Area'].fillna(-1)

# Analysis - Overall Probabilities
total_records = len(filtered_crimes)
primary_type_probs = filtered_crimes['Primary Type'].value_counts() / total_records
location_probs = filtered_crimes['Location Description'].value_counts() / total_records

# Analysis - Ward-Level Probabilities
primary_type_by_ward = filtered_crimes.groupby(['Ward', 'Primary Type']).size() / filtered_crimes.groupby('Ward').size()
primary_type_by_ward = primary_type_by_ward.reset_index(name='Probability')

location_by_ward = filtered_crimes.groupby(['Ward', 'Location Description']).size() / filtered_crimes.groupby('Ward').size()
location_by_ward = location_by_ward.reset_index(name='Probability')

# Save results
primary_type_probs.to_csv("primary_type_probs.csv", header=True)
location_probs.to_csv("location_probs.csv", header=True)
primary_type_by_ward.to_csv("primary_type_probs_by_ward.csv", index=False)
location_by_ward.to_csv("location_probs_by_ward.csv", index=False)

# Visualizations
# Visualization 1: Bar Chart for Primary Type Probabilities
plt.figure(figsize=(8, 6))
primary_type_probs.plot(kind='bar', legend=False, color=['blue', 'orange'])
plt.title('Overall Probabilities by Primary Type')
plt.xlabel('Primary Type')
plt.ylabel('Probability')
plt.xticks(rotation=0)
plt.savefig('primary_type_probabilities.png')
plt.show()

# Visualization 2: Bar Chart for Location Description Probabilities
plt.figure(figsize=(10, 8))
location_probs.sort_values(ascending=False).plot(kind='bar', legend=False, color='green')
plt.title('Overall Probabilities by Location Description')
plt.xlabel('Location Description')
plt.ylabel('Probability')
plt.xticks(rotation=45, ha='right')
plt.savefig('location_description_probabilities.png')
plt.show()

# Visualization 3: Stacked Bar Chart for Ward-Level Primary Type Probabilities
pivot_primary_type = primary_type_by_ward.pivot(index='Ward', columns='Primary Type', values='Probability')
pivot_primary_type.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Ward-Level Probabilities by Primary Type')
plt.xlabel('Ward')
plt.ylabel('Probability')
plt.legend(title='Primary Type')
plt.savefig('ward_primary_type_probabilities.png')
plt.show()

# Visualization 4: Heatmap for Ward and Location Description
pivot_location = location_by_ward.pivot(index='Ward', columns='Location Description', values='Probability')
plt.figure(figsize=(12, 10))
sns.heatmap(pivot_location, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Heatmap of Ward and Location Description Probabilities')
plt.xlabel('Location Description')
plt.ylabel('Ward')
plt.savefig('ward_location_heatmap.png')
plt.show()

print("\nAll probability results and visualizations have been saved successfully.")
