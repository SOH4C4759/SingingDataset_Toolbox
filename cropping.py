# -*- coding: utf-8 -*-
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


class Cropping:
    def __init__(self, audio_path, path):
        # 加载音频文件
        sound = AudioSegment.from_wav(audio_path)
        loudness = round(sound.dBFS, 2)
        print("-----------------------")
        print(f"该音频响度为：{loudness}")

        # 第一个参数为待分割音频，第二个为多少秒“没声”代表沉默，第三个为分贝小于多少dBFS时代表沉默，第四个为为截出的每个音频添加多少ms无声
        chunks = split_on_silence(sound,
                                  # must be silent for at least half a second,沉默半秒
                                  min_silence_len=500,
                                  # consider it silent if quieter than -16 dBFS
                                  silence_thresh=-50,
                                  keep_silence=500
                                  )
        print('总分段：', len(chunks))

        # 放弃长度小于2秒的录音片段
        for i in list(range(len(chunks)))[::-1]:
            if len(chunks[i]) <= 1000 or len(chunks[i]) >= 20000:
                chunks.pop(i)
        print('取有效分段(大于2s小于20s)：', len(chunks))

        # TODO 分段弃用率&总时长弃用率
        # TODO 运行耗时
        # TODO 多线程优化

        for i, chunk in enumerate(chunks):
            # 获取文件名和扩展名
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            print(f"写入文件：{file_name}_{i}.wav")
            new_file_path = os.path.join(path, f'{file_name}_{i}.wav')
            chunk.export(new_file_path, format="wav")


if __name__ == "__main__":
    path = input("请输入所需处理的地址：")

    # 获取目标目录下所有文件和子目录
    assert not path.isspace()
    for root, dirs, files in os.walk(path):
        # 遍历所有文件
        for file in files:
            # 如果文件是wav文件
            # 获取文件的绝对路径
            file_path = os.path.join(root, file)
            # 自动剪切与删除静音
            assert Cropping(file_path, path)
            os.remove(file_path)

    os.system("pause")
