import librosa
import numpy as np

# 加载音频文件
audio, sr = librosa.load('audio_file.wav')

# 计算音频信号的过零率和短时能量
zero_crossings = librosa.zero_crossings(audio)
energy = librosa.feature.rms(audio)

# 调整能量门限，以便识别语音段和静音段
threshold_ratio = 0.5
threshold = np.max(energy) * threshold_ratio

# 根据能量门限和最大静音长度，识别静音段和语音段
max_silence_length = 1.0
max_silence_samples = int(max_silence_length * sr)
segments = []
start = None
for i in range(len(audio)):
    if energy[0, i] > threshold:
        if start is None:
            start = i
        elif i - start > max_silence_samples:
            segments.append((start, i))
            start = i
    else:
        if start is not None and i - start > max_silence_samples:
            segments.append((start, i))
            start = None
if start is not None:
    segments.append((start, len(audio)))

# 根据片段最小长度，过滤掉过短的片段
min_segment_length = 0.5
min_segment_samples = int(min_segment_length * sr)
segments = [s for s in segments if s[1] - s[0] >= min_segment_samples]

# 迭代遍历每个片段，将其保存为新的音频文件
for i, segment in enumerate(segments):
    # 获取每个片段的起始和结束位置
    start = segment[0]
    end = segment[1]
    # 将该片段保存为独立的音频文件
    segment_audio = audio[start:end]
    librosa.output.write_wav(f'segment_{i}.wav', segment_audio, sr)