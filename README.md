# Colorization Using Optimization in Python

This code is a crude Python adaptation of
> Levin, Anat, Dani Lischinski, and Yair Weiss. 
> "Colorization using optimization." 
> In ACM Transactions on Graphics (TOG), vol. 23, no. 3, pp. 689-694. ACM, 2004.

For more details see http://www.cs.huji.ac.il/~yweiss/Colorization/

It works, but it's not very fast, there are probably various better ways to do this, in particular some vectorisation should be possible in order to improve the NumPy performance. 

Example files can be found at the URL given above (or for more fun, just create some yourself).

Example usage:
```
$ python colorizer.py inputGrey.png inputMarked.png output.png --view
```

## Usage Notes
* The front end (`colorizer.py`) requires [`argparse`](https://docs.python.org/3.4/library/argparse.html) and [`matplotlib`](http://matplotlib.org/) for loading, displaying, and saving the image.
* The back end (`colorizationSolver.py` and `colorConversion.py`) requires [`numpy`](http://www.numpy.org/) and [`scipy`](http://www.scipy.org/).
* It is possible to use the back end without the front end, simply use your favourite modules to load, save, and display images. Keep in mind, however, that the solver expects pixel values to be floating point numbers between 0 and 1. Some modules and filetypes (e.g. bitmap files) load pixel values as integers between 0 and 255. In this case, it is necessary to normalize the pixel values by dividing them by 255.
* When creating the color marks, make sure you use a hard, opaque brush, i.e. , the brush should have a precise border (and not fade out towards the border), as else the colorization solver will not work as expected, see [https://github.com/godfatherofpolka/ColorizationUsingOptimizationInPython/issues/2](https://github.com/godfatherofpolka/ColorizationUsingOptimizationInPython/issues/2).

### License

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

