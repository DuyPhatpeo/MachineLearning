import sys
import pickle
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QMessageBox, QVBoxLayout
)
from PyQt5.QtGui import QFont

# ------------------------------
# 1. Load mô hình và LabelEncoder đã huấn luyện từ file
# ------------------------------
with open("weather_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Danh sách các trường nhập liệu theo thứ tự
feature_columns = ["Temp", "Feels", "Gust", "Rain", "Humidity", "Cloud", "Pressure", "Wind Speed"]

# Từ điển ánh xạ tên thời tiết từ tiếng Anh sang tiếng Việt
weather_vn = {
    "Clear": "Trời quang đãng",
    "Cloudy": "Trời nhiều mây",
    "Mist": "Sương mù",
    "Overcast": "Trời u ám",
    "Rain": "Mưa",
    "Sunny": "Nắng"
}

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dự đoán Thời Tiết")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        font_label = QFont("Helvetica", 14)
        font_input = QFont("Helvetica", 14)
        font_button = QFont("Helvetica", 14, QFont.Bold)

        # Tạo layout chính
        layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(10)

        # Tạo các trường nhập liệu
        self.inputs = {}
        fields = [
            ("Nhiệt độ (Temp) (°C):", "Temp"),
            ("Cảm giác (Feels) (°C):", "Feels"),
            ("Gió giật (Gust) (m/s):", "Gust"),
            ("Mưa (Rain) (mm):", "Rain"),
            ("Độ ẩm (Humidity) (%):", "Humidity"),
            ("Mây (Cloud) (%):", "Cloud"),
            ("Áp suất (Pressure) (hPa):", "Pressure"),
            ("Tốc độ gió (Wind Speed) (m/s):", "Wind Speed")
        ]

        for i, (label_text, key) in enumerate(fields):
            label = QLabel(label_text)
            label.setFont(font_label)
            grid.addWidget(label, i, 0)
            line_edit = QLineEdit()
            line_edit.setFont(font_input)
            grid.addWidget(line_edit, i, 1)
            self.inputs[key] = line_edit

        layout.addLayout(grid)

        # Nút dự đoán
        btn_predict = QPushButton("Dự đoán")
        btn_predict.setFont(font_button)
        btn_predict.clicked.connect(self.predict_weather)
        layout.addWidget(btn_predict)

        self.setLayout(layout)

    def predict_weather(self):
        try:
            # Lấy dữ liệu từ các ô nhập và chuyển sang float
            features = [float(self.inputs[col].text()) for col in feature_columns]
            features = np.array([features])
            prediction = model.predict(features)[0]
            predicted_label = label_encoder.inverse_transform([prediction])[0]
            predicted_label_vn = weather_vn.get(predicted_label, predicted_label)
            self.show_result(predicted_label_vn)
        except ValueError:
            QMessageBox.critical(self, "Lỗi", "Vui lòng nhập giá trị hợp lệ.")

    def show_result(self, result):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Kết quả")
        msg.setText(f"Dự đoán: {result}")
        msg.setFont(QFont("Helvetica", 14))
        msg.exec_()
        # Xóa nội dung các ô nhập sau khi hiển thị kết quả
        for line_edit in self.inputs.values():
            line_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Áp dụng QSS để tùy chỉnh giao diện
    app.setStyleSheet("""
        QWidget {
            background-color: #f0f0f0;
        }
        QLabel {
            color: #333;
        }
        QLineEdit {
            border: 2px solid #ccc;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #0078D7;
        }
        QPushButton {
            background-color: #0078D7;
            color: white;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
    """)

    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
