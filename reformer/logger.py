import time
import colored
import colorama

from typing import Protocol


__all__ = ("Logger", "getlogger",)

colorama.just_fix_windows_console()

class _logger(object):
	__fn: str

	def __init__(self):
		try:
			raise Exception()
		except Exception as e:
			self.__fn = e.__traceback__.tb_frame.f_globals['__spec__'].name

	def __lshift__(self, message: str) -> None:
		now = time.localtime(time.time())

		print(rf"{colored.Fore.light_coral}[%s] {colored.Fore.light_salmon_1}[%s] {colored.Fore.grey_30}[%s] {colored.Fore.grey_50}%s" % (
			time.strftime("%y %b %d", now),
			time.strftime("%H:%M:%S", now),
			self.__fn,
			message
		) + colored.Style.RESET)

class Logger(Protocol):
	def __lshift__(self, message: str) -> None:
		"""Logs a message."""
		...

def getlogger() -> Logger:
	return _logger()
