# DOTMASTR: A Dotfiles manager written for fun!
import argparse, os, shutil, configparser
from git import Repo
from time import sleep
from pathlib import Path
from colorama import Fore, Back, Style

prif = lambda x: print(Fore.BLUE + "==> " + x + Style.RESET_ALL)

config = configparser.ConfigParser()

parser = argparse.ArgumentParser(
                    prog='dotmastr',
                    description='A dotfiles manager which uses git to manage dotfiles.')
parser.add_argument('-f', '--folder', default="~/.config/dotmastr", help="The default folder dotmastr will use for storing the git repo and config.")
parser.add_argument('-c', '--config', default="~/.config/dotmastr/dotmastr.conf")
parser.add_argument('--remove', help="Remove the repo from existence! " + Fore.RED + "(DANGEROUS!)" + Style.RESET_ALL + " Answer with 'true' to continue")
subparsers = parser.add_subparsers(dest="command")

parser_add = subparsers.add_parser("add", help="Add a dotfile to the backup directory")
parser_add.add_argument("dotfile", help="The dotfile to add to the backup directory")

parser_remove = subparsers.add_parser("remove", help="Remove a dotfile and its parent directory if empty")
parser_remove.add_argument("dotfile", help="The dotfile to remove")

args = parser.parse_args()
mfolder = os.path.expanduser(args.folder)

if args.folder != "~/.config/dotmastr":
    mfolder = os.path.expanduser(args.folder)
else:
    try:
        config_path = Path(os.path.expanduser(args.folder)) / "dotmastr.conf"
        config.read(config_path)

        if "Main" in config:
            mfolder = config["Main"].get("DefaultFolder", os.path.expanduser(args.folder))
        else:
            mfolder = os.path.expanduser(args.folder)
    except Exception as e:
        print(f"Error reading config: {e}")
        config.read(Path.cwd() / "dotmastr.def.conf")
        mfolder = config["Main"]["DefaultFolder"]

if os.path.isdir(mfolder) != True:
    prif("Main directory not found! Generating a new one.")
    os.makedirs(mfolder)

if os.path.isdir(os.path.join(mfolder, "repo.git")) != True:
    rfolder = os.path.join(mfolder, "repo.git")
    repo = Repo.init(rfolder)
    
    # Set up the remote URL if provided
    if remote_url:
        repo.create_remote('origin', remote_url)
        prif(f"Remote URL set to: {remote_url}")

    prif("Repo Initiated at: " + rfolder)
    sleep(1)

if os.path.isfile(os.path.join(mfolder, "dotmastr.conf")) != True:
    shutil.copy(os.path.join(Path(__file__).resolve().parent, "dotmastr.def.conf"), os.path.join(mfolder, "dotmastr.conf"))

def add_dotfile(dotfile):
    rfolder = os.path.join(mfolder, "repo.git")
    dotfile_path = Path(dotfile)  # No need for expanduser
    relative_path = Path(dotfile).relative_to(Path.home())
    destination_path = os.path.join(rfolder, relative_path)

    if not dotfile_path.exists():
        prif(f"Error: {dotfile} does not exist.")
        return

    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    if dotfile_path.is_file():
        shutil.copy2(dotfile_path, destination_path)
        prif(f"Added file: {dotfile_path} to {destination_path}")
    elif dotfile_path.is_dir():
        shutil.copytree(dotfile_path, destination_path, dirs_exist_ok=True)
        prif(f"Added directory: {dotfile_path} to {destination_path}")

def remove_dotfile(dotfile):
    dotfile_path = Path(dotfile)
    rfolder = os.path.join(mfolder, "repo.git")

    # Compute the destination path relative to the repository root
    destination_path = os.path.join(rfolder, dotfile_path)

    if not os.path.exists(destination_path):
        prif(f"Error: {dotfile} does not exist in the repo.")
        return

    # Remove the file or directory
    if os.path.isfile(destination_path):
        os.remove(destination_path)
        prif(f"Removed file: {destination_path}")
    elif os.path.isdir(destination_path):
        shutil.rmtree(destination_path)
        prif(f"Removed directory: {destination_path}")

    # Remove empty parent directories
    parent_dir = os.path.dirname(destination_path)
    while parent_dir != rfolder:
        if not os.listdir(parent_dir):  # Check if directory is empty
            os.rmdir(parent_dir)
            prif(f"Removed empty directory: {parent_dir}")
            parent_dir = os.path.dirname(parent_dir)
        else:
            break


if args.command == "add":
    add_dotfile(args.dotfile)
elif args.command == "remove":
    remove_dotfile(args.dotfile)
elif args.remove == "true":
    rfolder = os.path.join(mfolder, "repo.git")
    shutil.rmtree(rfolder, ignore_errors=True)
else:
    parser.print_help()