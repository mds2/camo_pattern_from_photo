import numpy as np
import cv2
from cluster_image import cluster_img_colors
from perlin_noise import PerlinNoise


def make_camo_patch(
        palette: np.ndarray,
        size: int
) -> np.ndarray:
    """Makes a tileable camo patch from a palette.
    """
    palette = cv2.filter2D(palette, -1, np.ones((25,1))) / 25
    palette = np.array(np.clip(palette, 0, 255), dtype=np.uint8)
    xs = np.linspace(0,1,size)
    ys = np.linspace(0,1,size)
    noise = PerlinNoise(octaves=3, seed=2)
    print("About to create big perlin noise image")
    lookups = np.array(
        [[noise([x, y], tile_sizes=[1,1]) for x in xs]
         for y in ys
         ]
    )
    print("Created big perlin noise image")
    range = [np.min(lookups), np.max(lookups)]
    lookups = palette.shape[0] * (lookups - range[0]) / (range[1] - range[0])
    lookups = np.array(
        np.clip(
            np.round(lookups), 0, palette.shape[0] - 1),
        dtype='int',
    )
    colors = palette[lookups, 0, :]
    return colors

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
                        type=Path,
                        help="input image file")
    parser.add_argument('--size', '-s',
                        type=int,
                        default=256,
                        required=False,
                        help="Output camo image dimensions")
    parser.add_argument('--num-clusters', '-n',
                        type=int,
                        default=5,
                        help="Number of clusters")
    args = parser.parse_args()
    img = cv2.imread(str(args.input))
    colors, reduced, pal = cluster_img_colors(img,
                                              num_clusters = args.num_clusters)
    output_filename = args.input.with_stem(
        args.input.stem +
        f".camo.{args.num_clusters}.{args.size}",
    )
    camo = make_camo_patch(pal, args.size)
    cv2.imwrite(str(output_filename),
                camo)
    pal_filename = args.input.with_stem(
        args.input.stem +
        f".palette.{args.num_clusters}",
    )
    cv2.imwrite(str(pal_filename), pal)
    print(f"Colors are :\n{np.array(colors, dtype=int)}")
