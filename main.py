import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QVBoxLayout, QDialog, QTableWidgetItem, QTableWidget, QHBoxLayout, QFileDialog
import pymysql
from new_test import Ui_Form
from PyQt5.QtGui import QFont
from keras.applications.vgg19 import VGG19
from keras.applications.convnext import preprocess_input
from video import MaskRecognition
from sklearn.preprocessing import MinMaxScaler
from keras.utils import img_to_array, load_img
from config.config import UpdateUserStatus

font = QFont()
font.setPointSize(20)



class ChooseType(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.resize(400, 200)
        self.setWindowTitle('Put Form')

        layout = QVBoxLayout()

        # Create three buttons and add them to the layout manager
        self.btn1 = QPushButton('PHOTO')
        self.btn1.clicked.connect(self.photo)
        layout.addWidget(self.btn1)

        self.btn2 = QPushButton('EMOTION')
        self.btn2.clicked.connect(self.emotion)
        layout.addWidget(self.btn2)

        self.btn3 = QPushButton('CAMERA')
        self.btn3.clicked.connect(self.camera)
        layout.addWidget(self.btn3)

        # Set the layout manager as the main layout of the window
        self.setLayout(layout)

    def photo(self):
        self.photo = Photo()
        self.photo.show()

    def emotion(self):
        dialog = QDialog(self)

        ui_form = Ui_Form()
        ui_form.setupUi(dialog)

        dialog.exec_()

    def camera(self):
        mask = MaskRecognition()
        mask.recognize(self.username)


class Photo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 200)
        self.setWindowTitle('Photo Forum')
        self.image_label = QLabel(self)
        if hasattr(self.image_label, 'setAlignment'):
            self.image_label.setAlignment(Qt.AlignCenter)
        else:
            self.image_label.setAlignment(int(Qt.AlignCenter))

        self.button = QPushButton('pick a picture', self)
        self.button.clicked.connect(self.select_image)
        self.show()

    def select_image(self):
        fname = QFileDialog.getOpenFileName(self, 'pick picture', '.', 'Image Files (*.png *.jpg *.bmp)')[0]
        if fname:
            self.detect_mask(fname)

    def detect_mask(self, fname):
        img = load_img(fname, target_size=(224, 224))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        scaler = MinMaxScaler()
        x_scaled = scaler.fit_transform(x.reshape(-1, 1)).reshape(x.shape)
        mean_value = np.mean(x_scaled)
        # Print the mean value
        print(mean_value)
        # Save the weights of the VGG19 model
        model = VGG19(weights='imagenet')
        pred = model.predict(x)
        result = np.argmax(pred)
        print(result)
        if mean_value > 0.3:
            QMessageBox.information(self, 'no_mask', 'no_mask!')


        else:
            QMessageBox.information(self, 'masked', 'masked!')

        if hasattr(self.image_label, 'setAlignment'):
            self.image_label.setAlignment(Qt.AlignCenter)
        else:
            self.image_label.setAlignment(int(Qt.AlignCenter))


class Signup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Signup Form')
        self.setFixedSize(400, 200)

        # Labels
        self.lbl_username = QLabel('Username:', self)
        self.lbl_username.move(50, 50)
        self.lbl_password = QLabel('Password:', self)
        self.lbl_password.move(50, 100)

        # Text fields
        self.txt_username = QLineEdit(self)
        self.txt_username.move(150, 50)
        self.txt_password = QLineEdit(self)
        self.txt_password.move(150, 100)
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Button
        self.btn_signup = QPushButton('Signup', self)
        self.btn_signup.move(150, 150)
        self.btn_signup.clicked.connect(self.signup)

        # MySQL database
        self.db = pymysql.connect(
            user="root",
            password="xyz",
            database="finalproject"
        )

    def signup(self):
        cursor = self.db.cursor()
        username = self.txt_username.text()
        password = self.txt_password.text()

        if len(username) < 6 or len(password) < 6:
            QMessageBox.warning(self, 'Error', 'Username and password must be at least 6 characters long',
                                QMessageBox.Ok)
            return
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        cursor.execute(sql, val)
        self.db.commit()
        QMessageBox.information(self, 'Information', 'Signup Successfully', QMessageBox.Ok)
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.setFixedSize(400, 200)

        # Labels
        self.lbl_username = QLabel('Username:', self)
        self.lbl_username.setFont(font)
        self.lbl_username.move(50, 50)
        self.lbl_password = QLabel('Password:', self)
        self.lbl_password.setFont(font)
        self.lbl_password.move(50, 100)

        # Text fields
        self.txt_username = QLineEdit(self)
        self.txt_username.move(150, 50)
        self.txt_password = QLineEdit(self)
        self.txt_password.move(150, 100)
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Buttons
        self.btn_login = QPushButton('Login', self)
        self.btn_login.move(100, 150)
        self.btn_login.clicked.connect(self.login)
        self.btn_signup = QPushButton('Signup', self)
        self.btn_signup.move(200, 150)
        self.btn_signup.clicked.connect(self.show_signup)

        # MySQL database
        self.db = pymysql.connect(
            user="root",
            password="xyz",
            database="finalproject"
        )
        self.logged_in_username = ""

    def login(self):
        cursor = self.db.cursor()
        username = self.txt_username.text()
        password = self.txt_password.text()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, password)
        cursor.execute(sql, val)

        # If login is successful, open the corresponding window
        if cursor.fetchone():
            # Check if the user is an admin
            print(username + " login")
            self.logged_in_username = username
            if username == "Admin":
                QMessageBox.information(self, 'Success', 'Admin Login Successful!')
                self.open_admin_window()
            else:
                QMessageBox.information(self, 'Success', 'Login Successful!')
                self.open_type_window()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Username or Password!')

    def open_admin_window(self):
        # Open the administrator user interface window
        print("Opening admin window")  # Add this line for debugging purposes
        self.admin_window = AdminWindow()
        self.admin_window.show()

    def open_type_window(self):
        # Open the camera window
        print("Opening Choose type window")  # Add this line for debugging purposes
        self.type = ChooseType(self.logged_in_username)  # Pass the username as a parameter
        self.type.show()

    def show_signup(self):
        self.signup = Signup()
        self.signup.show()



