# Ghost Imaging Analysis Tool

## Overview
This tool processes and plots raw data from our lab's Quantum Ghost Imaging (QGI) setup. 

The raw data consists in a collection of text files: 1 text file per pixel containing a column vector of 4096 values. 
These values are the number of coincidence counts recorded during each time bin. The bin width is defined by the coincidence window (default 50ns) divided by ADC_resolution (default 2^10).

The script loads the data, performs a frequency analysis to identify the time bins that are the most likely to contain actual coincidence detection events and reduce noise. The selection is made by fitting a Gaussian and selecting time bins in the range µ±2σ.

## Features
- Data loading from CSV files
- Frequency analysis
- Filtering based on Gaussian parameters
- Visualization of average images and distributions

## Requirements
- numpy
- matplotlib
- scipy
- glob
- re

## Usage
- Place your QGI data files in the data directory
- Update the data_path variable in the script
- Run the script:
python QGI_data_cleaner.py

## Data Format
Input files should be CSV format with naming convention: x_y_0 where x and y are integer coordinates

## Example
<img width="290" alt="image" src="https://github.com/user-attachments/assets/005c98ed-7911-4597-8a73-cea03960c6c0" />
