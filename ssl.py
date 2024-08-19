import argparse

parser = argparse.ArgumentParser(
                    prog='dotmastr',
                    description='A dotfiles manager which uses git to manage dotfiles.')
parser.add_argument('--remove', help="Remove the repo from existence! (DANGEROUS!). " + "\n" + "Answer with 'true' to continue")
args = parser.parse_args()

if args.remove == "true":
    print("sssss")