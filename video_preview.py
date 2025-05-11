import subprocess
import os
from generate_edl_playlist import generate_edl_playlist

def preview_video(csv_path):
    """
    预览一个缝合视频
    """
    edl_path = generate_edl_playlist(csv_path)
    try:
        # 构建FFmpeg命令
        cmd = [
            'mpv',
            edl_path,
            '--geometry=30%',
        ]
        
        # 执行命令并检查返回状态
        result = subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"播放完成")
        
    except subprocess.CalledProcessError as e:
        print(f"调用播放器失败：{e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"发生异常：{str(e)}")

# 示例调用
if __name__ == "__main__":
    csv_path = 'playlist.csv'
    preview_video(csv_path)