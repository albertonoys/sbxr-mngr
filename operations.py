import subprocess
import sh
from sandbox import Sandbox


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
        error = subprocess.getoutput('sbxr halt ' + sbx.name)
        print(error)

    def start_sandbox(self, sbx):
        error = subprocess.getoutput('sbxr start ' + sbx.name)
        print(error)
