import sys

import typing

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from db import *


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

        self.label.setFont(QFont('Default_SC', 40))


class LoginScreen(QMainWindow):
    def __init__(self, stack, menu_label):
        super(LoginScreen, self).__init__()
        loadUi("screens/login.ui", self)
        QFontDatabase.addApplicationFont('fonts/Default_SC.ttf')

        self.Stack = stack
        self.menu_label = menu_label

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
        button trigger
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
            self.menu_label.setText(f"Welcome, {get_app_user_name(username).capitalize()}!")
            stack_navigation(self.Stack, 1)


def application() -> None:
    app = QApplication(sys.argv)

    # Stacked widget and screen creation
    Stack = Screens()
    menu_screen = MenuScreen(Stack)
    login_screen = LoginScreen(Stack, menu_screen.label)
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
    Changes the screen person sees
    :param stack: Stacked widget which is going to be swiped
    :param step: Direction and mesaure of swiping
    :return: Nothing
    """

    stack.setCurrentIndex(stack.currentIndex() + step)


if __name__ == "__main__":
    application()
