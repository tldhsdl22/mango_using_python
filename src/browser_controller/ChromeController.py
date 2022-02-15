'''
import abc
class BrowserController(metaclass=abc.ABCMeta):
    """A demo shape class"""

    @abc.abstractmethod
    def test1(self):
        """Draw a circle"""
        raise NotImplemented

    @abc.abstractmethod
    def test2(self):
        """ Draw a square"""
        raise NotImplemented
'''

class ChromeController():
    def zaza(self):
        print("11")
    def test1(self):
        print("Chrome 1")

    def test2(self):
        print("Chrome 2")


controller = ChromeController()

controller.test2()