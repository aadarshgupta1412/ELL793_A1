# -*- coding: utf-8 -*-
"""ELL793_Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KC722hhzN64-mwXod5UWUdXggeNYDR1y

## **Assignment 1**
"""

import numpy as np
import pandas as pd
import io
import math
import cv2
import os
import glob
from scipy import linalg
from numpy.linalg import svd
import scipy
import mpmath

def adc(data): #gives Average Distance and Centre
  avg_dist = 0
  num_points = data.shape[0]
  centre = np.mean(data, axis=0)
  for x in data:
    avg_dist += np.linalg.norm(x-centre)
  avg_dist/=num_points
  return avg_dist, centre

def normalize(data, value):

  def norm_matrix(data, value):
    dist, centre = adc(data)
    if data.shape[1] == 2:
      T = np.array([[1, 0, -1*centre[0]], [0, 1, -1*centre[1]], [0, 0, 1]])
    else:
      T = np.array([[1, 0, 0, -1*centre[0]], [0, 1, 0, -1*centre[1]], [0, 0, 1, -1*centre[2]], [0, 0, 0, 1]])
    T*=value/dist
    v = data.shape[1]
    T[v, v] = 1
    return T

  def normalized_coord(data, value):
    T = norm_matrix(data, value)
    num_points = data.shape[0]
    a1 = [np.ones(num_points)]
    coord = np.append(data.T, a1, axis = 0)
    xnew = np.dot(T, coord)
    c2 = np.mean(data, axis=0)
    normalised_coord = xnew[0:data.shape[1]].T
    return normalised_coord

  T = norm_matrix(data, value)
  datan = normalized_coord(data, value)
  return T, datan

def estimate_P(x, X, T, U):
  num_points = X.shape[0]
  X = np.append(X, np.ones((num_points, 1)), axis = 1)
  x = np.append(x, np.ones((num_points, 1)), axis = 1)
  ax = np.append(-X,np.zeros((X.shape[0],4)), axis = 1)
  ax = np.append(ax,x[:,0][:, np.newaxis]*X, axis = 1)
  ay = np.append(np.zeros((X.shape[0],4)),-X, axis = 1)
  ay = np.append(ay,x[:,1][:, np.newaxis]*X, axis = 1)
  M = np.append(ax,ay, axis = 1).reshape(2*X.shape[0],12)
  M = -1*M
  u, s, vh = svd(M)
  v = vh.T
  p = v[:,-1]
  Pn = p.reshape(3,4)
  P = np.dot(Pn, U)
  P = np.dot(np.linalg.inv(T), P)
  return Pn, P

def parameters(P):
  m = P[:,0:3]
  K, R = scipy.linalg.rq(m) 
  X0 = -np.linalg.inv(m)@P[:,-1]
  return K, R, X0

def predict(P, X):
  Xtest = np.append(X, np.ones((X.shape[0],1)), axis=1)
  xtest = P@Xtest.T
  xtest = xtest/xtest[2]
  xtest = xtest[0:2].T
  return xtest

def get_rmse(xtest, x):
    return np.sqrt(np.mean((xtest-x)**2))

def get_parameters(P):
    A = P[:,0:3]
    b = P[:,-1]
    epsilon = -1
    rho = epsilon/np.linalg.norm(A[2])
    x0 = rho*rho*np.dot(A[0],A[2])
    y0 = rho*rho*np.dot(A[1],A[2])
    a1_a3 = np.cross(A[0],A[2])
    a2_a3 = np.cross(A[1],A[2])
    cos_theta = (-1)*np.dot(a1_a3, a2_a3)/(np.linalg.norm(a1_a3)*np.linalg.norm(a2_a3))
    theta = math.acos(cos_theta)*180/math.pi
    sin_theta = math.sin(theta*math.pi/180)
    alpha = rho*rho*np.linalg.norm(a1_a3)*sin_theta
    beta = rho*rho*np.linalg.norm(a2_a3)*sin_theta
    K = np.array([[alpha, (-1)*alpha*cos_theta/sin_theta, x0], [0, beta/sin_theta, y0], [0, 0, 1]])   
    r3 = rho*A[2]
    r1 = a2_a3/np.linalg.norm(a2_a3)
    r2 = np.cross(r3, r1)
    R = np.empty((0,3))
    R = np.append(R, r1.reshape((1,3)), axis=0)
    R = np.append(R, r2.reshape((1,3)), axis=0)
    R = np.append(R, r3.reshape((1,3)), axis=0)
    t = rho*np.dot(np.linalg.inv(K), b)   
    print('K:', K, '\n')
    print('R:', R, '\n')
    print('t:', t,'\n')
    return alpha, beta, theta, rho, x0, y0, K, R, t

"""# Upload file"""

X = np.array([[0, 2, 2], [0, 2, 1], [0, 2, 0],[1, 2, 0],[2, 2, 0],[0, 1, 2],[0, 1, 1],[0, 1, 0],[1, 1, 0],[2, 1, 0], [0, 0, 2],[0, 0, 1],[0, 0, 0],[1, 0, 0],[2, 0, 0]])

from google.colab import files
uploaded = files.upload()
x1 = np.loadtxt('img1.txt')
x2 = np.loadtxt('img2.txt')
x3 = np.loadtxt('img3.txt')
x4 = np.loadtxt('img4.txt')
x5 = np.loadtxt('img5.txt')
x6 = np.loadtxt('img6.txt')
x7 = np.loadtxt('img7.txt')
x8 = np.loadtxt('img8.txt')
x9 = np.loadtxt('img9.txt')
x10 = np.loadtxt('img10.txt')
x11 = np.loadtxt('img11.txt')
x12 = np.loadtxt('img12.txt')
x13 = np.loadtxt('img13.txt')
x14 = np.loadtxt('img14.txt')
x15 = np.loadtxt('img15.txt')

x = (x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15)

rmse, alpha, beta, theta, rho, x0, y0 = [0]*15, [0]*15, [0]*15, [0]*15, [0]*15, [0]*15, [0]*15

for i in range(len(x)):
  print('Performing camera calibration for Image', i+1)
  T, xn = normalize(x[i], math.sqrt(2))
  U, Xn = normalize(X, math.sqrt(3))
  Pn, P = estimate_P(xn, Xn, T, U)
  K, R, X0 = parameters(P)
  xtest = predict(P, X)
  rmse[i] = get_rmse(xtest, x[i])
  alpha[i], beta[i], theta[i], rho[i], x0[i], y0[i], K, R, t = get_parameters(P)

def averaged_parameters():

  def avg(x):
    s = 0
    for i in range(len(x)):
      s+=x[i]
    return s/len(x)
  error = avg(rmse)
  i1 = avg(alpha)
  i2 = avg(beta)
  i3 = avg(theta)
  i4 = avg(x0)
  i5 = avg(y0)
  e1 = avg(rho)
  print('Averaged RMSE error :', error)
  print('alpha:', i1)
  print('beta:', i2)
  print('theta:', i3)
  print('x0:', i4)
  print('y0:', i5)
  print('rho (scaling factor):', e1)

averaged_parameters()