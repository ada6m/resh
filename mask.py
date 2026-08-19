import math
import resvg_py
from PIL import Image
from io import BytesIO
import numpy as np
import time

def rasterize(region):
    paths = region.paths

    print(region.name, paths[0].bbox())
    xmin = math.floor(min(p.bbox()[0] for p in paths))
    xmax = math.ceil(max(p.bbox()[1] for p in paths))
    ymin = math.floor(min(p.bbox()[2] for p in paths))
    ymax = math.ceil(max(p.bbox()[3] for p in paths))

    width = xmax - xmin
    height = ymax - ymin

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}" height="{height}">
        <g transform="translate({-xmin},{-ymin})">
            {''.join(f'<path d="{p.d()}" fill="white"/>' for p in paths)}
        </g>
    </svg>'''

    start = time.perf_counter()

    png = resvg_py.svg_to_bytes(
        svg_string=svg,
        width=width,
        height=height,
        shape_rendering="optimize_speed",
    )

    print(f"RASTER TIME: {time.perf_counter() - start:.2f}s")

    mask = np.array(
        Image.open(BytesIO(png)).getchannel("A")
    )

    return mask, xmin, ymin, width, height

def measure(image, mask, xmin, ymin):
    height, width = mask.shape

    region = image[
        int(ymin):int(ymin) + height,
        int(xmin):int(xmin) + width
    ].compute()

    pixels = region[mask > 0]

    return {
        "area": len(pixels),
        "mean": float(np.mean(pixels)),
        "median": float(np.median(pixels)),
        "integrated": float(np.sum(pixels)),
    }
