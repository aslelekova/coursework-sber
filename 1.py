import os
from collections import defaultdict

dataset_root = "/Users/anastasialelekova/Yandex.Disk.localized/datasets/cropped_classification_dataset"

splits = ['train', 'valid', 'test']
classes = ['clean', 'dirty']

summary = defaultdict(dict)

for split in splits:
    for cls in classes:
        dir_path = os.path.join(dataset_root, split, cls)
        if os.path.exists(dir_path):
            count = len([f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            summary[split][cls] = count
        else:
            summary[split][cls] = 0

# Печатаем красиво
for split in splits:
    clean_count = summary[split]['clean']
    dirty_count = summary[split]['dirty']
    total = clean_count + dirty_count
    print(f"\n📂 {split.upper()} — всего {total} изображений:")
    print(f"  🧼 clean: {clean_count}")
    print(f"  🧹 dirty: {dirty_count}")
