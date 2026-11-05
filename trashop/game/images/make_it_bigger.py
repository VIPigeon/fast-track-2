from PIL import Image
from pathlib import Path

INPUT_DIR = Path("")
OUTPUT_DIR = Path("")
TARGET_HEIGHT = 461

# Список изображений для обработки
FILES_TO_RESIZE = [
    # "_background.png",
    # "_granny.png",
    # "_square.png",
    # "_fan.png",
    # "_snob.png",
    # "_girl.png",
    "_hat.png",
    "_demon.png",
    "_wallet.png",
    "_sock.png",
    "_teabag.png",
]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for filename in FILES_TO_RESIZE:
    source = INPUT_DIR / filename
    destination = OUTPUT_DIR / filename[1:]

    if not source.exists():
        print(f"Не найдено: {filename}")
        continue

    with Image.open(source) as img:
        width, height = img.size
        new_width = round(width * TARGET_HEIGHT / height)

        resized = img.resize(
            (new_width, TARGET_HEIGHT),
            Image.Resampling.NEAREST
        )

        resized.save(destination)

        print(f"Создано: {destination} ({new_width}x{TARGET_HEIGHT})")

print("Готово! Исходные изображения не изменены.")