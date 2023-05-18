import os
import random
import shutil
import sys
import subprocess
from os import listdir, path, getcwd
from PIL import Image
from PyQt5.QtGui import QTextCursor
from PyQt5 import uic, QtGui  # Импортируем uic
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QWidget, QFileDialog, \
    QGraphicsOpacityEffect, QLabel, QTextEdit, QLineEdit
from PyQt5 import QtCore, QtWidgets
from textRedactor import Ui_MainWindow
import subprocess as sp
import ctypes
import platform, socket, re, uuid, json, psutil, logging


def get_system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


commands = {
    'cd': ['cd',
           'Переходит по указанной директории'],
    'systeminfo': ['systeminfo',
                   'Системная информация'],
    'clear': ['clear',
              'Очищает консоль'],
    'help': ['help',
             'Выводит все команды'],
    'ls': ['ls',
           'Выводит все файлы и папки в текущей директории'],
    'nano': ['nano',
             'текстовый редактор'],
    'ls.dirs': ['ls.dirs',
                'Выводит только папки в текущей директории'],
    'ls.files': ['ls.files',
                 'Выводит только файлы в текущей директории'],
}

hacker = '''⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀
⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣤⠶⠶⠶⠰⠦⣤⣀⠀⠙⣷⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⢀⣀⣤⢴⠆⠲⠶⠶⣤⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣆⠀⠀⢠⣾⣫⣶⣾⣿⣿⣿⣿⣷⣯⣿⣦⠈⠃⡇⠀⠀⠀⠀⢸⠘⢁⣶⣿⣵⣾⣿⣿⣿⣿⣷⣦⣝⣷⡄⠀⠀⡰⠂⠀
⠀⠀⣨⣷⣶⣿⣧⣛⣛⠿⠿⣿⢿⣿⣿⣛⣿⡿⠀⠀⡇⠀⠀⠀⠀⢸⠀⠈⢿⣟⣛⠿⢿⡿⢿⢿⢿⣛⣫⣼⡿⣶⣾⣅⡀⠀
⢀⡼⠋⠁⠀⠀⠈⠉⠛⠛⠻⠟⠸⠛⠋⠉⠁⠀⠀⢸⡇⠀⠀⠄⠀⢸⡄⠀⠀⠈⠉⠙⠛⠃⠻⠛⠛⠛⠉⠁⠀⠀⠈⠙⢧⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⢠⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠁⣿⠇⠀⠀⠀⠀⢸⡇⠙⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠰⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠖⡾⠁⠀⠀⣿⠀⠀⠀⠀⠀⠘⣿⠀⠀⠙⡇⢸⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠄⠀
⠀⠀⢻⣷⡦⣤⣤⣤⡴⠶⠿⠛⠉⠁⠀⢳⠀⢠⡀⢿⣀⠀⠀⠀⠀⣠⡟⢀⣀⢠⠇⠀⠈⠙⠛⠷⠶⢦⣤⣤⣤⢴⣾⡏⠀⠀
⠀⠀⠈⣿⣧⠙⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢊⣙⠛⠒⠒⢛⣋⡚⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠁⣾⡿⠀⠀⠀
⠀⠀⠀⠘⣿⣇⠈⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⡟⠁⣼⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠘⣿⣦⠀⠻⣿⣷⣦⣤⣤⣶⣶⣶⣿⣿⣿⣿⠏⠀⠀⠻⣿⣿⣿⣿⣶⣶⣶⣦⣤⣴⣿⣿⠏⢀⣼⡿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢿⣷⣄⠙⠻⠿⠿⠿⠿⠿⢿⣿⣿⣿⣁⣀⣀⣀⣀⣙⣿⣿⣿⠿⠿⠿⠿⠿⠿⠟⠁⣠⣿⡿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠻⣯⠙⢦⣀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⣠⠴⢋⣾⠟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢧⡀⠈⠉⠒⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⠒⠉⠁⢀⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠃⠀⠀⠀⠀'''

