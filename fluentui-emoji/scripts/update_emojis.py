import sys
import os
import json
import shutil
import traceback 
import re
from PIL import Image
from unidecode import unidecode

dir_regular = './emojis/regular/assets'
dir_animated = './emojis/animated/Emojis'

dir_output = './cdn/fluentui-emoji/Emojis'

data = {}

def format(string):
  return unidecode(string).lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace('.png', '').replace(',', '').replac("'", '')

def is_animated_png(file_path):
    try:
        img = Image.open(file_path)
        return hasattr(img, 'n_frames') and img.n_frames > 1
    except Exception as e:
        return False

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
       

def fetch_regular():
  for emoji_name in os.listdir(dir_regular):
    emoji_path = os.path.join(dir_regular, emoji_name)
    emoji = format(emoji_name)
    data[emoji] = {
      'name': emoji_name
    }
    
    if (os.path.exists(os.path.join(emoji_path, '3D'))):
      data[emoji]['hasSkinTones'] = False
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
      data[emoji]['hasSkinTones'] = True
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

def fetch_animated():
  regex = r'_(light|medium_light|medium|medium_dark|dark)_skin_tone'
  replacements = {'women_wrestling': 'woman_wrestling', 'men_wrestling': 'man_wrestling'}
  addPerson = ['fairy', 'genie']
  for category in os.listdir(dir_animated):
    category_path = os.path.join(dir_animated, category)
    for emoji_file in os.listdir(category_path):
      emoji_path = os.path.join(category_path, emoji_file)
      if not (is_animated_png(emoji_path)): continue
      emoji_name = format(emoji_file)
      emoji = re.sub(regex, '', emoji_name)
      
      emoji = try_varients(emoji)
      if not (emoji):
        data.setdefault('not_found', {})[emoji_file] = emoji_name
        continue
      
      data[emoji]['isAnimated'] = True
      if (data[emoji]['hasSkinTones']):
        color_match = re.search(regex, emoji_name)
        color = color_match.group(1) if color_match else 'default'
        
        path_out = os.path.join(dir_output, emoji, 'animated')
        os.makedirs(path_out, exist_ok=True)
        shutil.copy(emoji_path, os.path.join(path_out, f'{color}.png'))
        
      else:
        shutil.copy(emoji_path, os.path.join(dir_output, emoji, 'animated.png'))
  
def try_varients(emoji):
  if (emoji in data): return emoji
  if (emoji.replace('men', 'man') in data): return emoji.replace('men', 'man')
  if (emoji.replace('people', 'person') in data): return emoji.replace('people', 'person')
  return False

def main():
  try:
    fetch_regular()
    fetch_animated()


    with open(os.path.join(dir_output, 'metadata.json'), 'w') as f:
      json.dump(data, f)
      
    return 0

  except Exception as e:
    traceback.print_exc()
    return e


if __name__ == '__main__':
  sys.exit(main())