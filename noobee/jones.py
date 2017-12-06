"""
Jones Vectors and Common Optical Devices

Representation of pure polarization states using Jones matrices.  Common optical
devices such as the Quarter waveplates (QWP), Half waveplates (HWP) and linear polarizers (LP).

Examples:

"""

import numpy as np
import math

EPS = 0.000000001

def j(j0, j1):
    """
    Jones Vector

    Args:
        j0 (float): Jones vector parameter.
        j1 (float): Jones vector parameter.

    Returns:
        array: Jones vector numpy array.
    """
    return np.array([[j0], [j1]])

def lp(phi):
    """
    General Linear Polarizer

    Args:
        phi (float): Transmission axis is degrees relative
            to the X axis.

    Returns:
        array: Jones matrix
    """
    a = np.power(np.cos(phi), 2)
    b = np.sin(phi)*np.cos(phi)
    c = np.sin(phi)*np.cos(phi)
    d = np.power(np.sin(phi), 2)

    return np.matrix([[a,b], [c,d]])

def lph():
    """
    Linear Polarizer with transmission axis at 0 degrees.

    Returns:
        array: numpy array representation for LPH.
    """
    return np.matrix([[1,0], [0,0]])

def lpv():
    """
    Linear Polarizer with transmission Axis at 90 degrees.

    Returns:
        array: numpy array representation of LPV.
    """
    return np.matrix([[0,0], [0,1]])

def lp45():
    """
    Linear Polarizer with transmission axis at 45 degress.

    Returns:
        array: numpy array representation for LP45.
    """
    return 0.5 * np.matrix([[1,1],[1,1]])

def lp135():
    """
    Linear Polarizer with transmission axis at 135 degrees.

    Returns:
        array: numpy array representation for LP135.
    """
    return 0.5 * np.matrix([[1,-1], [-1,1]])

def rcp():
    """
    Right Circular Polarizer

    Returns:
        array: numpy array representation for RCP.
    """
    return 0.5 * np.matrix([[1,1j],[-1j, 1]])

def lcp():
    """
    Left Circular Polarizer

    Returns:
        array: numpy array representation for a LCP.
    """
    return 0.5 * np.matrix([[1,-1j], [1j, 1]])

def qwp(theta):
    """
    Quarter Waveplate

    Args:
        theta (float): Angle of the fast axis of waveplate.

    Returns:
        array: numpy representation of QWP.
    """
    theta = math.radians(theta)

    QWP =  np.exp(1j*np.pi/4)*np.matrix([[np.cos(theta)**2 + 1j*np.power(np.sin(theta), 2), (1-1j)*np.cos(theta)*np.sin(theta) ],
    [(1-1j)*np.cos(theta)*np.sin(theta), np.sin(theta)**2 + 1j*np.power(np.cos(theta), 2)]])

    QWP[np.abs(QWP) < EPS] = 0

    return QWP

def hwp(theta):
    """
    Half Waveplate

    Args:
        theta (float): Angle of the fast axis of a waveplate.

    Returns:
        array: numpy representation of HWP.
    """
    theta = math.radians(theta)

    HWP = np.matrix([[np.cos(2*theta), np.sin(2*theta)],
    [np.sin(2*theta), -np.cos(2*theta)]])

    HWP[np.abs(HWP) < EPS] = 0

    return HWP
