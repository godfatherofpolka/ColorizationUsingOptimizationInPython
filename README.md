# Colorization Using Optimization in Python

This code is a crude Python adaptation of
> Levin, Anat, Dani Lischinski, and Yair Weiss. 
> "Colorization using optimization." 
> In ACM Transactions on Graphics (TOG), vol. 23, no. 3, pp. 689-694. ACM, 2004.
For more details see http://www.cs.huji.ac.il/~yweiss/Colorization/

It works, but it's not very fast, there are probably various better ways to do this, in particular some vectorisation should be possible in order to improve the NumPy performance. 

Example files can be found at the URL given above (or for more fun, just create some yourself).

Example usage:
  $ python colorizer.py example.png example_marked.png output.png --view
