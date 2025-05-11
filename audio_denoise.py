import numpy as np
import noisereduce as nr
import librosa
import soundfile as sf

def read_and_normalize(input_path, target_sr=16000):
    """
    读取音频并标准化（支持MP3/WAV等格式）
    
    参数:
        input_path: str - 音频文件路径
        target_sr: int - 目标采样率（默认16kHz）
    """
    # 读取音频（自动转为单声道，强制重采样）
    y, sr = librosa.load(input_path, 
                        sr=target_sr,  # 自动重采样
                        mono=True)     # 强制单声道
    
    return y, target_sr
def denoise_audio(input_path, output_path, prop_decrease=0.95, target_sr=16000):
    """
    音频降噪核心方法
    
    参数:
        input_path (str): 输入音频路径（支持wav/mp3/m4a等格式）
        output_path (str): 输出音频路径（建议wav格式）
        prop_decrease (float): 降噪强度（0-1，默认0.95）
        target_sr (int): 目标采样率（默认16kHz，优化语音频段）
    """
    try:
        # 步骤1：读取音频并标准化
        y, sr = librosa.load(input_path, 
            sr=target_sr, 
            mono=True,
            dtype=np.float32)  # 确保数据类型统一
        
        # 步骤2：噪声特征分析（自动检测噪声段）
        noise_samples = int(0.5 * target_sr)  # 前0.5秒样本数
        noise_clip = y[:noise_samples]  # 直接截取numpy数组
        
        # 步骤3：应用频谱门控降噪
        reduced_noise = nr.reduce_noise(
            y=y,  # 直接使用librosa读取的浮点数组
            y_noise=noise_clip,
            sr=target_sr,
            prop_decrease=prop_decrease,
            stationary=False
        )
        
        # 步骤4：保存处理结果
        sf.write(output_path, 
                reduced_noise, 
                target_sr,
                subtype='PCM_16')  # 指定16位量化
        
        print(f"降噪完成，文件已保存至：{output_path}")
        
    except Exception as e:
        print(f"处理失败：{str(e)}")

# 示例调用
if __name__ == "__main__":
    denoise_audio(
        "还珠格格第一部_01_slice.mp3",
        "还珠格格第一部_01_slice_denoised.wav",
        prop_decrease=0.98)