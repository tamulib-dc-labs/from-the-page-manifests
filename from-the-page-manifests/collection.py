from iiif_prezi3 import Collection
import os
import json

collection = Collection(
    id="https://tamulib-dc-labs.github.io/from-the-page-manifests/collection.json",
    label="Cherokee Freedmen",
    type="Collection"
)
for path, directories, files in os.walk("manifests/cherokee-freedmen-corrected_objects"):
    for filename in files:
        if filename.endswith(".json"):
            with open(os.path.join(path, filename), "r") as f:
                data = json.load(f)
            collection.make_manifest(
                id=data.get("@id"),
                label=data.get("label"),
            )
y = collection.json(indent=4)
with open("collections.json", 'w') as f:
    f.write(y)
