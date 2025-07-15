import os
import xml.etree.ElementTree as ET
import requests
import gzip
import shutil

print("🔧 Starting EPG merge process...")

# Step 1: Read environment variables
epg_url_1 = os.getenv("EPG_URL_1")
epg_url_2 = os.getenv("EPG_URL_2")
epg_url_3 = os.getenv("EPG_URL_3")

print("📥 Checking environment variables...")
if not epg_url_1:
    print("❌ EPG_URL_1 is missing.")
if not epg_url_2:
    print("❌ EPG_URL_2 is missing.")
if not epg_url_3:
    print("❌ EPG_URL_3 is missing.")

def download_and_extract(url, out_xml, temp_gz):
    try:
        print(f"➡️ Downloading from: {url}")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(temp_gz, 'wb') as f:
            f.write(r.content)
        print(f"✅ Downloaded: {temp_gz}")
        
        # Decompress
        with gzip.open(temp_gz, 'rb') as f_in:
            with open(out_xml, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"📂 Extracted to: {out_xml}")
    except Exception as e:
        print(f"❌ Failed to download or extract {url}: {e}")

def merge_epg(base_xml, others, output):
    try:
        print(f"📂 Parsing base EPG file: {base_xml}")
        tree = ET.parse(base_xml)
        root = tree.getroot()

        added_channels = 0
        added_programmes = 0

        for epg_file in others:
            print(f"📂 Merging EPG file: {epg_file}")
            other_tree = ET.parse(epg_file)
            other_root = other_tree.getroot()

            for channel in other_root.findall('channel'):
                root.append(channel)
                added_channels += 1

            for programme in other_root.findall('programme'):
                root.append(programme)
                added_programmes += 1

        tree.write(output, encoding='utf-8', xml_declaration=True)
        print(f"✅ Merge complete. Added {added_channels} channels and {added_programmes} programmes.")
        print(f"💾 Merged EPG saved as: {output}")
    except Exception as e:
        print(f"❌ Error during merging: {e}")

# Step 2: Run the process
if epg_url_1 and epg_url_2 and epg_url_3:
    print("✅ Environment variables loaded.")
    print("⬇️ Starting download and extraction of EPG files...")

    download_and_extract(epg_url_1, 'epg1.xml', 'epg1.xml.gz')
    download_and_extract(epg_url_2, 'epg2.xml', 'epg2.xml.gz')
    download_and_extract(epg_url_3, 'epg3.xml', 'epg3.xml.gz')

    print("🔀 Starting merge of EPG files...")
    merge_epg('epg1.xml', ['epg2.xml', 'epg3.xml'], 'merged_epg.xml')
else:
    print("❌ Cannot continue. One or more EPG URLs are missing.")
