from pathlib import Path
from PIL import Image

for png in Path("assets/images").rglob("*.png"):
    try:
        img = Image.open(png)
        img.info.pop("icc_profile", None)
        img.save(png)
        print(f"Fixed: {png}")
    except Exception as e:
        print(f"Failed: {png} ({e})")