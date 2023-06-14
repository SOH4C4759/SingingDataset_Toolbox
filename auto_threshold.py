# 使用特征提取和机器学习的方法，使用Librosa提取音频信号的能量和频率特征，使用sklearn库训练一个分类模型来自动选择阈值
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

audio_path = "vo_01.wav"

# 加载音频文件
audio, sr = librosa.load(audio_path)

# 计算音频信号的能量和频率特征
energy = np.abs(audio)
mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)

# 将能量特征重复多次，使其与MFCC特征的帧数相同
n_frames = mfccs.shape[1]
energy_repeated = np.tile(energy, n_frames).reshape(n_frames, -1).T

# 将能量特征和MFCC特征拼接为一个特征矩阵
features = np.concatenate((energy_repeated, mfccs), axis=0).T

# 构建标签（声音活动为1，静音为0）
labels = np.zeros_like(energy)
for start, end in librosa.effects.split(audio):
    labels[start:end] = 1

# 将数据集划分为训练集和测试集
X_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42) # FIXME Found input variables with inconsistent numbers of samples: [1301, 665910]
# FIXME 搞不定没救了等死吧
# 训练一个随机森林分类器，用于自动选择阈值
clf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
clf.fit(X_train, y_train)

# 在测试集上评估分类器的准确率
accuracy = clf.score(x_test, y_test)
print(f"Accuracy:{accuracy}")

# 使用分类器预测测试集中的标签
y_pred = clf.predict(x_test)

# 计算阈值（能量的平均值）
threshold = np.mean(energy[y_pred == 1])
print(f"Threshold:{threshold}")

#　使用阈值来裁减音频文件

