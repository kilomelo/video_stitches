import subprocess
import os

def convert_mp4_to_audio(input_path, output_path, start_time, end_time):
    """
    将MP4视频转换为音频文件，并指定时间范围
    参数：
        input_path: 输入视频路径（MP4格式）
        output_path: 输出音频路径（支持mp3/wav等格式）
        start_time: 开始时间（格式：00:01:00 或秒数）
        end_time: 结束时间（格式：00:02:30 或秒数）
    """
    try:
        # 构建FFmpeg命令
        cmd = [
            'ffmpeg',
            '-y',  # 覆盖已存在文件
            '-ss', str(start_time),  # 开始时间
            '-to', str(end_time),    # 结束时间
            '-i', input_path,        # 输入文件
            '-vn',                   # 禁用视频流
            '-acodec', 'libmp3lame', # MP3编码器（输出为wav时自动改为pcm_s16le）
            '-q:a', '0',             # 最高音频质量
            output_path
        ]
        
        # 执行命令并检查返回状态
        result = subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"转换成功！音频文件保存至：{os.path.abspath(output_path)}")
        
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"发生异常：{str(e)}")

# 示例调用
if __name__ == "__main__":
    convert_mp4_to_audio(
        input_path="还珠格格第一部_01.mp4",
        output_path="还珠格格第一部_01_slice.mp3",
        # start_time="00:03:00",  # 支持时间戳或秒数格式（如60）
        start_time="00:05:52",  # 支持时间戳或秒数格式（如60）
        end_time="00:08:20"
    )