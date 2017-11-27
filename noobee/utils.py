"""
Utilities for working with datasets.

These functions are intended to be used to quickly work with datasets that contain
numerous samples.  Basic statistics, histogram binning, etc. are provided for
conveniance.

Author: Nicholas Ericksen
"""

def datasummary(data):
    """
    Provides the max, min, mean, standard deviation, and number of data points
    for a given dataset.

    Args:
    data (array): an array of histogram data. [[1,99], [0.9, 35], ...]

    Returns:
    dictionary: summary of a given histogram.
    """
    maxValue = np.amax(data)
    minValue = np.amin(data)
    length = len(data)
    mean = np.mean(data)
    std = np.std(data)

    return {
        "max": maxValue,
        "min": minValue,
        "mean": mean,
        "std": std,
        "numpts": length
    }

def createhistogram(data, bins):
    """
    A function for putting a raw dataset into histogrgam bins.

    Args:
        data (array): raw set of data to be binned. [34, 54, 45.5, ...]
        bins (int): the number of bins to create.

    Returns:
        array: zipped values for each bin.
    """
    hist = np.histogram(data, bins=bins, density=True)
    bins = hist[1].tolist()
    values = hist[0].tolist()

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values)]

    return zipped


def divide( a, b ):
    """
    A function to handle dividing by zero.  The result will not be infinitey, but
    rather it will be zero.

    Args:
        a (float): numerator of the division.
        b (float): denominator of the division.

    Returns:
        array: corrected array with Nan, inf, -inf values replaced with 0.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = 0  # -inf inf NaN
    return c
