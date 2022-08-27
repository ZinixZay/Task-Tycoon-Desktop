import sys

import typing

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from db import *
from axuilary_funcs import *


class SelectedUser:
    def __init__(self, username):
        self.username = username


class Screens(QtWidgets.QStackedWidget):
    def closeEvent(self, event):
        close_all_threads()
        event.accept()


class MenuScreen(QMainWindow):
    def __init__(self, stack):
        super(MenuScreen, self).__init__()
        loadUi("screens/menu.ui", self)
        QFontDatabase.addApplicationFont('fonts/Default_SC.ttf')

        self.Stack = stack

        self.submit_button.setIcon(QIcon('img/btn_submit.png'))
        self.submit_button.setIconSize(QSize(100, 100))

        self.submit_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.submit_button.clicked.connect(self.browse_folder)

        self.label.setFont(QFont('Default_SC', 35))

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения файла')
        create_excel_task_statistic(directory, menu_screen.task.currentText())


class LoginScreen(QMainWindow):
    def __init__(self, stack):
        super(LoginScreen, self).__init__()
        loadUi("screens/login.ui", self)
        QFontDatabase.addApplicationFont('fonts/Default_SC.ttf')

        self.stack = stack

        self.login_input.setFont(QFont('Default_SC', 20))

        self.password_input.setFont(QFont('Default_SC', 20))

        self.label.setFont(QFont('Default_SC', 20))
        self.label_2.setFont(QFont('Default_SC', 20))
        self.label_3.setFont(QFont('Default_SC', 40))

        self.sign_in_button.setFont(QFont('Default_SC', 26))
        self.sign_in_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.sign_in_button.clicked.connect(self.sign_clicked)

    def sign_clicked(self) -> None:

        """
        sign in button trigger
        1. check input correctioness
        2.1. if not correct -> show error message
        2.2. if correct -> ...
        :return:  nothing
        """

        username = self.login_input.text()
        psw = self.password_input.text()
        if not check_login_correctness(username, psw):
            show_critical_messagebox('Invalid username or password')
        else:
            stack_navigation(self.stack, 1)


def application() -> None:
    global menu_screen
    global login_screen

    app = QApplication(sys.argv)

    # Stacked widget and screen creation
    Stack = Screens()
    menu_screen = MenuScreen(Stack)
    login_screen = LoginScreen(Stack)
    Stack.setWindowTitle('Task Tycoon')
    Stack.setFixedSize(800, 600)

    # Font setting
    # QFontDatabase.addApplicationFont('fonts/Default_SC.ttf')
    # font = QFont('Default_SC')
    # Stack.setFont(font)

    # Stacked widget incremention
    Stack.addWidget(login_screen)
    Stack.addWidget(menu_screen)

    Stack.show()

    sys.exit(app.exec_())


def show_critical_messagebox(text: str = 'blank') -> None:

    """
    show critical messagebox with transmitted text
    :param text: text which person will see in the messagebox
    :return: Nothing
    """

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle('Error')
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()


def stack_navigation(stack: Screens, step: int = 1) -> None:

    """
    Changes the screen that person sees
    :param stack: Stacked widget which is going to be swiped
    :param step: Direction and mesaure of swiping
    :return: Nothing
    """

    stack.setCurrentIndex(stack.currentIndex() + step)

    if stack.currentIndex() == 1:

        username = login_screen.login_input.text()
        capitalized_username = ' '.join([*map(lambda x: x.capitalize(), get_app_user_name(username).split())])
        menu_screen.label.setText(f"Welcome, {capitalized_username}!")

        menu_screen.task.addItems(get_task_titles(get_app_user_name(username)))


if __name__ == "__main__":
    application()
