import os
import sys
import csv
import re
from argparse import ArgumentParser

def parse_srt_file(file_path, macro_dir, macro_extension):
    entries = []
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    file_path_str = f"{macro_dir}/{base_name}.{macro_extension}"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    style_pattern = re.compile(r'\{.*?\}')  # 新增样式标记正则

    for block in content.split('\n\n'):
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        
        time_line = lines[1]
        match = time_pattern.match(time_line.strip())
        if not match:
            continue
        
        # 处理文本内容
        text = ' '.join(lines[2:]).strip()
        text = style_pattern.sub('', text)  # 过滤样式标记
        
        start = match.group(1).replace(',', '.')
        end = match.group(2).replace(',', '.')
        
        entries.append({
            "start": start,
            "end": end,
            "text": text,
            "path": file_path_str
        })
    
    return entries

def csv_from_srt(srt_dir, output_filename, macro_dir, macro_extension):

    output_path = os.path.join(srt_dir, output_filename)
    srt_files = []
    
    for f in sorted(os.listdir(srt_dir)):
        if f.lower().endswith('.srt'):
            srt_files.append(os.path.join(srt_dir, f))

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        for srt_file in srt_files:
            entries = parse_srt_file(srt_file, macro_dir, macro_extension)
            for entry in entries:
                writer.writerow([
                    entry["start"],
                    entry["end"],
                    '0',
                    '0',
                    entry["path"]
                ])
                writer.writerow(['$', entry["text"]])

    print(f"CSV file '{output_filename}' created successfully.")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python csv_from_srt.py <input.csv> <output.edl> <macro_dir> <macro_extension")
        sys.exit(1)
    csv_from_srt(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])