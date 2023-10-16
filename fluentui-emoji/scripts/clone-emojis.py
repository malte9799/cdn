import sys
import os
import json
from unidecode import unidecode

dir_regular = './data/regular/assets'
dir_animated = './data/animated/Emojis'

dir_output = './cdn/Emojis'

styles = ['3D', 'Color', 'Flat', 'High Contrast']
skin_tones = ['Default', 'Light', 'Medium-Light', 'Medium', 'Medium-Dark', 'Dark']

data = {}

i = 0
def main():
  for (dirpath, dirnames, filenames) in os.walk(dir_regular):
    print(f'Path: {dirpath}  --  DirNames: {dirnames}  --  Filenames: {filenames} \n')


  # fetch_regular()


  # folder_dict = {"default":[], "color":[]}
  # arr = []
  # for folder in sorted(os.listdir(root_dir)):
  #     key = "" if "3D" in os.listdir(os.path.join(root_dir, folder)) else "-color"
  #     # folder_dict[key].append("_".join(folder.lower().split()))
  #     arr.append("_".join(folder.lower().split())+key)
      
  # with open("./cdn/fluentui-emoji/list.json", "w") as f:
  #     json.dump(arr, f, ensure_ascii=False)
  return 0



# def fetch_regular():
#    for emoji_name in os.listdir(dir_regular):
#       emoji_name_out = emoji_name.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
#       emoji_name_out = unidecode(emoji_name_out)
#       data[emoji_name_out] = {}

#       emoji_path = os.path.join(dir_regular, emoji_name)
#       if (os.path.exists(os.path.join(emoji_path, '3D'))): # No Skin Tones
#         for style in os.listdir(emoji_path):
#           style_out = style.lower().replace(' ', '_').replace('-', '_')
#           data[emoji_name_out][style_out] = os.path.join()

#    return

# path_out = os.path.join(dir_output, emoji_name_out)
# if not (os.path.exists(path_out)):
#   os.mkdir(path_out)



# if not (os.path.exists(os.path.join(emoji_path, '3D'))):
#   for color in os.listdir(emoji_path):
#     color_out = color.lower().replace(' ', '_').replace('-', '_')
#     if not (os.path.exists(os.path.join(emoji_path, color_out))):
#       os.mkdir(os.path.join(emoji_path, color_out))
#     get_styles(os.path.join(emoji_path, color))

# else:
#   get_styles(emoji_path)


# def get_styles(path):
#   for style in os.listdir(path):
#     return

if __name__ == '__main__':
  try:
    sys.exit(main())
  except Exception as e:
    print(repr(e))