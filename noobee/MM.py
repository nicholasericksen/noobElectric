"""
Muller Matrix Polarimetric Devices and The Stokes Vector

This module provides standard optical elements useful in polarimetric applications.
The Mueller matrix is a 4x4 matrix used to classify a materials ability to
modify the polarization of incident light.  A Stokes vector is used for
quantifying the polarization state of an electromagnetic wave. Each MM and Stokes
vector should be normalized to 1.

The problem is defined in linear algebra as

    Sout = M * Sin

    |0|          |  1 -1  0  0 | |1|
    |0| =  1/2 * | -1  1  0  0 | |1|
    |0|          |  0  0  0  0 | |0|
    |0|          |  0  0  0  0 | |0|

Examples:
    >>> from noobelectric import mm
    >>> M = mm.lp(90)
    >>> print M
    [[ 0.5 -0.5  0.   0. ]
     [-0.5  0.5  0.   0. ]
     [ 0.   0.   0.   0. ]
     [ 0.   0.   0.   0. ]]
    >>> diatt, ret = mm.decompose(M)
    >>> print diatt
    [[ 1.  -0.5  0.   0. ]
     [-0.5  1.  -0.  -0. ]
     [ 0.  -0.   1.   0. ]
     [ 0.  -0.   0.   1. ]]
    >>> print ret
    [[ 1.   0.   0.   0. ]
     [ 0.   0.5  0.   0. ]
     [ 0.   0.   0.   0. ]
     [ 0.   0.   0.   0. ]]
"""

import math
import numpy as np

EPS = 0.000000001


def decompose(mm):
    #  TODO: check calculations, add depolarization
    """
    Mueller Matrix Decomposition

    Docomposition of Mueller Matrices using the Lu-Chipman decomposition in [1].

    [1] "Polarized Light", 3rd Edition. Goldstein.

    Args:
        mm (matrix): Mueller matrix to decompose.
    Returns:
        matrix, matrix: Two matrices representing the diattenuation and retardance
            Mueller matrices respectively.
    """
    D = mm[0,1]**2 + mm[0,2]**2 + mm[0,3]**2

    a = (1 - D)**(1/2)
    b = (1 - a) / D

    MM_diatt = np.matrix(
        [[1, mm[0,1], mm[0,2], mm[0,3]],
        [mm[0,1], a + b*mm[0,1]**2, b*mm[0,1]*mm[0,2], b*mm[0,1]*mm[0,2]],
        [mm[0,2], b*mm[0,2]*mm[0,1], a + b*mm[0,2]**2, b*mm[0,2]*mm[0,3]],
        [mm[0,3], b*mm[0,3]*mm[0,1], b*mm[0,3]*mm[0,2], a + b*mm[0,3]**2]]
    )

    MM_ret = np.matrix(
        [[a, 0, 0, 0],
        [0, mm[1,1] - b*mm[1,0]*mm[0,1], mm[1,2] - b*mm[1,0]*mm[0,2], mm[1,3] - b*mm[1,0]*mm[0,3]],
        [0, mm[2,1] - b*mm[2,0]*mm[0,1], mm[2,2] - b*mm[2,0]*mm[0,2], mm[2,3] - b*mm[2,0]*mm[0,3]],
        [0, mm[3,1] - b*mm[3,0]*mm[0,1], mm[3,2] - b*mm[3,0]*mm[0,2], mm[3,3] - b*mm[3,0]*mm[0,3]]]
    )

    return MM_diatt, MM_ret

def absorb(a):
    """
    Absorber

    Args:
        a (float): Value to attenuate the input Stokes beam.
    Returns:
        matrix: Mueller matrix of a diattenuator with a specified
            absorbtion coefficent.
    """
    MM = np.matrix([
    [a, 0, 0, 0],
    [0, a, 0, 0],
    [0, 0, a, 0],
    [0, 0, 0, a]])

    MM[np.abs(MM) < EPS] = 0

    return MM


