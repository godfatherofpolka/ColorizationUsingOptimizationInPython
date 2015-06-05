'''
Copyright 2014 Samuel Bucheli

This file is part of ColorizationUsingOptimizationInPython.

ColorizationUsingOptimizationInPython is free software: you can 
redistribute it and/or modify it under the terms of the 
GNU General Public License as published by the Free Software 
Foundation, either version 2 of the License, or (at your option) 
any later version.

ColorizationUsingOptimizationInPython is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY; without even 
he implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ColorizationUsingOptimizationInPython.  If not, see
<http://www.gnu.org/licenses/>.
'''

"""Helper functions to convert from RGB color space to YIQ color space and vice-versa.

Values for conversion matrices taken from http://en.wikipedia.org/wiki/YIQ#Formulas

"""

import numpy as np

def rgb2yiq(rgb):
  """Convert RGB image to YIQ image.

  Output values are restricted as follows
  .. math::
    Y \in [0,1]\\
    I \in [-0.5957,0.5957]\\
    Q \in [-0.5226,0.5226]

  Args:
    rgb (array_like): An array of shape (m,n,3) and type float.

  Returns:
    array_like: An array of the same shape as the input, colours converted to YIQ.
 
  """
  conv = np.array([[0.299,0.595716,0.211456],
                   [0.587,-0.274453,-0.522591],
                   [0.114,-0.321263,0.311135]])
  # convert
  yiq = np.dot(rgb, conv)
  # check boundaries
  y = yiq[:,:,0]
  i = yiq[:,:,1]
  q = yiq[:,:,2]
  y[y < 0] = 0
  y[y > 1] = 1
  i[i < -0.5957] = -0.5957
  i[i > 0.5957] = 0.5957
  q[q < -0.5226]  = -0.5226
  q[q > 0.5226] = 0.5226
  return yiq

def yiq2rgb(yiq):
  """Convert YIQ image to RGB image.

  Output values are restricted as follows
  .. math::
    R \in [0,1]\\
    G \in [0,1]\\
    B \in [0,1]\\


  Args:
    rgb (array_like): An array of shape (m,n,3) and type float.

  Returns:
    array_like: An array of the same shape as the input, colours converted to RGB.
 
  """
  conv = np.array([[1.0,1.0,1.0],
                   [0.9563,-0.2721,-1.1070],
                   [0.6210,-0.6474,1.7046]])
  # convert
  rgb = np.dot(yiq,conv)
  # check boundaries
  r = rgb[:,:,0]
  g = rgb[:,:,1]
  b = rgb[:,:,2]
  r[r < 0] = 0
  r[r > 1] = 1
  g[g < 0] = 0
  g[g > 1] = 1
  b[b < 0] = 0
  b[b > 1] = 1
  return rgb

