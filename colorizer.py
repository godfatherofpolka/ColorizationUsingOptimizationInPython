#!/usr/bin/env python

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

"""A Python implementation of Colorization Using Optimization

This code is based on
  Levin, Anat, Dani Lischinski, and Yair Weiss. 
  "Colorization using optimization." 
  In ACM Transactions on Graphics (TOG), vol. 23, no. 3, pp. 689-694. ACM, 2004.
  http://www.cs.huji.ac.il/~yweiss/Colorization/

Example usage:
  $ python colorizer.py inputGrey.png inputMarked.png output.png --view

"""
import argparse
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from colorizationSolver import colorize
                 
def main():
  # parse command line arguments
  parser = argparse.ArgumentParser(description='Colorize pictures')
  parser.add_argument('greyImage', help='png image to be coloured')
  parser.add_argument('markedImage', help='png image with colour hints')
  parser.add_argument('output', help='png output file')
  parser.add_argument('-v', '--view', help='display image', action='store_true')
  args = parser.parse_args()

  # Note: when reading .png, division by 255. is not required
  # Note: when reading .bmp, division by 255. is required
  # TODO: make this more universal, i.e., support various image formats
  # read images
  greyImage = mpimg.imread(args.greyImage, format='png')
  markedImage = mpimg.imread(args.markedImage, format='png')
  
  # colorize
  colouredImage = colorize(greyImage, markedImage)
    
  # save output
  mpimg.imsave(args.output,colouredImage, format='png')
  
  # display output, if requested
  if args.view:
    plt.imshow(colouredImage)
    plt.show()
  
if __name__ == "__main__":
  main()
