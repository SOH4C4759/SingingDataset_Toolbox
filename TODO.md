#### TODO 目前大部分歌曲能提供谱子，我这边可以score to midi，全段成品歌声的话，能够溯源到原始工程的我都导一份给你，少部分没有谱子的我这边可以提供bpm，应该能完成音频和midi的对齐，没有bpm的我这边还需要安排从成品音频测试一下bpm


### librosa 打包须知
- [ ] 需要将数据文件指定为pyinstaller hook
- [ ] 创建一个文件夹 extra-hooks,并在其中创建文件 hook-librosa.py
- [ ] 在创建的py文件中写入
```python
from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('librosa')
```
- 通过pyinstaller 命令中添加参数告诉pyinstaller 在哪儿找到此文件
```commandline
# --additional-hooks=extra-hooks
--additional-hooks-dir "[PATH_TO_YOUR_PROJECT]/extra-hooks"
```