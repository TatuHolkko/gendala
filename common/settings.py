import configparser
from typing import Callable, List, TypeVar

T = TypeVar('T')


class Settings:
    """
    Object for reading a settings ini file
    """

    def __init__(self, iniPath: str) -> None:
        """
        Initialize the ini reader

        Args:
            iniPath (str): Path to the ini file
        """
        self.config = configparser.ConfigParser()
        self.config.read(iniPath)
    
    def __str__(self) -> str:
        s = ""
        for section, content in self.config.items():
            s += section + ":\n"
            for setting, value in content.items():
                s += "\t" + setting + ": " + value + "\n"
        return s

    def getBool(self, section: str, setting: str) -> bool:
        """
        Get a boolean setting.

        Will raise an exception if the boolean value is invalid

        Args:
            section (str): Section name
            setting (str): Setting name

        Raises:
            ValueError: If the value is not one of "true", "false", "1", "0"

        Returns:
            bool: Setting value
        """
        s = self.getItem(section=section, setting=setting, constructor=str)
        s = s.strip().lower()
        if s == "false" or s == "0":
            return False
        elif s == "true" or s == "1":
            return True
        raise ValueError("Invalid boolean value: " + s)

    def getItem(self, section: str, setting: str,
                constructor: Callable[[str], T]) -> T:
        """
        Get a single item

        Args:
            section (str): Section name
            setting (str): Setting name
            constructor (Callable[[str], T]): Constructor that constructs the return value

        Returns:
            T: Return value
        """
        if constructor == bool:
            return self.getBool(section=section, setting=setting)
        else:
            return constructor(self.config[section][setting])

    def getList(self, section: str, setting: str,
                constructor: Callable[[str], T]) -> List[T]:
        """
        Get a list of items

        Args:
            section (str): Section name
            setting (str): Setting name
            constructor (Callable[[str], T]): Constructor that constructs each element

        Returns:
            List[T]: Return value
        """
        settingstring = self.getItem(section, setting, str)
        return [constructor(value) for value in settingstring.split(',')]
