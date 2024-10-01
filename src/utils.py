from typing import List
import csv
import json
from .seo_checker import SEOMetadata

def export_to_csv(metadata_list: List[SEOMetadata], filename: str):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Title', 'Meta Description', 'H1 Tags'])
        for metadata in metadata_list:
            writer.writerow([
                metadata.url,
                metadata.title,
                metadata.meta_description,
                '|'.join(metadata.h1_tags)
            ])

def export_to_json(metadata_list: List[SEOMetadata], filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([vars(m) for m in metadata_list], f, indent=2)
