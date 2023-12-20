import pandas as pd
from pyproj import Transformer
import os

# Define the path to the uploaded file
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'Data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv')
print("File path set.")

# Function to convert Lambert93 to GPS coordinates
def lamber93_to_gps(x, y):
    transformer = Transformer.from_crs("epsg:2154", "epsg:4326", always_xy=True)
    long, lat = transformer.transform(x, y)
    return long, lat

# Function to process a chunk of data
def process_chunk(chunk, chunk_id):
    print(f"Processing chunk {chunk_id}...")
    chunk['Longitude'], chunk['Latitude'] = zip(*chunk.apply(lambda row: lamber93_to_gps(row['x'], row['y']), axis=1))
    print(f"Chunk {chunk_id} processed.")
    return chunk

# Read the CSV in chunks (adjust the chunksize as needed)
chunksize = 10000  # chunk size, adjust based on your system's capability
chunks = pd.read_csv(file_path, delimiter=';', chunksize=chunksize)
print("CSV reading initiated in chunks.")

# Process each chunk
processed_chunks = []
for i, chunk in enumerate(chunks):
    processed_chunk = process_chunk(chunk, i+1)
    processed_chunks.append(processed_chunk)

processed_data = pd.concat(processed_chunks)
print("All chunks processed and concatenated.")

# Mapping operator codes to names for better readability
operator_mapping = {
    20801: 'Orange',
    20810: 'SFR',
    20815: 'Free',
    20820: 'Bouygues'
}
processed_data['Operateur'] = processed_data['Operateur'].map(operator_mapping)
print("Operator codes mapped to names.")

# Basic data analysis
operator_counts = processed_data['Operateur'].value_counts()
network_availability = processed_data[['2G', '3G', '4G']].sum()
print("Basic data analysis completed.")

# Displaying the first few rows of the dataset and some basic analysis
print("First few rows of processed data:\n", processed_data.head())
print("\nOperator Counts:\n", operator_counts)
print("\nNetwork Availability:\n", network_availability)

# Save Processed Data to CSV
processed_data.to_csv('processed_data.csv', index=False)


# you will get output like this in 2-3 minutes depending on your computer performance:
# (papernest) PS C:\Users\hkcha\OneDrive\Desktop\papernest> python .\data_processing.py
# File path set.
# CSV reading initiated in chunks.
# Processing chunk 1...
# Chunk 1 processed.
# Processing chunk 2...
# Chunk 2 processed.
# Processing chunk 3...
# Chunk 3 processed.
# Processing chunk 4...
# Chunk 4 processed.
# Processing chunk 5...
# Chunk 5 processed.
# Processing chunk 6...
# Chunk 6 processed.
# Processing chunk 7...
# Chunk 7 processed.
# Processing chunk 8...
# Chunk 8 processed.
# All chunks processed and concatenated.
# Operator codes mapped to names.
# Basic data analysis completed.
# First few rows of processed data:
#    Operateur         x          y  2G  3G  4G  Longitude   Latitude
# 0    Orange  102980.0  6847973.0   1   1   0  -5.088856  48.456575
# 1       SFR  103113.0  6848661.0   1   1   0  -5.088018  48.462854
# 2  Bouygues  103114.0  6848664.0   1   1   1  -5.088009  48.462882
# 3    Orange  112032.0  6840427.0   0   1   1  -4.956782  48.397297
# 4    Orange  115635.0  6799938.0   1   1   0  -4.854029  48.038050

# Operator Counts:
#  Operateur
# Orange      24612
# SFR         21449
# Bouygues    18816
# Free        12271
# Name: count, dtype: int64

# Network Availability:
#  2G    57565
# 3G    72338
# 4G    50772
# dtype: int64