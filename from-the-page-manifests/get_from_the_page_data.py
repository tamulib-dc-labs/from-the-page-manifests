from csv import DictReader
import requests
import os
import json

class FromThePageReader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.all_manifests = self.read_csv(csv_file)

    @staticmethod
    def read_csv(csv_file):
        with open(csv_file, "r") as current_data:
            reader = DictReader(current_data)
            all_manifests = []
            for row in reader:
                item  = {
                    "new_manifest": f"https://fromthepage.com/iiif/{row.get('*FromThePage ID*', '')}/manifest",
                    "original manifest": row.get("*Originating Manifest ID*", ""),
                    "collection": row.get("*Originating Manifest ID*", "").split('/')[-2],
                    "work_id": row.get("*Originating Manifest ID*", "").split('/')[-1],
                }
                all_manifests.append(item)
            return all_manifests

    def get_all_manifests(self):
        for manifest in self.all_manifests:
            os.makedirs(f"manifests/{manifest.get('collection', '')}", exist_ok=True)
            r = requests.get(manifest.get('new_manifest'))
            with open(f"manifests/{manifest.get('collection', '')}/{manifest.get('work_id', '')}.json", 'w') as ftp:
                print(manifest.get('new_manifest'))
                current = r.json()
                current['@id'] = f"https://tamulib-dc-labs.github.io/from-the-page-manifests/manifests/{manifest.get('collection', '')}/{manifest.get('work_id', '')}.json"
                json.dump(current, ftp, indent=4)
        

if __name__ == "__main__":
    csv_file = "data/cherokee.csv"
    x = FromThePageReader(csv_file)
    x.get_all_manifests()
