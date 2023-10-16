import sys
import os
import json
import shutil
from unidecode import unidecode
import traceback 

dir_regular = './emojis/regular/assets'
dir_animated = './emojis/animated/Emojis'

dir_output = './cdn/fluentui-emoji/Emojis'

styles = ['3D', 'Color', 'Flat', 'High Contrast']
skin_tones = ['Default', 'Light', 'Medium-Light', 'Medium', 'Medium-Dark', 'Dark']

data = {}

def format_string(string):
  return unidecode(string).lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')


def main():
  try:
    fetch_regular()

    return 0

  except Exception as e:
    print(repr(e))
    traceback.print_exc()


def fetch_regular():
  for emoji_name in os.listdir(dir_regular):
    emoji_path = os.path.join(dir_regular, emoji_name)
    if (os.path.exists(os.path.join(emoji_path, '3D'))): # No Skin Tones
      path_out = os.path.join(dir_output, format(emoji_name))
      os.makedirs(path_out, exist_ok=True)
      for style in os.listdir(emoji_path):
        path = os.path.join(emoji_path, style)
        
        if (os.path.isfile(path)):
          handle_metadata()
          continue
          
        img = os.listdir(path)[0]
        img_extension = img.split('.')[1]
        shutil.copy(os.path.join(path, img), os.path.join(path_out, f'{format(style)}.{img_extension}'))

    else:
      for color in os.listdir(emoji_path):
        if (os.path.isfile(os.path.join(emoji_path, color))):
          handle_metadata()
          continue
        
        for style in os.listdir(emoji_path):
          path_out = os.path.join(dir_output, format(emoji_name), format(style))
          path = os.path.join(emoji_path, color, style)

          os.makedirs(path_out, exist_ok=True)
          img = os.listdir(path)[0]
          img_extension = img.split('.')[1]
          shutil.copy(os.path.join(path, img), os.path.join(path_out, f'{format(color)}.{img_extension}'))
      
def handle_metadata():
  return
       
if __name__ == '__main__':
  sys.exit(main())