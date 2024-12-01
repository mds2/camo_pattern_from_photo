Create camo patterns from natural photographs
======================

Creates "camouflage" patterns inspired by the color pallettes of input images.

Uses k-means clustering to extract the color palette, and perlin noise to drive the shape of the "camouflage" patterns.

For sample output, see folder `examples`.

How to use it
---------------

First create a virtual environment and pip install the stuff.

`python3 -m venv .`

`source bin/activate`

`python3 -m pip install -r requirements.txt`

Then whenever you need to go back and re-activate the venv

`source bin/activate`

To run it

`python3 make_camo.py -i example/socal-mountains-no-sky.png -n 4 -s 1024`

General usage
-------------


    usage: make_camo.py [-h] [--input INPUT] [--size SIZE] [--num-clusters NUM_CLUSTERS]
    
    options:
      -h, --help            show this help message and exit
      --input INPUT, -i INPUT
                            input image file
      --size SIZE, -s SIZE  Output camo image dimensions
      --num-clusters NUM_CLUSTERS, -n NUM_CLUSTERS
                            Number of clusters


How it works
------------

This set of programs takes an input image (be sure to exclude sky from the input image) of a natural environment and creates a vaguely camouflage-looking pattern with colors from the palette of the input image.

It does this in two steps.

1. First it creates a color palette by running k-means clustering on the rgb values of the input image pixels. It notes, not only the color centroid of each cluster, but also the number of pixels assigned to each one. You can visualize the palettes it creates by looking at the output images it makes that contain the word "palette".
2. Then it creates a "Perlin noise" texture of the size of the intended output image. It uses values from this to index into the color palette created in step 1.

There is a bit of subtlety in step 2.  Rather than directly indexing into the color palette with the perlin noise texture, the program first creates the inverse of the CDF (cumulative distribution function) of the values of the perlin noise texture by sorting the flattened array of perlin noise values. It then fits a polynomial to that to approximate the forward CDF, and runs the Perlin noise through *that* before indexing into the color palette.  This ensures that each color in the palette will get approximately the same amount of representation in the output image as it had in the input palette.
