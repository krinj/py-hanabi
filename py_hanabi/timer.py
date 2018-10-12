# -*- coding: utf-8 -*-

"""
Use this to time an event according to a key, and measure unit performance.
"""

import time

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class TimeObject:
    def __init__(self, key: str):
        self.key = key
        self.count = 0
        self.duration = 0
        self.previous_timestamp = 0
        self.is_timing = False

    def reset(self):
        self.count = 0
        self.duration = 0
        self.previous_timestamp = 0
        self.is_timing = False

    def start(self):
        if not self.is_timing:
            self.previous_timestamp = time.time()
            self.is_timing = True
            self.count += 1

    def stop(self):
        if self.is_timing:
            current_timestamp = time.time()
            self.duration += current_timestamp - self.previous_timestamp
            self.previous_timestamp = current_timestamp
            self.is_timing = False


class Timer:
    # Singleton instance.
    _INSTANCE = None

    # ==================================================================================================================
    # Public Interface -------------------------------------------------------------------------------------------------
    # ==================================================================================================================

    @staticmethod
    def get_instance() -> "Timer":
        if Timer._INSTANCE is None:
            Timer()
        return Timer._INSTANCE

    @staticmethod
    def start(key: str) -> None:
        Timer.get_instance()._start(key)

    @staticmethod
    def stop(key: str) -> None:
        Timer.get_instance()._stop(key)

    @staticmethod
    def end(key: str) -> float:
        return Timer.get_instance()._end(key, count_units=False)

    @staticmethod
    def end_per_unit(key: str) -> float:
        return Timer.get_instance()._end(key, count_units=True)

    @staticmethod
    def reset(key: str) -> None:
        Timer.get_instance()._reset(key)

    # ==================================================================================================================
    # Private Methods --------------------------------------------------------------------------------------------------
    # ==================================================================================================================

    def __init__(self):
        self._time_objects = {}
        Timer._INSTANCE = self

    def _get_time_object(self, key: str):
        if key not in self._time_objects:
            self._time_objects[key] = TimeObject(key)
        return self._time_objects[key]

    def _start(self, key: str):
        time_object = self._get_time_object(key)
        time_object.start()

    def _stop(self, key: str):
        time_object = self._get_time_object(key)
        time_object.stop()

    def _end(self, key: str, count_units: bool = False) -> float:
        time_object = self._get_time_object(key)
        time_object.stop()
        duration = time_object.duration
        if count_units:
            duration /= time_object.count

        time_header = "(Timer) {}"
        if time_object.count > 1:
            time_header += " ({} Units)"
        print(f"{time_header.format(time_object.key, time_object.count)}: {duration:.2f}s")
        time_object.reset()
        return duration

    def _reset(self, key: str):
        time_object = self._get_time_object(key)
        time_object.reset()
