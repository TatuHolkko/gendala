import sys              # nopep8
sys.path.append('..')   # nopep8
from common.settings import Settings
from system.environment import Environment


def main():
    s = Settings('../settings.ini')
    e = Environment(s)
    e.run()


main()
