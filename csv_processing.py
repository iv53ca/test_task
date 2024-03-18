from PIL import Image
import csv

def csv2png (file_path):
    # Чтение файла CSV
    pixels_data = []

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            pixels_data.append(','.join(row).split(','))

    
    # Преобразование данных в изображение
    height = len(pixels_data)
    width = len(pixels_data[1])
    img = Image.new('L', (width, height))
    for i in range(1, height):
        for j in range(0, width):
            pixel_value = int(pixels_data[i][j])
            img.putpixel((j, i), pixel_value)
    return img

        
