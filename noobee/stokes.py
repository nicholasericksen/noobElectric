"""
Stokes vector calculations and formulation.

The degree of polarization (DOP) and degree of linear polarization (DOLP)
can be calculated for a given Stokes vector that describes an electromagnectic
wave. Stokes vectors can also be created and represented as numpy arrays.

Examples:
    >>> from noobee import stokes
    >>> S = stokes.s(1,0.5,0,0.5)
    >>> print S
    [[ 1. ]
     [ 0.5]
     [ 0. ]
     [ 0.5]]
    >>> print stokes.dop(S)
    [ 0.70710678]
    >>> print stokes.dolp(S)
    [ 0.5]
    >>> print stokes.docp(S)
    [ 0.5]
"""

import numpy as np

def s(s0, s1, s2, s3):
    """
    Stokes Vector

    Args:
        s0 (float): Intensity of the electromagnetic wave.
        S1 (float): Linear polarization component.
        s2 (float): Polarization difference between 45 and -45 degrees.
        s3 (float): Circular polarization component.

    Returns:
        array: A numpy array in the shape of a vector.
    """
    return np.array([[s0], [s1], [s2], [s3]], dtype=np.float)

def dop(S):
    """
    Degree of Polarization

    Args:
        S (array): vector shaped Stokes parameters.

    Returns:
        float: The percentage of total polarization.
    """
    return np.sqrt(S[1]**2 + S[2]**2 + S[3]**2) / S[0]


def dolp(S):
    """
    Degree of Linear Polarization

    Args:
        S (array): vector shaped Stokes parameters.

    Returns:
        float: The percentage of linear polarization.
    """
    return np.sqrt(S[1]**2 + S[2]**2) / S[0]

def docp(S):
    """
    Degree of Cicular Polarization

    Args:
        S (array): vector shaped Stokes parameters.

    Returns:
        float: The percentage of circular polarization.
    """
    return S[3] / S[0]
