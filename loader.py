import json
import sys

from sandbox import Sandbox
import subprocess


def is_tool(name):
    # TODO
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None


class Loader:
    SANDBOXES_DICT = []

    def __init__(self):
        self.GetJsonFromSandboxer()
        self.ParseJsonToObjects()

    def GetJsonFromSandboxer(self):
        try:
            Loader.SANDBOXES_DICT = json.loads(subprocess.getoutput('sbxr list --format json'))
        except ValueError as e:
            print('sbxr json is fucked again!')
            sys.exit(e)

    def ParseJsonToObjects(self):
        Sandbox.ListOfSandboxes.clear()
        for sandbox in Loader.SANDBOXES_DICT:
            Sandbox.ListOfSandboxes.append(Sandbox(sandbox['Name'], sandbox['Status']))