errorFormat = '<font color="red">{}</font>'
warningFormat = '<font color="orange">{}</font>'
validFormat = '<font color="green">{}</font>'
darkgreenFormat = '<font color="#80CF0C";">{}</font>'
whiteFormat = '<font color="#A1A1A1">{}</font>'
titleFormat = '<font style="color:#010101; background-color: #1F4D3C">{}</font>'


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('textRedactor.ui', self)

        self.timer = QTimer()
        self.timer.setInterval(503)
        self.timer.timeout.connect(self.timeStep)
        self.timer.start()

        self.pushButton.clicked.connect(self.close_nano)
        self.setMinimumSize(700, 400)
        self.lineEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: #162e22")
        self.textEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: #162e22")
        self.textEdit.setReadOnly(True)
        self.pushButton_2.clicked.connect(self.terminate_file)
        self.pushButton_4.clicked.connect(self.save_file)
        self.pushButton_3.clicked.connect(self.open_file_1)

        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton.hide()
        self.pushButtonEnter.clicked.connect(self.send_command)
        self.fl = ""
        self.fl_is_run = False
        self.function_set_txt = None
        self.label.setText(f'┌{os.getcwd()}┐')
        self.set_cursor()
        self.text_main = f'''<span style="color:green;">НАЧАЛО РАБОТЫ!</span><br>'''

    def resizeEvent(self, event):
        self.textEdit.resize(self.size().width() - 26, self.size().height() - 123)
        self.lineEdit.resize(self.size().width() - 88, 40)
        self.lineEdit.move(self.lineEdit.x(), self.size().height() - 73)
        self.pushButton_4.move(10, self.size().height() - 80)
        self.pushButton_3.move(120, self.size().height() - 80)
        self.pushButton_2.move(230, self.size().height() - 80)
        self.pushButton.move(340, self.size().height() - 80)
        self.pushButtonEnter.move(self.lineEdit.width() + 10, self.size().height() - 73)

    # слот для таймера
    def timeStep(self):
        ex.setWindowTitle("".join(list(map(lambda x: f'{x}!' if random.randrange(0, 4) == 2 else f'{x}.', [str(random.choice([0, 1])) for i in range(10)]))))

    def send_command(self):
        def set_txt(out=""):
            self.textEdit.setText(
                f'{self.text_main}{titleFormat.format(cp + "~")} {command}<br><span style="background-color: #AB274F">#</span> {out if out else output}')
            self.text_main = self.textEdit.toHtml()
            self.set_cursor()
            self.label.setText(f'┌{os.getcwd()}┐')

        if not self.function_set_txt:
            self.function_set_txt = set_txt

        command = self.lineEdit.text()
        if not command:
            return
        output = ""
        fcm = command.split()[0]
        fcms = command.split()[0].split('.')
        arg = command[len(fcm) + 1:]
        cp = os.getcwd()
        ch = "<font color='#162e22'>&nbsp;</font>"
        path_ = ''

        if fcm in commands:
            if fcm == commands['cd'][0]:
                try:
                    os.chdir(arg if ":" in arg else (os.getcwd() + '\\' + arg))
                    output = os.getcwd()
                except Exception as ex:
                    output += errorFormat.format(ex)
            elif fcm == commands['clear'][0]:
                self.text_main = ''
                output = 'Консоль очищена.'
            elif fcm == commands['nano'][0]:
                try:
                    path_ = arg if ":" in arg else (os.getcwd() + '\\' + arg)

                except Exception as ex:
                    output += errorFormat.format(ex)
            elif fcms[0] == commands['ls'][0]:
                onlyfiles = ''
                if len(fcms) > 1:
                    if fcms[1] == 'DIRS':
                        onlyfiles = [f for f in listdir(cp) if not os.path.isfile(os.path.join(cp, f))]
                    elif fcms[1] == 'FILES':
                        onlyfiles = [f for f in listdir(cp) if os.path.isfile(os.path.join(cp, f))]
                else:
                    # if os.path.isfile(os.path.join(cp, f))
                    onlyfiles = [f for f in listdir(cp)]

                output = f",{ch * 2}".join(onlyfiles)
            elif fcm == commands['help'][0]:
                try:
                    for i in commands:
                        name = f"{i}:"
                        ln = 20 - len(name)
                        output += '<br>' + f'{validFormat.format(name)}{ln * ch}{darkgreenFormat.format(commands[i][1])}</span>'
                except Exception as ex:
                    output += errorFormat.format(ex)
            elif fcm == commands['systeminfo'][0]:
                inf = json.loads(get_system_info())

                for i in inf:
                    name = f"{i}:"
                    ln = 20 - len(name)
                    output += f'<br>{validFormat.format(name)}{ln * ch}{darkgreenFormat.format(inf[i])}</span>'

        else:
            output = warningFormat.format("Команда не обнаружена! (help - список команд)")

        if path_:
            ex = self.active_nano(path_)
            if ex:
                set_txt(ex)
        else:
            set_txt()

    def active_nano(self, pt):
        try:
            self.open_file(pt)
            self.textEdit.setReadOnly(False)
            self.lineEdit.hide()
            self.pushButtonEnter.hide()
            self.pushButton_4.show()
            self.pushButton_3.show()
            self.pushButton_2.show()
            self.pushButton.show()
            return ""
        except Exception as ex:
            print(ex)
            return errorFormat.format(ex)

    def close_nano(self):
        self.textEdit.setReadOnly(True)
        self.lineEdit.show()
        self.pushButtonEnter.show()
        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton.hide()
        self.function_set_txt("nano exit")
        return ""

    def set_cursor(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)

    def run_file(self):
        if self.fl:
            self.fl_is_run = True
            os.system(f'python {self.fl}')

    def open_file_1(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "Text Files(*.txt);;Python File(*.py);;All Files(*)")
        if filename.strip():
            self.open_file(filename)

    def save_file(self):
        filename, ok = QFileDialog.getSaveFileName(self,
                                                   "Сохранить файл",
                                                   ".",
                                                   "All Files(*.*)")
        if ok:
            with open(filename, 'w', encoding="utf-8") as fl:
                fl.write(self.textEdit.toPlainText())

    def terminate_file(self):
        if self.fl_is_run:
            self.fl_is_run = False
            ext_proc = sp.Popen(['python', self.fl.split('\\')[-1]])
            sp.Popen.terminate(ext_proc)

    def open_file(self, file_):
        fl = sys.argv[0]
        fl = fl.replace('/', '\\')
        nm = file_.split("\\")[-1]
        self.fl = ""
        if file_ != fl:
            if file_.endswith('.py') or file_.endswith('.pyr'):
                self.fl = file_
            self.label.setText(f'┌{nm}┐')

            with open(file_, 'r', encoding="utf-8") as fl__:
                tx = fl__.read()
                self.textEdit.setPlainText(tx)
                self.textEdit.setText(f'<a style="color:#95CBBF;">{self.textEdit.toHtml()}</a>')

                count = len(tx.split("\n"))
                self.label_2.setText(f'┌{count}┐')
        self.set_cursor()

    def keyPressEvent(self, e):
        count = len(self.textEdit.toPlainText().split("\n"))
        self.label_2.setText(f'┌{count}┐')
        if e.key() == Qt.Key_Escape:
            self.send_command()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    ex.setMinimumSize(QSize(600, 400))
    sys.exit(app.exec_())
