#!/usr/bin/env python3

from paramiko import SSHClient
from scp import SCPClient, SCPException
from contextlib import contextmanager
import ntpath
import random
import string
import sys
import os

# Use example:
# ./sign_tool.py --avsign --username <user> --password <password> -- /var/tmp/test_file
# ./sign_tool.py --help
# ./sign_tool.py --version

# Credentials
user = "george.vlad"
host = "1.2.3.4"

# Variables
arguments = " ".join(sys.argv[1:-1])
file_to_sign = os.path.abspath(sys.argv[-1])
local_file_dir = ntpath.dirname(file_to_sign)
server_temp_dir = "/tmp/" + "signedfile_" + \
                  ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
server_file_path = os.path.join(server_temp_dir, ntpath.basename(file_to_sign))


def run_command (cmd, ssh):
    """Run cli comamands on remote machine."""
    _, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    logs = stdout.read()
    for output_line in logs.splitlines():
        print(output_line.decode("utf-8", errors="replace"))
    error_msg = stderr.read()
    if error_msg:
        for output_line in error_msg.splitlines():
            print(output_line.decode("utf-8", errors="replace"))
        if "signing-client" not in cmd:
            return False
    return logs


def upload_file(ssh, file, destination):
    """Upload a single file to a remote directory."""
    scp = SCPClient(ssh.get_transport())
    try:
        scp.put(file, recursive=True, remote_path=destination)
    except SCPException as error:
        print(error)
        return False
    print(f"\nFile '{file}' was successfully uploaded on target machine\n")
    scp.close()
    return True


def download_files(ssh, source, destination):
    """Download signed files from remote directory to local dir"""
    scp = SCPClient(ssh.get_transport())
    sftp = ssh.open_sftp()
    files = sftp.listdir(source)
    for file in files:
        print(f"Downloading file '{file}' to {destination}/{file}")
        try:
            scp.get(os.path.join(source, file), destination)
        except SCPException as error:
            print(error)
            return False
    sftp.close()
    scp.close()
    return True


@contextmanager
def ssh_connection(hostname, username):
    ssh = SSHClient()
    try:
        #  Initialization
        ssh.load_system_host_keys()
        ssh.connect(hostname=hostname, username=username, password=None, timeout=10)

        # Create temporary directory
        run_command(f"mkdir {server_temp_dir}", ssh)

        yield ssh

    finally:
        # Cleanup (delete the file from multi-server)
        print("Cleaning up...")
        run_command(f"rm -rf {server_temp_dir}", ssh)
        ssh.close()


if __name__ == '__main__':

    rc = 1

    with ssh_connection(hostname=host, username=user) as ssh:

        # Check arguments
        if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "--version":
            run_command(f"signing-client {sys.argv[1]}", ssh)
            rc = 0

            # Send file to be signed
        if rc:
            rc = upload_file(ssh, file_to_sign, server_temp_dir)

            # Sign File
        if rc:
            logs = run_command(f"signing-client {arguments} {server_file_path}", ssh)

            if f"signed {server_file_path}" in logs.decode("utf-8", errors="replace"):
                # Download signed file(s) to local temp dir
                download_files(ssh, server_temp_dir, local_file_dir)
            else:
                print("ERROR! File not signed!")
                rc = 0

    exit(not rc)
