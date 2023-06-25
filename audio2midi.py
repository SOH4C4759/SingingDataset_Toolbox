from basic_pitch.inference import predict_and_save, predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import os


def get_audio_files(directory):
    audio_files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            audio_files.extend(get_audio_files(item_path))
        elif os.path.isfile(item_path) and item.lower().endswith(('.mp3', '.wav', '.flac')):
            audio_files.append(item_path)
    return audio_files


directory = input("请输入所需处理的地址：")
audio_files_list = get_audio_files(directory)

predict_and_save(audio_path_list=audio_files_list,output_directory=directory, save_midi=True, save_model_outputs=True,
                 save_notes=True, minimum_note_length=58,sonify_midi=False)
