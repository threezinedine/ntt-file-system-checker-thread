from PyQt5.QtWidgets import *
from test_widget import *
from nttinject import *
from _testWidgetViewModel import *
from ntt_file_system_checker import *


@dependency_inject(TestWigetViewModel)
class TestWidget(QWidget):
    def __init__(self, vmTestWidget: TestWigetViewModel) -> None:
        super().__init__()
        self._vmTestWidget = vmTestWidget
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._cssChecker: IFileContentChecker = FileContentChecker("test.css")

        self._vmTestWidget.ClickedTimesChanged.Connect(self._OnClickedTimesChanged)
        self._ui.pushButton.clicked.connect(self._OnClicked_PushButton)

        self._OnCssContentChanged()
        self._cssChecker.ContentChanged.Connect(self._OnCssContentChanged)

    def _OnCssContentChanged(self) -> None:
        try:
            self.setStyleSheet(self._cssChecker.Content)
        except Exception as e:
            print(e)

    def _OnClickedTimesChanged(self, nClickedTimes: int) -> None:
        self._ui.label.setText(f"Clicked Times: {nClickedTimes}")

    def _OnClicked_PushButton(self) -> None:
        self._vmTestWidget.IncreaseClickedTimes()