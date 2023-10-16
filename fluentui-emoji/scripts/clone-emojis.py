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

def format(string):
  return unidecode(string).lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')


def main():
  try:
    fetch_regular()


    with open(os.path.join(dir_output, 'metadata.json'), 'w') as f:
      json.dump(data, f)
      
    with open('./cdn/fluentui-emoji/metadata.json', 'w') as f:
      f.write(json.dumps(data, indent=4))

    return 0

  except Exception as e:
    traceback.print_exc()
    return e


def fetch_regular():
  for emoji_name in os.listdir(dir_regular):
    emoji_path = os.path.join(dir_regular, emoji_name)
    emoji = format(emoji_name)
    data[emoji] = {
      'name': emoji_name
    }
    
    if (os.path.exists(os.path.join(emoji_path, '3D'))):
      data[emoji]['hasSkintones'] = False
      path_out = os.path.join(dir_output, format(emoji_name))
      os.makedirs(path_out, exist_ok=True)
      for style in os.listdir(emoji_path):
        path = os.path.join(emoji_path, style)
        if (os.path.isfile(path)):
          handle_metadata(emoji, path)
          continue
        img = os.listdir(path)[0]
        img_extension = img.split('.')[1]
        shutil.copy(os.path.join(path, img), os.path.join(path_out, f'{format(style)}.{img_extension}'))

    else:
      data[emoji]['hasSkintones'] = True
      for color in os.listdir(emoji_path):
        color_path = os.path.join(emoji_path, color)
        if (os.path.isfile(color_path)):
          handle_metadata(emoji, color_path)
          continue
        for style in os.listdir(color_path):
          path_out = os.path.join(dir_output, format(emoji_name), format(style))
          path = os.path.join(color_path, style)

          os.makedirs(path_out, exist_ok=True)
          img = os.listdir(path)[0]
          img_extension = img.split('.')[1]
          shutil.copy(os.path.join(path, img), os.path.join(path_out, f'{format(color)}.{img_extension}'))
      
def handle_metadata(emoji, metadata_path):
  f = open(metadata_path)
  metadata = json.load(f)
  copy_values = ['glyph', 'group', 'keywords']
  for value in copy_values:
    if (metadata[value]):
      data[emoji][value] = metadata[value]
  
  if ('unicodeSkintones' in metadata):
    data[emoji]['unicodes'] = metadata['unicodeSkintones']
  else:
    data[emoji]['unicodes'] = [metadata['unicode']]
  
  f.close()
  return
       
if __name__ == '__main__':
  sys.exit(main())