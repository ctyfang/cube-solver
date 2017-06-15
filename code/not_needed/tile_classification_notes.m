Detection of Colors using Machine Vision

Current method in-use may be unreliable, as seen by test images. The algorithm
currently takes a cropped image of the cubeface, then proceeds to divide the image
into a three-by-three grid.

The algorithm then cycles through each tile in the two-dimensional grid, summing
the total values for R, G, and B in all pixels within the tile. The tile's color
is decided using the ratios between these sums (red_sum, blue_sum, green_sum)

An alternative method exists using color boundaries. A boundary is defined by 
two tuples, lower = [R1, G1, B1], upper = [R2, G2, B2]. If a pixel's RGB tuple
lies within these bounds, it receives that tuple's corresponding classification.
With this method, lies the inherent challenge of rgb boundary calibration.
This can be done by eye by using the extents of each color as its bounds
(For instance, using the lightest and darkest shades of a color). Neural networks
may also be an option.

Another method may be machine learning. If the images of tiles can be rescaled,
we can fix the Number of Features (n), where the features would simply be an
unrolled vector containing all RGB values of all pixels in a tile. One example
of an ML algorithm that could work would be Multiclass Logistic Regression via 
the One vs. All method. Training examples would contain images of tiles under
different lighting conditions, re-scaled from different initial dimensions,
with different angular offsets, etc. Six different models would be needed for
each color, then the model with the greatest output p would be used to classify
the tile.

***
Moving forward, a camera setup should be decided and the current algorithm 
evaluated. If its performance fails to be adequate, these other options should
be explored.