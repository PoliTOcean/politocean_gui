from PyQt5.QtWidgets import QLabel, QWidget

import pytest
import re

from QDiveTimer import QDiveTimer

startTime = "00:00:00"


@pytest.fixture
def diveTimer(qtbot):
    qDiveTimer = QDiveTimer()
    return qDiveTimer


def test_time(diveTimer):
    assert re.match(
        r'^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$', diveTimer.time)


def test_init(diveTimer):
    assert diveTimer.started == False
    assert diveTimer.paused == False
    assert diveTimer.elapsed == 0
    assert diveTimer.time == startTime


def test_start(diveTimer):
    diveTimer.start()

    assert diveTimer.started == True
    assert diveTimer.paused == False


def test_pause(diveTimer):
    diveTimer.start()
    diveTimer.pause()

    assert diveTimer.started == True
    assert diveTimer.paused == True


def test_stop(diveTimer):
    diveTimer.start()
    diveTimer.stop()

    assert diveTimer.started == False
    assert diveTimer.paused == False
    assert diveTimer.time == startTime
