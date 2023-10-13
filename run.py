#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import tempfile
import shutil
import urllib.request
import tarfile

VERSION = "1.21.1"
# GOROOT = os.path.expanduser("~/.go")
# GOPATH = os.path.expanduser("~/go")

# Get GOROOT and GOPATH from environment variables, if not set, use default values
GOROOT = os.environ.get("GOROOT", os.path.expanduser("~/.go"))
GOPATH = os.environ.get("GOPATH", os.path.expanduser("~/go"))
print(f"GOROOT: {GOROOT}")
print(f"GOPATH: {GOPATH}")

# using urllib.request to get the output
VERSION = urllib.request.urlopen("https://go.dev/VERSION?m=text").read().decode("utf-8").splitlines()[0].strip()

print(f"Go VERSION: {VERSION}")
# print(f"GOROOT: {GOROOT}")
# print(f"GOPATH: {GOPATH}")

OS = platform.system()
ARCH = platform.architecture()[0]

if OS == "Linux":
    if ARCH == "64bit":
        PLATFORM = "linux-amd64"
    elif ARCH == "32bit":
        PLATFORM = "linux-386"
    else:
        print("Unsupported architecture")
        sys.exit(1)
elif OS == "Darwin":
    PLATFORM = "darwin-amd64"
else:
    print("Unsupported operating system")
    sys.exit(1)

def print_help():
    print("Usage: python goinstall.py OPTIONS")
    print("\nOPTIONS:")
    print("  --remove\tRemove currently installed version")
    print("  --version\tSpecify a version number to install")

if len(sys.argv) > 1:
    if sys.argv[1] == "--remove":
        shutil.rmtree(GOROOT)
        print("Go removed.")
        sys.exit(0)
    elif sys.argv[1] == "--help":
        print_help()
        sys.exit(0)
    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        if len(sys.argv) < 3:
            print("Please provide a version number for: --version or -v")
            sys.exit(1)
        else:
            VERSION = f"go{sys.argv[2]}"
            # print(f"VERSION: {VERSION}")
            # sys.exit(0)
    else:
        print(f"Unrecognized option: {sys.argv[1]}")
        sys.exit(1)

# if os.path.exists(GOROOT):
#     print(f"The Go install directory ({GOROOT}) already exists. Exiting.")
#     sys.exit(1)

PACKAGE_NAME = f"{VERSION}.{PLATFORM}.tar.gz"
print(f"PACKAGE_NAME: {PACKAGE_NAME}")
TEMP_DIRECTORY = tempfile.mkdtemp()

# download link: https://go.dev/dl/go1.21.3.linux-amd64.tar.gz
print(f"Downloading {PACKAGE_NAME} ...")
# url = f"https://storage.googleapis.com/golang/{PACKAGE_NAME}"
url = f"https://go.dev/dl/{PACKAGE_NAME}"
urllib.request.urlretrieve(url, os.path.join(TEMP_DIRECTORY, "go.tar.gz"))

print("Extracting File...")
os.makedirs(GOROOT, mode=0o777, exist_ok=True)
# subprocess.run(["tar", "-C", GOROOT, "--strip-components=1", "-xf", os.path.join(TEMP_DIRECTORY, "go.tar.gz")])

try:
    # Extract the tar file to the specified directory and strip the components
    with tarfile.open(os.path.join(TEMP_DIRECTORY, "go.tar.gz"), 'r:gz') as tar:
        for member in tar.getmembers():
            member.path = os.path.join(GOROOT, os.path.relpath(member.path, 'go'))
            tar.extract(member)

    print(f'Tar file extracted successfully to {GOROOT}')

except tarfile.TarError as e:
    print(f'Error extracting tar file: {e}')

print(f"Go {VERSION} was installed into {GOROOT}.\n"
    f"Make sure to relogin into your shell or run:\n\n"
    f"\texport GOROOT={GOROOT}\n"
    f"\texport PATH=$GOROOT/bin:$PATH\n"
    f"\texport GOPATH={GOPATH}\n"
    f"\texport PATH=$GOPATH/bin:$PATH\n\n"
    f"to update your environment variables.")
print("Tip: Opening a new terminal window usually just works. :)")
shutil.rmtree(TEMP_DIRECTORY)
