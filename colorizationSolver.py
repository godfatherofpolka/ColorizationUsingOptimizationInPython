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

import math
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.linalg import lsqr

from colorConversion import rgb2yiq, yiq2rgb

def getWeights(neighbourhood,centerIndex):
  """Calculates weights of neighbours.

  See http://www.cs.huji.ac.il/~yweiss/Colorization/ 

  The following formula is used

  .. math::
    w_rs = e^{-(Y(s)-Y(r))^2 / 2\sigma_r^2}

  where r is the index of the center, s the index of a neighbour and 
  sigma_r is the variance in a neighbourhood around r.
    
  Args:
    neighbourhood (array_like): array of intensities of neighbours of shape (m,n) including "center".
    centerIndex: index of the "center" in neighbourhood array.

  Returns:
    array_like: array weights for neighbours of shape (m*n-1).

  """
  # get Y(r)
  centerValue = neighbourhood[centerIndex]
  # calculate variance and sigma
  variance = np.mean((neighbourhood - np.mean(neighbourhood))**2)
  sigma = 0.6 * variance
  # calculate index of center in flattened array
  flatCenterIndex = np.ravel_multi_index(centerIndex, dims=neighbourhood.shape)
  # remove center from neighbourhood, get just the neighbours 
  neighbours = np.delete(neighbourhood, flatCenterIndex)
  # making some numbers nicer
  # (the first was part of the original Matlab code and does not seem to have much effect)
  '''
  mgv = np.min((neighbours-centerValue)**2)
  if sigma < (-mgv/math.log(0.01)):
    sigma = -mgv/math.log(0.01)
  '''
  if sigma < 0.000002:
    sigma = 0.000002
  weights = np.zeros(neighbours.shape)
  # calculate the weights
  weights = np.exp(-(((neighbours-centerValue)**2)/sigma))
  # normalize
  weights = weights/np.sum(weights)
  return weights


