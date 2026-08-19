 import ome
import svg
import mask
import export

ome_path = "Files/Section1.ome.tif"
svg_path = "Files/Section1.svg"

ome_metadata = ome.read_metadata(ome_path)
regions = svg.read_file(svg_path)

print(ome_metadata)
print(f"Found {len(regions)} valid structures.")

channels = ome_metadata[0]["Channels"]

print(f"Found {len(channels)} channels:")
for i, channel in enumerate(channels):
    print(f"  {i}: {channel}")

images = {
    channel_name: ome.load_file(ome_path, i)
    for i, channel_name in enumerate(channels)
}

templates = [
    mask.rasterize(region)
    for region in regions.values()
]

"""viewer.show_all_regions(
    images[channels[0]],
    regions,
    templates,
    downsample=10,
    alpha=0.25,
)"""

input("\nPress Enter to begin analysis...")

results = []

for region, template in zip(regions.values(), templates):
    print("Working on: ", region.name)
    raster_mask, xmin, ymin, width, height = template

    for channel_name, image in images.items():
        intensity = mask.measure(
            image,
            raster_mask,
            xmin,
            ymin,
        )
        results.append({
            "region": region.name,
            "channel": channel_name,
            **intensity,
        })

export.export_excel(
    results,
    "Files/results.xlsx"
)