def lp(TA):
    """
    Linear Polarizer

    Args:
        TA (float): Transmission axis angle of the linear polarizer in degrees.
    Returns:
        matrix: Mueller matrix representing a linear polarizer with Transmission
            axis at the given angle.
    """
    TA = math.radians(TA)

    MM = 0.5*np.matrix([
    [1, np.cos(2*TA), np.sin(2*TA), 0],
    [np.cos(2*TA), np.cos(2*TA)**2, np.sin(2*TA)*np.cos(2*TA), 0],
    [np.sin(2*TA), np.sin(2*TA)*np.cos(2*TA), np.sin(2*TA)**2, 0],
    [0, 0, 0, 0]])

    MM[np.abs(MM) < EPS] = 0

    return MM

def ld(TA, q, r):
    """
    Linear Diattenuator

    Args:
        TA (float): Transmission axis in degrees.
        q (float): Intensity transmittance.
        r (float): Intensity transmittane.
    Returns:
        matrix: Mueller matrix of a linear diatttenuator.
    """
    TA = math.radians(TA)

    MM = 0.5*np.matrix([
    [q+r, (q-r)*np.cos(2*TA), (q-r)*np.sin(2*TA), 0],
    [(q-r)*np.cos(2*TA), (q+r)*np.cos(2*TA)**2 + 2*((q*r)**(1/2))*(np.sin(2*TA)**2), (q+r-2*((q*r)**(1/2)))*np.sin(2*TA)*np.cos(2*TA), 0],
    [(q-r)*np.sin(2*TA), (q+r-2*((q*r)**(1/2)))*np.sin(2*TA)*np.cos(2*TA), (q+r)*np.sin(2*TA)**2 + 2*((q*r)**(1/2))*(np.cos(2*TA)**2), 0],
    [0, 0, 0, 2*((q*r)**(1/2))]])

    MM[np.abs(MM) < EPS] = 0

    return MM

def cd(q, r):
    """
    Circular Diattenuator

    Args:
        q (float): Intensity transmittance.
        r (float): Intensity transmittane.
    Returns:
        matrix: Mueller matrix of a circular diattenuator.
    """
    MM = 0.5*np.matrix([
    [q+r, 0, 0 , q-r],
    [0, 2*((q*r)**(1/2))],
    [0, 0, 2*((q*r)**(1/2)), 0],
    [q-r, 0, 0, q+r]])

    MM[np.abs(MM) < EPS] = 0

    return MM

def lr(FA, ret):
    """
    General Linear Retarder

    Args:
        FA (float): The fast axis of the waveplate.
        ret (float): The phase delay of the waveplate. Common values for this
            device are pi/2 for half waveplate and pi/4 for a quarter waveplate.
    Returns:
        matrix: Mueller Matrix of a linear retarder.
    """
    FA = math.radians(FA)
    ret = math.radians(ret)

    MM = np.matrix([
    [1, 0, 0, 0],
    [np.cos(2*FA)**2+(np.sin(2*FA)**2)*cos(ret), np.sin(2*FA)*np.cos(2*FA)*(1-np.cos(ret)), -np.sin(2*FA)*np.sin(ret)],
    [np.sin(2*FA)*np.cos(2*FA)*(1-np.cos(ret)), np.sin(2*FA)**2+(np.cos(2*FA)**2)*cos(ret), np.cos(2*FA)*np.sin(ret)],
    [0, np.sin(2*FA)*np.sin(ret), -np.cos(2*FA)*np.sin(ret), np.cos(ret)]])

    MM[np.abs(MM) < EPS] = 0

    return MM

def cr(ret):
    """
    Circular Retarder

    Args:
        ret: Phase delay
    Returns:
        matrix: The Mueller Matrix for circular retarder.
    """
    ret = math.radians(ret)

    MM = np.matrix([
    [1, 0 ,0, 0],
    [0, np.cos(ret), np.sin(ret), 0],
    [0, -np.sin(ret), np.cos(ret), 0],
    [0, 0, 0, 1]])

    MM[np.abs(MM) < EPS] = 0

    return MM

def depol(d):
    """
    Depolarizer

    Args:
        d (float): The amount of depolarization.  0 is a perfect depolarizer.
    Returns:
        matrix: Mueller matrix of a depolarizer.
    """
    MM = np.matrix([
    [1, 0, 0, 0],
    [0, d, 0, 0],
    [0, 0, d, 0],
    [0, 0, 0, d]])

    MM[np.abs(MM) < EPS] = 0

    return MM