def getColorization(hasColor, luma, chromaI, chromaQ, neighbourRadius = 1):
  """Solves the minimization problem induced by the marked image.

  See http://www.cs.huji.ac.il/~yweiss/Colorization/ 

  Given monochromatic luminance Y and  The aim is to minimize

  .. math::
    J(X) = \sum_r \left( X_r - \sum_{s \in N(r)} w_{rs} X_s \right)^2

  for X=I and X=Q, where I and Q are the chrominance channels of the output image 
  and N(r) denotes a neighbourhood around r.

  This is done by solving the following set of linear equations:
  .. math::
    X_r - \sum_{s \in N(r)} w_{rs} X_s = 0

  where no constraints are given by markings and additionally

  .. math::
    X_r = I_r

  or

  .. math::
    X_r = Q_r

  for the constraints given by the markings for the chrominance channels I and Q,
  respectively.

  Given an input image of size (m,n), the majority of the code below sets up 
  this system of linear equations, resulting in a sparse matrix A of size (m*n, m*n).
  The system is then solved using scipy.sparse.linalg.spsolve
    
  Args:
    hasColor (array_like): array of shape (height, width) of type bool indicating color constraints given by markings.
    luma (array_like): array of shape (height, width) of type bool specifying the monochromatic luminance channel.
    chromaI (array_like): array of shape (height, width) of type bool specifying the I chrominance channel given by the markings.
    chromaQ (array_like): array of shape (height, width) of type bool specifying the Q chrominance channel given by the markings. 
    neighbourRadius (int): size of neighbourhoods for weight calculation (default 1)

  Returns:
    array_like: colorized picture in YIQ format.

  """
  # image dimensions
  (height, width) = luma.shape
  imageSize = height*width
  
  #variance = ndimage.generic_filter(luma, np.var, footprint=np.array([[1,1,1],[1,1,1],[1,1,1]]))

  # set up storage for result
  result = np.empty( luma.shape + (3,) )
  # luminance channel of result is the same as given
  result[:,:,0] = luma

  # enumerate indices
  imageIndices = np.arange(0,imageSize).reshape((height,width))

  # neighbourhood size
  numberOfNeighbours = (2*neighbourRadius+1)**2
  # maximal size of the indices and values arrays
  indicesSize = imageSize*numberOfNeighbours
  # data structures for creating sparse csr matrix
  columnIndices = np.zeros(indicesSize, dtype=np.int)
  # in case a sparse.coo_matrix is desired instead
  #rowIndices = np.zeros(indicesSize, dtype=np.int)
  indicesPointer = np.zeros(indicesSize, dtype=np.int)
  values = np.zeros(indicesSize)
 
  # to keep track of current position in columnIndices and values
  pos = 0
  # current row in sparse matrix
  row = 0
  for (i,j), value in np.ndenumerate(luma):
    # calculate weights if no color is assigned
    if not hasColor[i,j]:
      # some numpy slicing to get neighbours
      neighbourSlice = np.s_[max(0,i-neighbourRadius):min(i+neighbourRadius+1,height),max(0,j-neighbourRadius):min(j+neighbourRadius+1,width)]
      # indices of the neighbours, i.e., N(r) (but including center)
      neighbourIndices = imageIndices[neighbourSlice]
      # luminance of neighbours (including center)
      neighbours = luma[neighbourSlice]
      # index of the center, i.e., r
      centerIndex = np.where(neighbourIndices==imageIndices[(i,j)])
      # calculate weights
      weights = -getWeights(neighbours, centerIndex)
      # TODO: store calculated weights more elegantly
      neighbourCount = 0
      # store weights in sparse matrix
      for (ii,jj), index in np.ndenumerate(neighbourIndices):
        if not (ii,jj)==centerIndex:
          #rowIndices[pos] = row
          columnIndices[pos] = index
          values[pos] = weights[neighbourCount]
          pos += 1
          neighbourCount += 1
    
    # matrix entry for current pixel, it's always 1
    #rowIndices[length] = rowCounter
    columnIndices[pos] = imageIndices[i,j]
    values[pos] = 1

    pos += 1    
    row += 1
    indicesPointer[row] = pos
    
  # trim arrays to actually used lengths (pixels near the border do not have a "full" neighbourhood), this probably could be avoided with some clever thinking
  #rowIndices = rowIndices[0:length+1]
  columnIndices = columnIndices[0:pos+1]
  indicesPointer = indicesPointer[0:row+1]
  values = values[0:pos+1]

  # create sparse matrix
  A = sparse.csr_matrix( (values,columnIndices,indicesPointer), 
                         shape=(row, imageSize))
  #A = sparse.coo_matrix( (values, (rowIndices, columnIndices)),
  #                      shape=(rowCounter, imageSize)).tocsc()

  # enumeration of indices where color is already given
  coloredIndices = hasColor.flatten().nonzero()

  # constraints given by markings
  bI = np.zeros(row)
  bQ = np.zeros(row)
  bI[coloredIndices] = chromaI.flatten()[coloredIndices]
  bQ[coloredIndices] = chromaQ.flatten()[coloredIndices]

  # solve system of linear equations
  result[:,:,1] = spsolve(A,bI).reshape(height,width)
  result[:,:,2] = spsolve(A,bQ).reshape(height,width)

  #result[:,:,1] = lsqr(A,bI)[0].reshape(height,width)
  #result[:,:,2] = lsqr(A,bQ)[0].reshape(height,width)

  # done, yay!
  return result

def colorize(greyImage, markedImage):
  """Colorizes a given monochrome image using given markings as constraints.

  Args:
    greyImage (array_like): monochrome image in RGB format as array of shape (height, width,3) of type float.
    markedImage (array_like): image in RGB format as array of shape (height, width, 3) giving coloring constraints.

  Returns:
    array_like: colorized image as array of shape (height,width,3) of type float.

  """
  # calculate color mask, i.e., where are constraints given
  hasColor = np.sum(abs(greyImage - markedImage),axis=2) > 0.01
  # extract chroma and luma layers
  luma = rgb2yiq(greyImage)[:,:,0]
  chromaI = rgb2yiq(markedImage)[:,:,1]
  chromaQ = rgb2yiq(markedImage)[:,:,2]
  # call solver
  colouredImageYUV = getColorization(hasColor, luma, chromaI, chromaQ)
  # convert to RGB and return
  return yiq2rgb(colouredImageYUV)

