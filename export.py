import pandas as pd

def export_excel(results, output_path):
    rows = {}

    for result in results:
        region = result["region"]

        if region not in rows:
            rows[region] = {
                "Region": region,
                "Area": result["area"],
            }

        channel = result["channel"]

        rows[region][channel] = result["mean"]

    df = pd.DataFrame(rows.values())

    df.to_excel(
        output_path,
        index=False,
        engine="openpyxl"
    )

    print(f"Created Excel file: {output_path}")
