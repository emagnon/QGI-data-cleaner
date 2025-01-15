#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: elie
"""

import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import re
from scipy import optimize

def gaussian(x, amplitude, mean, stddev):
    """
    Returns a Gaussian distribution with the given amplitude, mean, and standard deviation.
    """
    return amplitude * np.exp(-((x - mean) / 4 / stddev)**2)

# Set the path to the data directory
data_path = 'data/'

# Find all CSV files matching the pattern: x_y_0
files = [f for f in glob('[0-9]*_[0-9]*_0', root_dir=data_path) if re.match(r'^\d+_\d+_0$', f)]

# Extract x and y values from filenames
x_values = set()
y_values = set()
for file in files:
    x, y, _ = file.split('_')
    x_values.add(int(x))
    y_values.add(int(y))

max_x = max(x_values)
max_y = max(y_values)

print(f"Maximum x and y values: {max_x}, {max_y}")

data = np.zeros((max_x + 1, max_y + 1, 4096))

for file in files:
    x, y, _ = file.split('_')
    x, y = int(x), int(y)
    data[x, y, :] = np.genfromtxt(data_path + file, delimiter=',')

# Reduce data to non-zero values
deepest_index = np.max(np.argwhere(data!= 0)[:, 2])
data = data[:, :, :deepest_index + 1]

# Calculate average values for each pixel
avg_2D = np.mean(data, axis=2)

# Calculate average values for the entire image
avg_values = np.mean(data, axis=(0, 1))

# Fit a Gaussian distribution to the average values
x = np.arange(0, deepest_index + 1)
if deepest_index + 1 == 1024:
    x = np.arange(0, 256)
popt, _ = optimize.curve_fit(gaussian, x, avg_values)
print(f"Gaussian fit parameters: {popt}")

# Plot average values
plt.imshow(avg_2D)
plt.title('Average Picture')
plt.show()

plt.plot(avg_values)
plt.title('Average Values')
plt.xlabel('Index')
plt.ylabel('Average Value')
plt.plot(x, gaussian(x, *popt))
plt.tight_layout()
plt.show()

# Use the Gaussian fit to filter the image
mu = popt[1]
stdev = popt[2]
sel_range = np.array([np.floor(mu - 2 * stdev), np.ceil(mu + 2 * stdev)], dtype='int')
data = data[:, :, sel_range[0]:sel_range[1]]
print(f"Selected range: {sel_range}")

# Calculate average values for the filtered image
avg_2D = np.mean(data, axis=2)

#np.save('data.npy',avg_2D)

plt.imshow(avg_2D)
plt.title('Average Picture Filtered')
plt.colorbar()
plt.show()
