from lxml import etree
import pickle
from svgpathtools import Document

pkl_path = "Files/MouseRegions.pkl"

class Region:
    def __init__(self, name, parent, root, paths):
        self.name = name
        self.parent = parent
        self.root = root
        self.paths = []

    def add_path(self, path):
        self.paths.append(path)

def read_metadata(svg_path):
    tree = etree.parse(svg_path)
    root = tree.getroot()
    metadata = []
    return metadata

def get_region(structure_id, region_lookup):
    try:
        lookup = region_lookup[int(structure_id)]
        if lookup["has_children"] is False:
            return lookup
    except (KeyError, TypeError, ValueError):
        return None
    return None

def read_file(svg_path):
    with open(pkl_path, "rb") as f:
        region_lookup = pickle.load(f)

    parser = etree.XMLParser(huge_tree=True)
    tree = etree.parse(svg_path, parser)
    root = tree.getroot()
    doc = Document(svg_path)
    regions = {}

    for path in doc.paths():
        element = path.element

        structure_id = element.get("structure_id")
        if not structure_id: continue

        info = get_region(structure_id, region_lookup)
        if info is None: continue

        structure_id = int(structure_id)
        if structure_id not in regions:
            regions[structure_id] = Region(
                name=info["name"],
                parent=info["parent"],
                root=info["root"],
                paths=[]
            )
        regions[structure_id].add_path(path)
    return regions
