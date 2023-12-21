from cli.detectSerialCli import DetectSerialCli
from cli.ehz import EhzCli
from cli.dd3 import Dd3Cli
from cli.easy import EasyCli
from cli.mt175cli import Mt175Cli
from cli.mt681cli import Mt681Cli


class Cli:
    detect = DetectSerialCli
    mt175 = Mt175Cli
    mt681 = Mt681Cli
    dd3 = Dd3Cli
    ehz = EhzCli
    easy = EasyCli
