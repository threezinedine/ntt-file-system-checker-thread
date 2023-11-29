from ntt_signal import Signal


class TestWigetViewModel:
    def __init__(self) -> None:
        self.ClickedTimesChanged = Signal(int)

        self._nClickedTimes: int = 0

    @property
    def ClickedTimes(self) -> int:
        return self._nClickedTimes

    def IncreaseClickedTimes(self) -> None:
        self._nClickedTimes += 1
        self.ClickedTimesChanged.Emit(self._nClickedTimes)