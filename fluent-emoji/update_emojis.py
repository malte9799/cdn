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

dir_output = './cdn/fluent-emoji/Emojis'

data = {'not_found': []}

img_sizes = [128, 64, 32]

def format(string):
  string = unidecode(string).lower().replace(' ', '_').replace('-', '_')
  string = re.sub(r"\.png|[(),'.]", '', string)
  return string.replace('_blond_', '_blonde_')

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
       
def try_varients(emoji):
  if (emoji in data): return emoji
  if (emoji.replace('men', 'man') in data): return emoji.replace('men', 'man')
  if (emoji.replace('people', 'person') in data): return emoji.replace('people', 'person')
  if ('person_' + emoji in data): return 'person_' + emoji

  if (emoji == 'mermaid' and 'woman_merpeople' in data): return 'woman_merpeople'
  if (emoji == 'merman' and 'man_merpeople' in data): return 'man_merpeople'
  if (emoji == 'merperson' and 'person_merpeople' in data): return 'person_merpeople'

  return False

def save_images(img_path, output_path):
  extension = img_path.split('.')[1]
  if (extension == 'svg'):
    os.makedirs('/'.join(output_path.split('/').pop()), exist_ok=True)
    shutil.copy(img_path, f'{output_path}.svg')
  else:
    os.makedirs(output_path, exist_ok=True)
    shutil.copy(img_path, f'{output_path}/256.png')
    for size in img_sizes:
      img = Image.open(img_path)
      img.thumbnail((size, size), Image.Resampling.LANCZOS)
      img.save(f'{output_path}/{size}.png')

def fetch_regular():
  for emoji_name in os.listdir(dir_regular):
    emoji_path = os.path.join(dir_regular, emoji_name)
    emoji = format(emoji_name)
    data[emoji] = {
      'name': emoji_name
    }
    
    if (os.path.exists(os.path.join(emoji_path, '3D'))): # No Skintones
      data[emoji]['hasSkinTones'] = False
      for style in os.listdir(emoji_path):
        path = os.path.join(emoji_path, style)
        if (os.path.isfile(path)):
          handle_metadata(emoji, path)
          continue
        img = os.listdir(path)[0]
        img_path = os.path.join(path, img)
        output_path = os.path.join(dir_output, emoji, format(style))
        save_images(img_path, output_path)

    else:
      data[emoji]['hasSkinTones'] = True
      for color in os.listdir(emoji_path):
        color_path = os.path.join(emoji_path, color)
        if (os.path.isfile(color_path)):
          handle_metadata(emoji, color_path)
          continue
        for style in os.listdir(color_path):
          path = os.path.join(color_path, style)
          output_path = os.path.join(dir_output, emoji, format(style), format(color))
          img = os.listdir(path)[0]
          img_path = os.path.join(path, img)
          save_images(img_path, output_path)

    # if (os.path.exists(os.path.join(emoji_path, '3D'))): # No Skintones
    #   data[emoji]['hasSkinTones'] = False
    #   path_out = os.path.join(dir_output, format(emoji_name))
    #   for style in os.listdir(emoji_path):
    #     if (image_path.split('.')[1] == 'png'):
    #       path_out = os.path.join(path_out, format(style))
    #     os.makedirs(path_out, exist_ok=True)

    #     path = os.path.join(emoji_path, style)
    #     if (os.path.isfile(path)):
    #       handle_metadata(emoji, path)
    #       continue
    #     img = os.listdir(path)[0]
    #     # img_extension = img.split('.')[1]
    #     save_images(os.path.join(path, img), path_out)
    #     # shutil.copy(os.path.join(path, img), os.path.join(path_out, f'{format(style)}.{img_extension}'))

    # else: # Has Skintones
    #   data[emoji]['hasSkinTones'] = True
    #   for color in os.listdir(emoji_path):
    #     color_path = os.path.join(emoji_path, color)
    #     if (os.path.isfile(color_path)):
    #       handle_metadata(emoji, color_path)
    #       continue
    #     for style in os.listdir(color_path):
    #       path_out = os.path.join(dir_output, format(emoji_name), format(style))
    #       if (image_path.split('.')[1] == 'png'):
    #         path_out = os.path.join(path_out, format(color))
    #       path = os.path.join(color_path, style)

    #       os.makedirs(path_out, exist_ok=True)
    #       img = os.listdir(path)[0]
    #       save_images(os.path.join(path, img), path_out)
    #       # img_extension = img.split('.')[1]
    #       # shutil.copy(os.path.join(path, img), os.path.join(path_out, f'{format(color)}.{img_extension}'))

def fetch_animated():
  regex = r'_(light|medium_light|medium|medium_dark|dark)_skin_tone'
  for category in os.listdir(dir_animated):
    category_path = os.path.join(dir_animated, category)
    for emoji_file in os.listdir(category_path):
      emoji_path = os.path.join(category_path, emoji_file)
      if not (is_animated_png(emoji_path)): continue
      emoji_name = format(emoji_file)
      emoji = re.sub(regex, '', emoji_name)
      
      emoji = try_varients(emoji)
      if not (emoji):
        e = re.sub(regex, '', emoji_name)
        if (e not in data['not_found']):
          data['not_found'].append(e)
        continue
      
      data[emoji]['isAnimated'] = True
      output_path = os.path.join(dir_output, emoji, 'animated')
      if (data[emoji]['hasSkinTones']):
        color_match = re.search(regex, emoji_name)
        color = color_match.group(1) if color_match else 'default'
        output_path = os.path.join(output_path, color)

      save_images(emoji_path, output_path)

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