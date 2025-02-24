import json
import sys
import logging
from sandbox import Sandbox
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            command = 'lxc list --fast --format json'
            logging.info(f'Executing command: {command}')
            Loader.SANDBOXES_DICT = json.loads(subprocess.getoutput(command))
        except ValueError as e:
            logging.error('sbxr json is borked again!')
            sys.exit(e)

    def ParseJsonToObjects(self):
        Sandbox.ListOfSandboxes.clear()
        for sandbox in Loader.SANDBOXES_DICT:
            logging.info(f'Appending sandbox: {sandbox["name"]} with status: {sandbox["status"]}')
            Sandbox.ListOfSandboxes.append(Sandbox(sandbox['name'], sandbox['status']))
