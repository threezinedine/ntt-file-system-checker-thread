import logging
import sys
import typing
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from ntt_file_system_checker import *
from nttinject import *
from _testWidgetViewModel import *
from _testWidget import *


@dependency_inject(IFileContentCheckingService)
class MainWidget(QWidget):
    def __init__(self, serFileCheckingService: IFileContentCheckingService) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._serFileCheckingService = serFileCheckingService

        self.mainCssChecker: IFileContentChecker = FileContentChecker("main.css")
        self.testButton = QPushButton("Hello")
        self.testButton.setObjectName("test_btn")
        self.layout.addWidget(self.testButton)
        self.layout.addWidget(TestWidget())

        self._OnCssContentChanged()
        self.mainCssChecker.ContentChanged.Connect(self._OnCssContentChanged)

    def _OnCssContentChanged(self) -> None:
        try:
            self.setStyleSheet(self.mainCssChecker.Content)
        except Exception as e:
            print(e)

    def closeEvent(self, a0) -> None:
        self._serFileCheckingService.Stop()
        return super().closeEvent(a0)


@dependency_inject(IFileContentCheckingService)
class MainWindow(QMainWindow):
    def __init__(self, serFileCheckingService: IFileContentCheckingService) -> None:
        super().__init__()
        self._serFileCheckingService = serFileCheckingService
        self.setGeometry(400, 400, 700, 500)

        self.setCentralWidget(MainWidget())

    def closeEvent(self, a0) -> None:
        self._serFileCheckingService.Stop()
        return super().closeEvent(a0)


if __name__ == "__main__":
    serFileContentCheckingService: IFileContentCheckingService = FileContentCheckingService()
    serFileContentCheckingService.Start()

    try:
        app = QApplication(sys.argv)

        injector = Injector()
        injector.AddSingleton(IFileContentCheckingService, lambda: serFileContentCheckingService)
        injector.AddSingleton(TestWigetViewModel, lambda: TestWigetViewModel())

        win = MainWindow()
        win.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        serFileContentCheckingService.Stop()