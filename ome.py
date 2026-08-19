import tifffile
import dask.array as da
from lxml import etree

def load_file(path, channel):
    store = tifffile.imread(path, aszarr=True)
    img = da.from_zarr(store) #use zarr to lazy load .ome
    return img[channel]

def read_metadata(path):
    metadata = []
    with tifffile.TiffFile(path) as tif: #open .ome.tif file
        xml = tif.ome_metadata 
    root = etree.fromstring(xml.encode()) 
    ns = {"ome": "http://www.openmicroscopy.org/Schemas/OME/2016-06"} 
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
