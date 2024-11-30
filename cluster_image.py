import numpy as np
import cv2
from sklearn.cluster import KMeans

from typing import Tuple

def cluster_img_colors(
        img: np.ndarray,
        num_clusters: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Here is a lovely empty docstring
    """
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(img.reshape((-1, 3)))
    buckets = kmeans.predict(img.reshape((-1, 3)))
    colors = kmeans.cluster_centers_
    reduced = colors[buckets, :]
    palette = colors[sorted(buckets), :][::img.shape[0], :].reshape((-1, 1, 3))
    palette = np.hstack([palette for i in range(img.shape[1] // 5)])
    return colors, reduced.reshape(img.shape), palette

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
                        type=Path,
                        help="input image file")
    parser.add_argument('--num-clusters', '-n',
                        type=int,
                        default=5,
                        help="Number of clusters")
    args = parser.parse_args()
    img = cv2.imread(str(args.input))
    colors, reduced, pal = cluster_img_colors(img,
                                              num_clusters = args.num_clusters)
    output_filename = args.input.with_stem(args.input.stem +
                                           f".colors.{args.num_clusters}")
    cv2.imwrite(str(output_filename),
                reduced)
    pal_filename = args.input.with_stem(args.input.stem +
                                        f".palette.{args.num_clusters}")
    cv2.imwrite(str(pal_filename), pal)
    print(f"Colors are :\n{np.array(colors, dtype=int)}")

