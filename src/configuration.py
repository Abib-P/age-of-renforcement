import configparser


class Configuration:
    def __init__(self, file):
        self.__config = configparser.ConfigParser()
        self.__config.read(file)

    def get_string(self, section, key):
        return self.__config.get(section, key)

    def get_int(self, section, key):
        return self.__config.getint(section, key)

    def get_bool(self, section, key):
        return self.__config.getboolean(section, key)
