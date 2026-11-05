from PIL import Image, ImageDraw

# Наша палитра из 20 цветов
colors = [
    "#F3EFEA", "#E8DFD8", "#DCD0C8", "#E5C3B8", "#D3AA9C", 
    "#B88C7D", "#654A4A", "#4E3737", "#856F6B", "#A38B85", 
    "#C4B5B2", "#9E8D8A", "#726666", "#3B3232", "#A7584E", 
    "#C97A60", "#DFA089", "#89453A", "#D1D1D1", "#EFE2D6"
]

# Размеры: 20 цветов по 50 пикселей в ширину, высота 100 пикселей
width_per_color = 50
height = 100
img_width = width_per_color * len(colors)

# Создаем пустое изображение
img = Image.new("RGB", (img_width, height), "white")
draw = ImageDraw.Draw(img)

# Рисуем прямоугольники для каждого цвета
for i, hex_color in enumerate(colors):
    x0 = i * width_per_color
    x1 = x0 + width_per_color
    draw.rectangle([x0, 0, x1, height], fill=hex_color)

# Сохраняем файл
img.save("palette.png")
print("Файл palette.png успешно создан!")