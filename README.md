# Network Coverage API

## Introduction

This API provides network coverage information based on addresses.

## Installation

- Clone the repository: `git clone git@github.com:chakravartyharish/network_coverage.git`
- Install dependencies: `pip install -r requirements.txt`

## Running the App

- 1st run - python data_processing.py
- 2nd run - Python main.py
- Then Run the API server: `uvicorn main:app --reload`
- load in browser:
- http://127.0.0.1:8000/get_coverage?address=19+Rue+de+Malnoue%2C+93160+Noisy-le-Grand
- or this one http://127.0.0.1:8000/get_coverage?address=42+rue+du+Chemin+Vert+75011+Paris

## Usage

- To get network coverage: `GET /get_coverage?address=your_address_here`

## Testing

- Run tests using: `pytest`
