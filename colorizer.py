#!/usr/bin/env python
"""A Python implementation of Colorization Using Optimization

This code is based on
  Levin, Anat, Dani Lischinski, and Yair Weiss. 
  "Colorization using optimization." 
  In ACM Transactions on Graphics (TOG), vol. 23, no. 3, pp. 689-694. ACM, 2004.
  http://www.cs.huji.ac.il/~yweiss/Colorization/

Example usage:
  $ python colorizer.py example.png example_marked.png output.png --view

"""
import argparse
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from colorizationSolver import colorize
                 
def main():
  parser = argparse.ArgumentParser(description='Colorize pictures')
  parser.add_argument('greyImage', help='png image to be coloured')
  parser.add_argument('markedImage', help='png image with colour hints')
  parser.add_argument('output', help='png output file')
  parser.add_argument('-v', '--view', help='display image', action='store_true')
  args = parser.parse_args()

  # Note: when reading .png, the division by 255. is not required
  greyImage = mpimg.imread(args.greyImage, format='png')
  markedImage = mpimg.imread(args.markedImage, format='png')
  
  colouredImage = colorize(greyImage, markedImage)
    
  mpimg.imsave(args.output,colouredImage, format='png')
  
  if args.view:
    plt.imshow(colouredImage)
    plt.show()
  
if __name__ == "__main__":
  main()
