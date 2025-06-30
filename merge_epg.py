import os
import xml.etree.ElementTree as ET
import requests

# Get URLs from environment variables
epg_url_1 = os.getenv("EPG_URL_1")
epg_url_2 = os.getenv("EPG_URL_2")

def download_xml(url, filename):
    try:
        print(f"Downloading: {url}")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def merge_epg(epg1, epg2, output):
    try:
        tree1 = ET.parse(epg1)
        root1 = tree1.getroot()

        tree2 = ET.parse(epg2)
        root2 = tree2.getroot()

        for elem in root2.findall('channel') + root2.findall('programme'):
            root1.append(elem)

        tree1.write(output, encoding='utf-8', xml_declaration=True)
        print(f"Merged EPG saved as: {output}")
    except Exception as e:
        print(f"Error merging EPG files: {e}")

if epg_url_1 and epg_url_2:
    download_xml(epg_url_1, 'epg1.xml')
    download_xml(epg_url_2, 'epg2.xml')
    merge_epg('epg1.xml', 'epg2.xml', 'merged_epg.xml')
else:
    print("Missing EPG_URL_1 or EPG_URL_2 environment variables.")
