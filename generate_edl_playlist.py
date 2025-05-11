import csv
import sys
import os
from io import StringIO

def time_to_seconds(time_str):
    parts = time_str.split(':')
    if len(parts) != 3:
        raise ValueError(f"Invalid time format: {time_str}")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def replace_macros(path, macros):
    for macro, value in sorted(macros.items(), key=lambda x: -len(x[0])):
        path = path.replace(macro, value)
    return path

def format_float(value):
    formatted = "{0:.3f}".format(value).rstrip('0').rstrip('.')
    return formatted

def generate_edl_playlist(csv_path, edl_path=None):
    macros = {}
    data_lines = []
    if edl_path is None or edl_path == '':
            edl_path = os.path.splitext(csv_path)[0] + '.edl'
    with open(csv_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                macro_line = line[1:].strip()
                if '=' in macro_line:
                    key, value = macro_line.split('=', 1)
                    macros[key.strip()] = value.strip()
            elif line.startswith('$,'):
                continue
            else:
                data_lines.append(line)
    
    reader = csv.reader(StringIO('\n'.join(data_lines)))
    edl_entries = []
    for row in reader:
        if len(row) < 5:
            continue
        
        try:
            start_time_str = row[0].strip()
            end_time_str = row[1].strip()
            start_offset = float(row[2].strip())
            end_offset = float(row[3].strip())
            file_path = replace_macros(row[4].strip(), macros)
            
            start_sec = time_to_seconds(start_time_str)
            end_sec = time_to_seconds(end_time_str)
            
            edl_start = start_sec + start_offset
            duration = (end_sec - start_sec) + (end_offset - start_offset)
            
            edl_entries.append((
                file_path,
                format_float(edl_start),
                format_float(duration)
            ))
        except Exception as e:
            print(f"Error processing row {row}: {e}")
            continue
    
    with open(edl_path, 'w', encoding='utf-8') as f:
        f.write("# mpv EDL v0\n")
        for entry in edl_entries:
            f.write(f"{entry[0]},{entry[1]},{entry[2]}\n")
    print(f'EDL file generated at {edl_path}')
    return edl_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_edl_playlist.py <input.csv> <output.edl>")
        sys.exit(1)
    generate_edl_playlist(sys.argv[1], sys.argv[2])