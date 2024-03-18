import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QMenu, QSizePolicy, QScrollArea


from PIL.ImageQt import ImageQt
import csv_processing

class FileLoader(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Преобразование CSV в изображение")
        self.setGeometry(500, 100, 500, 500)

        self.image_labels = []
        self.image_paths = []
        self.current_image_index = 0

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        self.button = QPushButton("Выберите файлы", self)
        self.button.clicked.connect(self.load_files)
        layout.addWidget(self.button)

        self.prev_button = QPushButton("Предыдущее изображение", self)
        self.prev_button.clicked.connect(self.show_prev_image)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Следующее изображение", self)
        self.next_button.clicked.connect(self.show_next_image)
        layout.addWidget(self.next_button)

        self.save_button = QPushButton("Сохранить изображение", self)
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def pic_output(self, file_path):
        return csv_processing.csv2png(file_path)

    def load_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("CSV files (*.csv)")
        
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                image = self.pic_output(file_path)
                qimage = ImageQt(image)
                pixmap = QPixmap.fromImage(qimage)

                image_label = QLabel(self)
                image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

                self.image_labels.append(image_label)
                self.image_paths.append(file_path)

            self.show_image()

    def show_image(self):
        if len(self.image_labels) > 0:
            current_image = self.image_labels[self.current_image_index]
            self.image_label.setPixmap(current_image.pixmap())
    

    def show_prev_image(self):
        if len(self.image_labels) > 0:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_labels)
            self.show_image()

    def show_next_image(self):
        if len(self.image_labels) > 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_labels)
            self.show_image()

    def save_image(self):
        if len(self.image_labels) > 0:
            current_image = self.image_labels[self.current_image_index]
            pixmap = current_image.pixmap()
        
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
