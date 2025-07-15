import os
import xml.etree.ElementTree as ET
import requests
import gzip
import shutil

print("🔧 Starting EPG merge process...")

# Step 1: Read environment variables
epg_urls = [
    os.getenv("EPG_URL_1"),
    os.getenv("EPG_URL_2"),
    #os.getenv("EPG_URL_3")
]

for idx, url in enumerate(epg_urls, 1):
    if not url:
        print(f"❌ EPG_URL_{idx} is missing.")

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

def merge_multiple_epgs(epg_files, output):
    try:
        print("📂 Parsing and merging multiple EPG XML files...")
        base_tree = ET.parse(epg_files[0])
        base_root = base_tree.getroot()

        total_channels = 0
        total_programmes = 0

        for epg in epg_files[1:]:
            tree = ET.parse(epg)
            root = tree.getroot()

            for channel in root.findall('channel'):
                base_root.append(channel)
                total_channels += 1

            for programme in root.findall('programme'):
                base_root.append(programme)
                total_programmes += 1

        base_tree.write(output, encoding='utf-8', xml_declaration=True)
        print(f"✅ Merge complete. Added {total_channels} channels and {total_programmes} programmes.")
        print(f"💾 Merged EPG saved as: {output}")
    except Exception as e:
        print(f"❌ Error during merging: {e}")

# Step 2: Run the process
valid_urls = [url for url in epg_urls if url]

if len(valid_urls) >= 2:
    print("✅ Environment variables loaded.")
    print("⬇️ Starting download and extraction of EPG files...")

    xml_files = []

    for i, url in enumerate(valid_urls, 1):
        xml = f"epg{i}.xml"
        gz = f"epg{i}.xml.gz"
        download_and_extract(url, xml, gz)
        xml_files.append(xml)

    print("🔀 Starting merge of EPG files...")
    merge_multiple_epgs(xml_files, 'merged_epg.xml')
else:
    print("❌ Cannot continue. At least 2 valid EPG URLs are required.")
