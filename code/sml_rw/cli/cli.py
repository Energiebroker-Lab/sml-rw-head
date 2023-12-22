"""
fire cli module
"""
from cli.dd3 import Dd3CliSML, Dd3CliSML2Way, Dd3CliODT, Dd3CliODT2Way
from cli.detect_serial_cli import DetectSerialCli
from cli.easy import EasyCli
from cli.ehz import EhzCli
from cli.mt175cli import Mt175Cli
from cli.mt681cli import Mt681Cli


# pylint: disable=too-few-public-methods
class Cli:
    """
    available modules
    """
    detect = DetectSerialCli
    mt175 = Mt175Cli
    mt681 = Mt681Cli
    dd3sml = Dd3CliSML
    dd3sml2way = Dd3CliSML2Way
    dd3odt = Dd3CliODT
    dd3odt2way = Dd3CliODT2Way
    ehz = EhzCli
    easy = EasyCli
