import tifffile
import dask.array as da
from lxml import etree

def read_metadata(path):
    metadata = []
    with tifffile.TiffFile(path) as tif: #open .ome.tif file
        xml = tif.ome_metadata #only read xml metadata
    root = etree.fromstring(xml.encode()) #set root
    ns = {"ome": "http://www.openmicroscopy.org/Schemas/OME/2016-06"} #set namespace
    images = root.findall("ome:Image", ns) #find all image instances
    for image in images:
        pixels = image.find("ome:Pixels", ns) #find a pixel instance
        metadata.append({
            "Image": int(image.get("ID").split(":")[-1]), #extract image id
            "Width": int(pixels.get("SizeX")), #extract image width
            "Height": int(pixels.get("SizeY")), #extract image height
            "Channels": [
                ch.get("Name", "")
                for ch in pixels.findall("ome:Channel", ns) #extract channels
            ]
        })
    if metadata is not None: return metadata

def load_file(path, channel):
    store = tifffile.imread(path, aszarr=True)
    img = da.from_zarr(store)
    return img[channel]
