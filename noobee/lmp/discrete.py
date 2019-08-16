import numpy as np

from .utils import divide

def discrete(H, V, P, M):
    S1 = divide((Hraw - Vraw), (Hraw + Vraw))
    S2 = divide((Praw - Mraw), (Praw + Mraw))
