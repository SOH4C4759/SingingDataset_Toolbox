import os
import shutil


def rename_wav_files(path):
    # 将所有wav文件移动到目标目录
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".wav"):
                src_path = os.path.join(root, file)
                shutil.move(src_path, os.path.join(path, file))

    # 获取目标目录下所有文件和子目录
    for root, dirs, files in os.walk(path):
        # 遍历所有文件
        for file in files:
            # 如果文件是wav文件
            if file.endswith(".wav"):
                # 获取文件的绝对路径
                file_path = os.path.join(root, file)
                # 获取文件名和扩展名
                file_name, file_ext = os.path.splitext(file)
                # 生成新的文件名
                new_file_name = "{}{}".format(rename_wav_files.counter, file_ext)
                # 重命名文件
                os.rename(file_path, os.path.join(root, new_file_name))
                # 计数器加1
                rename_wav_files.counter += 1
                print(f"第{rename_wav_files.counter}个文件:{file_name}已整理并重命名为：{new_file_name}")
    return True


def list_folders(path):
    folders = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            folders.append(folder_path)
    return folders


def delete_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            os.rmdir(os.path.join(root, name))


if __name__ == "__main__":
    # 初始化计数器为1
    rename_wav_files.counter = 1
    path = input("请输入所需处理的地址：")
    folders = list_folders(path)
    for folder in folders:
        assert rename_wav_files(folder)
        delete_folders(folder)

