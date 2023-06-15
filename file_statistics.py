import os
import glob
import numpy as np
import librosa

# 定义要遍历的目录地址
directory = r"D:\FileBackup\SoundTest\SingerAudio\SingerAudio_DryVocalOnly\Nikki Singer_2"

# 定义变量
file_count = 0
total_duration = 0
durations = []

# 遍历所有音频文件
for root, dirs, files in os.walk(directory):
    for file in files:
        # 获取文件路径
        file_path = os.path.join(root, file)
        # 如果是音频文件，计算时长
        if file_path.endswith(".wav"):
            # 获取音频文件的时长
            try:
                duration = librosa.get_duration(filename=file_path)
            except:
                duration = 0
            # 将时长添加到列表中
            durations.append(duration)
            print(file_path,duration)
            # 更新文件数量和总时长
            file_count += 1
            total_duration += duration

# 计算中位数和四分位数
median_duration = np.median(durations)
lower_quartile = np.percentile(durations, 25)
upper_quartile = np.percentile(durations, 75)

# 输出结果
print("Total files:", file_count)
print("Total duration:", total_duration, "seconds")
print("Median duration:", median_duration, "seconds")
print("Lower quartile:", lower_quartile, "seconds")
print("Upper quartile:", upper_quartile, "seconds")