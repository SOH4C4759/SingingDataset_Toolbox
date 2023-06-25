# -*- coding: utf-8 -*-
import os
import random
import librosa
import numpy as np
from matplotlib import pyplot as plt, gridspec
import simpleaudio as sa


def find_wav_files(directory: str):
    """
    递归遍历指定目录中的所有wav文件
    :param directory: 指定目录
    :return: 返回wav文件地址的列表
    """
    wav_files = []
    index = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                index += 1
                wav_files.append(os.path.join(root, file))
    return wav_files,index


def extract_features(wav_files: list[str]):
    """
    从wav文件中提取各种音频特征
    :param wav_files:输入的音频文件地址
    :return:None
    """
    for wav in wav_files:
        print(f"当前文件为{os.path.basename(wav)},频谱&波形图加载中，请稍候")
        # 读取音频文件并提取特征
        y, sr = librosa.load(path=wav, sr=48000, mono=True)
        sr = 48000 # 强制采样率为48000
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        # 将特征拼接成一个特征向量
        features = [chroma_stft, rmse, spec_cent, spec_bw, rolloff, zcr, mfcc]
        features_vector = []
        for feature in features:
            features_vector.append(feature.mean())
            features_vector.append(feature.var())
        features_vector = np.array(features_vector)
        # 打印特征向量
        print(
            f"特征向量：[chroma_stft,rms,spectral_centroid,spectral_bandwidth,spectral_rolloff,zero_crossing_rate,mfcc]{features_vector}")

        # 绘制频谱图和波形图
        fig = plt.figure(figsize=(20, 12))
        gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[2, 1])
        ax0 = fig.add_subplot(gs[0])
        librosa.display.specshow(librosa.power_to_db(np.abs(librosa.stft(y)), ref=np.max), y_axis='log', x_axis='time',
                                 sr=sr, fmax=24000, ax=ax0)
        ax0.set_title('Spectrum graph')
        ax0.set_ylabel('Frequency (Hz)')
        ax0.set_xticks([])
        ax1 = fig.add_subplot(gs[1])
        librosa.display.waveshow(y, sr=sr, ax=ax1)
        ax1.set_title('Waveform plot')
        ax1.set_ylabel('Amplitude')
        ax1.set_xticks([])
        ax1.set_yticks([])
        plt.tight_layout(h_pad=2)
        plt.show()
        # 播放音频
        play_obj = sa.play_buffer((y * 32767).astype(np.int16), 1, 2, sr)
        # 等待用户输入并按空格键或Enter键
        print("按Enter键继续...")
        while True:
            key = input()
            if key == ' ':
                play_obj.stop()
                play_obj = sa.play_buffer((y * 32767).astype(np.int16), 1, 2, sr)
            elif key == '':
                break
        plt.close()


if __name__ == "__main__":
    directory = input("请输入进行随机抽查的文件地址:")
    assert not directory.isspace()
    directory.replace('\\','/')
    wav_files,index = find_wav_files(directory)
    print(f"共监测到{index}个wav文件")
    # 抽取文件
    num = input("请输入随机选取的文件数量并不得大于文件总数:")
    assert not num.isspace()
    print(f"开始随机抽取文件检查,共抽查{num}个文件")
    wav_files = random.sample(wav_files, int(num))
    extract_features(wav_files)
