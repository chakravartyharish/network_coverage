from fastapi import FastAPI, HTTPException
import httpx
from geopy.distance import geodesic
import pandas as pd
import logging
from fastapi import HTTPException
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path to the uploaded file
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'processed_data.csv')

# Loading processed data
try:
    processed_data = pd.read_csv(file_path)    
    logger.info(f"First few rows of processed data:\n{processed_data.head()}")
except FileNotFoundError:
    logger.error("Processed data file not found. Please run data_processing.py first.")
    exit()  # Exit the application if the file is not found
    
# Checking for NaN values in Longitude and Latitude
if processed_data[['Latitude', 'Longitude']].isnull().values.any():
    logger.error("DataFrame contains NaN values in Latitude or Longitude. Removing NaN values.")
    processed_data = processed_data.dropna(subset=['Latitude', 'Longitude'])
else:
    logger.info("No NaN values in Latitude or Longitude")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Network Coverage API"}

@app.get("/get_coverage")
async def get_coverage(address: str):
    if processed_data is None:
        raise HTTPException(status_code=500, detail="Processed data not available")
    coordinates = await convert_address_to_coordinates(address)
    if coordinates is None:
        raise HTTPException(status_code=404, detail="Address not found")
    
    coverage_data = find_nearest_coverage(coordinates)
    return coverage_data


# httpx to call the adresse.data.gouv.fr API
# Converting the address to coordinates  
async def convert_address_to_coordinates(address: str):
    api_url = f"https://api-adresse.data.gouv.fr/search/?q={address}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()

            # Assuming the first feature has the highest score
            top_feature = data['features'][0]

            # Check if the top feature's score is above a certain threshold
            if top_feature['properties']['score'] < 0.7:
                logger.error(f"Low confidence address: {address}")
                return None

            # Extract coordinates
            coordinates = top_feature['geometry']['coordinates']
            return {'longitude': coordinates[0], 'latitude': coordinates[1]}
        except httpx.HTTPStatusError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise HTTPException(status_code=424, detail=str(http_err))
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            raise HTTPException(status_code=500, detail=str(err))



# Function to find the nearest network coverage by operators
# from dataset based on the given coordinates
def find_nearest_coverage(coordinates, max_distance_km=1.0):
    # Filter data to get sites within the specified maximum distance
    filtered_data = processed_data.copy()
    filtered_data['Distance'] = processed_data.apply(
        lambda row: geodesic((coordinates['latitude'], coordinates['longitude']), (row['Latitude'], row['Longitude'])).kilometers,
        axis=1
    )
    nearby_sites = filtered_data[filtered_data['Distance'] <= max_distance_km]

    # Aggregate coverage data by operator
    coverage_by_operator = {}
    for operator in nearby_sites['Operateur'].unique():
        operator_data = nearby_sites[nearby_sites['Operateur'] == operator]
        coverage_by_operator[operator] = {
            '2G': bool(operator_data['2G'].max()),
            '3G': bool(operator_data['3G'].max()),
            '4G': bool(operator_data['4G'].max())
        }
    return coverage_by_operator
