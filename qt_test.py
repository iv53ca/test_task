import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel

from PIL.ImageQt import ImageQt
import csv_processing

class FileLoader(QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализировали окно, задаем его параметры
        self.setWindowTitle("Преобразование CSV в изображение")
        self.setGeometry(500, 100, 500, 500)

        self.image_labels = []
        self.image_paths = []
        self.current_image_index = 0

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)
        
        # Прописываем кнопку для выбора файлов с компьютера
        self.button = QPushButton("Выберите файлы", self)
        self.button.clicked.connect(self.load_files)
        layout.addWidget(self.button)

        # Создаем кнопку для переключения на предыдущую картинку
        self.prev_button = QPushButton("Предыдущее изображение", self)
        self.prev_button.clicked.connect(self.show_prev_image)
        layout.addWidget(self.prev_button)

        # Создаем кнопку для переключения на следующую картинку
        self.next_button = QPushButton("Следующее изображение", self)
        self.next_button.clicked.connect(self.show_next_image)
        layout.addWidget(self.next_button)

        # Создаем кнопку для сохранения текущей картинки в одном из трех форматов
        self.save_button = QPushButton("Сохранить изображение", self)
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Инициализируем функцию обработки csv-файла
    def pic_output(self, file_path):
        return csv_processing.csv2png(file_path)

    # Функция загрузки csv-файлов. 
    def load_files(self):
        file_dialog = QFileDialog() # Создание диалогового окна для выбора файлов
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("CSV files (*.csv)") # Установка фильтра имени файла для отображения только файлов с расширением .csv
        
        # Если пользователь нажал кнопку "Открыть" в диалоговом окне выбора файлов
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_paths = file_dialog.selectedFiles() # Получаем список выбранных файлов
            # Для каждого выбранного файла создаем изображение и преобразуем его в QPixmap
            for file_path in file_paths:
                image = self.pic_output(file_path)
                qimage = ImageQt(image)
                pixmap = QPixmap.fromImage(qimage)

                # Создаем метку изображения, устанавливаем на нее QPixmap и масштабируем ее
                image_label = QLabel(self)
                image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

                # Добавляем метку изображения и путь к файлу в списки класса
                self.image_labels.append(image_label)
                self.image_paths.append(file_path)

            self.show_image()

    # Функция отображения текущего файла на диалоговом окне
    def show_image(self):

        # Проверяем, что в списке image_labels есть хотя бы одна метка изображения
        if len(self.image_labels) > 0:
            current_image = self.image_labels[self.current_image_index] # Получаем текущую метку изображения из списка по индексу 
            self.image_label.setPixmap(current_image.pixmap()) # Устанавливаем на image_label главной формы QPixmap текущего изображения
    
    # Функция переключения на предыдущее изображение
    def show_prev_image(self):
        if len(self.image_labels) > 0:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_labels) # Вычисляем индекс предыдущего изображения, учитывая кольцевое обращение к списку (чтобы не выйти за границы)
            self.show_image()

    # Функция переключения на предыдущее изображение
    def show_next_image(self):
        if len(self.image_labels) > 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_labels) # Вычисляем индекс следующего изображения
            self.show_image()

    # Функция сохранения текущего изображения
    def save_image(self):
        if len(self.image_labels) > 0:
            current_image = self.image_labels[self.current_image_index]
            pixmap = current_image.pixmap() # Получаем текущее изображение из списка

            # Открываем диалоговое окно для сохранения файла
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "PNG files (*.png);;JPEG files (*.jpg);;BMP files (*.bmp)")
            if file_path:
                if file_path.endswith(".png"):
                    pixmap.save(file_path, "PNG")
                elif file_path.endswith(".jpg"):
                    pixmap.save(file_path, "JPG")
                elif file_path.endswith(".bmp"):
                    pixmap.save(file_path, "BMP")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileLoader()
    window.show()
    sys.exit(app.exec())
