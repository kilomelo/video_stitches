import subprocess
import os

def run_insanely_fast_whisper(input_path, output_path = ''):
    """
    将
    参数：
        input_path: 输入音频路径
    """
    try:
        if output_path is None or output_path == '':
            output_path = os.path.splitext(input_path)[0] + '.json'
        # print(f"输出文件：{output_path}")
        # 构建命令
        cmd = [
            'insanely-fast-whisper',
            '--file-name', input_path,        # 输入文件
            '--transcript-path', output_path,  # 输出文件
            '--language', 'Chinese',            # 语言
            # '--timestamp', 'word',            # 以词划分时间戳
            '--device-id', 'mps',             # mac设备mps加速
        ]
        
        print(f"运行insanely_fast_whisper，音频文件：{input_path}, 输出文件：{output_path}")
        # 执行命令并检查返回状态
        result = subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"执行完成")
        
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"发生异常：{str(e)}")

# 示例调用
if __name__ == "__main__":
    run_insanely_fast_whisper(
        input_path="还珠格格第一部_01_slice_denoised.wav",
        output_path='还珠格格第一部_01_slice_0.json'
    )