import math
import numpy as np

class  MM:
      def absorb(self, a):
                return np.matrix([
                [a, 0, 0, 0],
                [0, a, 0, 0],
                [0, 0, a, 0],
                [0, 0, 0, a]])

      def LP(self, TA):
                TA = math.radians(TA)

                return 0.5*np.matrix([
                [1, np.cos(2*TA), np.sin(2*TA), 0],
                [np.cos(2*TA), np.cos(2*TA)**2, np.sin(2*TA)*np.cos(2*TA), 0],
                [np.sin(2*TA), np.sin(2*TA)*np.cos(2*TA), np.sin(2*TA)**2, 0],
                [0, 0, 0, 0]])

      def LD(self, TA, q, r):
                TA = math.radians(TA)

                return 0.5*np.matrix([
                [q+r, (q-r)*np.cos(2*TA), (q-r)*np.sin(2*TA), 0],
                [(q-r)*np.cos(2*TA), (q+r)*np.cos(2*TA)**2 + 2*((q*r)**(1/2))*(np.sin(2*TA)**2), (q+r-2*((q*r)**(1/2)))*np.sin(2*TA)*np.cos(2*TA), 0],
                [(q-r)*np.sin(2*TA), (q+r-2*((q*r)**(1/2)))*np.sin(2*TA)*np.cos(2*TA), (q+r)*np.sin(2*TA)**2 + 2*((q*r)**(1/2))*(np.cos(2*TA)**2), 0],
                [0, 0, 0, 2*((q*r)**(1/2))]])

      def CD(self, q, r):
                return 0.5*np.matrix([
                [q+r, 0, 0 , q-r],
                [0, 2*((q*r)**(1/2))],
                [0, 0, 2*((q*r)**(1/2)), 0],
                [q-r, 0, 0, q+r]])

      def LR(self, FA, ret):
                FA = math.radians(FA)
                ret = math.radians(ret)

                return np.matrix([
                [1, 0, 0, 0],
                [np.cos(2*FA)**2+(np.sin(2*FA)**2)*cos(ret), np.sin(2*FA)*np.cos(2*FA)*(1-np.cos(ret)), -np.sin(2*FA)*np.sin(ret)],
                [np.sin(2*FA)*np.cos(2*FA)*(1-np.cos(ret)), np.sin(2*FA)**2+(np.cos(2*FA)**2)*cos(ret), np.cos(2*FA)*np.sin(ret)],
                [0, np.sin(2*FA)*np.sin(ret), -np.cos(2*FA)*np.sin(ret), np.cos(ret)]])

      def CR(self, ret):
                ret = math.radians(ret)

                return np.matrix([
                [1, 0 ,0, 0],
                [0, np.cos(ret), np.sin(ret), 0],
                [0, -np.sin(ret), np.cos(ret), 0],
                [0, 0, 0, 1]])

      def idealdepol(self):
                return np.matrix([
                [0, 0, 0, 0]
                [0, 0, 0, 0]
                [0, 0, 0, 0]])

      def partdepol(self, d):
                return np.matrix([
                [1, 0, 0, 0],
                [0, d, 0, 0]
                [0, 0, d, 0]
                [0, 0, 0, d]])

      def S(self, s0, s1, s2, s3):
                return np.array([[s0], [s1], [s2], [s3]], dtype=float)

class Jones:
      def J(self, J0, J1):
                return np.array([[J0], [J1]], dtype=float)
