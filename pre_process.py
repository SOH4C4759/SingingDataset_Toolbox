import librosa


class PreProcess(object):
    import librosa
    def __init__(self, audio_file):
        self.audio, self.sr = librosa.load(audio_file)

    def __del__(self):
        self.audio = None
        self.sr = None

    def delete_silent(self):
        pass

    # TODO 人声音色自动分类

    # TODO 语种检测

    # TODO 音频裁减

    # TODO 音频静音删除

    # TODO 歌唱文本检测

