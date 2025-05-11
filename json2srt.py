import json
import os

def convert_seconds_to_srt_time(total_seconds):
    """将秒数转换为SRT时间格式 HH:MM:SS,mmm"""
    total_seconds = max(total_seconds, 0)
    total_milliseconds = int(round(total_seconds * 1000))
    
    hours, remaining = divmod(total_milliseconds, 3600 * 1000)
    minutes, remaining = divmod(remaining, 60 * 1000)
    seconds, milliseconds = divmod(remaining, 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def json_to_srt(input_json_path, output_srt_path, offset_seconds=0.0):
    """
    将Whisper JSON转换为SRT字幕文件
    参数：
        input_json_path: 输入JSON文件路径
        output_srt_path: 输出SRT文件路径
        offset_seconds: 时间偏移（秒），正数延后，负数提前
    """
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    srt_lines = []
    counter = 1
    
    for chunk in data.get('chunks', []):
        # 跳过空文本
        text = chunk.get('text', '').strip()
        if not text:
            continue
        
        # 验证时间戳格式
        timestamp = chunk.get('timestamp', [])
        if len(timestamp) != 2:
            continue
        
        # 应用时间偏移
        start, end = timestamp
        new_start = max(start + offset_seconds, 0)
        new_end = max(end + offset_seconds, 0)
        
        # 跳过无效时间区间
        if new_start >= new_end:
            continue
        
        # 转换时间格式
        start_time = convert_seconds_to_srt_time(new_start)
        end_time = convert_seconds_to_srt_time(new_end)
        
        # 构建SRT条目
        srt_lines.append(str(counter))
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append('')  # 空行分隔
        counter += 1
    
    if output_srt_path is None or output_srt_path == '':
            output_srt_path = os.path.splitext(input_json_path)[0] + '.srt'
    # 写入SRT文件
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_lines))

# 使用示例
if __name__ == "__main__":
    json_to_srt('还珠格格第一部_01_slice_denoised.json', '', offset_seconds=352)