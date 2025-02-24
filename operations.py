import subprocess
import logging
from sandbox import Sandbox

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Operations(Sandbox):

    def toggle_sandbox(self, sbx):
        if sbx.status:
            Operations.stop_sandbox(self, sbx)
        else:
            Operations.start_sandbox(self, sbx)

    def stop_all_sandboxes(self):
        for sandbox in Sandbox.ListOfSandboxes:
            if sandbox.status:
                Operations.stop_sandbox(self, sandbox)

    def stop_sandbox(self, sbx):
        command = 'sbxr halt ' + sbx.name
        logging.info(f'Executing command: {command}')
        error = subprocess.getoutput(command)
        if error:
            logging.error(f'Result of stop command: {error}')
        else:
            logging.info(f'Successfully stopped sandbox: {sbx.name}')

    def start_sandbox(self, sbx):
        command = 'sbxr start ' + sbx.name
        logging.info(f'Executing command: {command}')
        error = subprocess.getoutput(command)
        logging.info(f'Result of start command: {error}')
