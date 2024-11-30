Create camo patterns from natural photographs
======================

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