def view_user_details(username):
    # Establish a connection to the MySQL database
    db_connection = pymysql.connect(
        host="localhost",
        user="root",
        password="xyz",
        database="finalproject"
    )
    # Create a cursor to execute SQL queries
    cursor = db_connection.cursor()

    # Execute a query to retrieve user details
    select_query = f"SELECT mask_time, masked FROM `{username}`"
    cursor.execute(select_query)

    # Fetch all rows of user details from the query result
    user_details = cursor.fetchall()

    # Create a message box to display the user details
    # 创建一个自定义的消息框对象
    message_box = CustomMessageBox()
    message_box.setText(f"User: {username}")

    # Create a table widget to display the user details
    table_widget = QTableWidget()
    QTableWidget.setFixedSize(table_widget, 300, 400)
    table_widget.setColumnCount(2)  # Two columns: mask_time, masked
    table_widget.setHorizontalHeaderLabels(["Mask Time", "Masked"])

    # Populate the table widget with user details
    table_widget.setRowCount(len(user_details))
    for row, data in enumerate(user_details):
        table_widget.setItem(row, 0, QTableWidgetItem(str(data[0])))  # mask_time
        table_widget.setItem(row, 1, QTableWidgetItem(data[1]))  # masked

    # Set the table widget as the message box's detailed text
    # message_box.setDetailedText("")
    message_box.layout().addWidget(table_widget)
    # message_box.resize(500, 300)  # Set the width and height of the message box

    # Execute the message box
    message_box.exec()

    # Close the database connection and cursor
    cursor.close()
    db_connection.close()

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 800)
        self.setWindowTitle('Admin Form')

        # Create a table to display user information
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Three columns: ID, Username, Password
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Password", "View"])
        # Set the table to stretch horizontally
        self.table.horizontalHeader().setStretchLastSection(True)

        # Create a button to delete selected user
        self.delete_button = QPushButton("Delete User")
        self.delete_button.clicked.connect(self.delete_user)

        # Create a layout and add the table and delete button to it
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        # Populate the table with user information from the database
        self.populate_table()

    def populate_table(self):
        # Clear the existing table content
        self.table.setRowCount(0)

        # Establish a connection to the MySQL database
        db_connection = pymysql.connect(
            user="root",
            password="xyz",
            database="finalproject"
        )

        # Create a cursor to execute SQL queries
        cursor = db_connection.cursor()

        # Execute a query to retrieve user information
        query = "SELECT * FROM users"
        cursor.execute(query)

        # Fetch all rows of user data from the query result
        user_data = cursor.fetchall()

        # Iterate over the user data and populate the table
        for row, data in enumerate(user_data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(data[0])))  # Assuming ID is in the first column
            self.table.setItem(row, 1, QTableWidgetItem(data[1]))  # Assuming username is in the second column
            self.table.setItem(row, 2, QTableWidgetItem(data[2]))  # Assuming password is in the third column

            # Create a button for each user
            view_button = QPushButton("View")
            view_button.clicked.connect(lambda checked, user=data[1]: view_user_details(user))

            # Create a layout for the button
            button_layout = QHBoxLayout()
            button_layout.addWidget(view_button)

            # Create a widget to hold the layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            self.table.setCellWidget(row, 3, button_widget)  # Assuming the button is in the fourth column


        # Close the database connection and cursor
        cursor.close()
        db_connection.close()

    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            confirm = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this user?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                # Retrieve the user ID from the selected row
                user_id = int(self.table.item(selected_row, 0).text())
                # Establish a connection to the MySQL database
                db_connection = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="xyz",
                    database="finalproject"
                )
                # Create a cursor to execute SQL queries
                cursor = db_connection.cursor()
                # Execute a query to delete the user with the specified ID
                delete_query = "DELETE FROM users WHERE id = %s"
                cursor.execute(delete_query, (user_id,))
                db_connection.commit()
                # Close the database connection and cursor
                cursor.close()
                db_connection.close()
                # Remove the selected row from the table
                self.table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Warning", "No user selected.")


class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStandardButtons(QMessageBox.Ok)

    def showEvent(self, event):
        self.setGeometry(100, 100, 400, 200)  # Set the size of the message box
        self.setStyleSheet("QMessageBox { font-size: 14px; }")  # Set the style of the message box
        super().showEvent(event)





if __name__ == '__main__':
    UpdateUserStatus()
    app = QApplication(sys.argv)
    login = MainWindow()
    login.show()
    sys.exit(app.exec_())
