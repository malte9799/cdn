import sys
import os
import json

def main():
    print(os.listdir())
    try:
        root_dir = './fluentui-emoji/assets'
        # folder_dict = {"default":[], "color":[]}
        arr = []
        for folder in sorted(os.listdir(root_dir)):
            key = "" if "3D" in os.listdir(os.path.join(root_dir, folder)) else "-color"
            # folder_dict[key].append("_".join(folder.lower().split()))
            arr.append("_".join(folder.lower().split())+key)
            
        with open("./cdn/fluentui-emoji-list.json", "w") as f:
            json.dump(arr, f, ensure_ascii=False)
        return 0

    except Exception as e:
        print(repr(e))
        return 1

if __name__ == '__main__':
    sys.exit(main())