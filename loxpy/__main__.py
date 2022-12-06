import sys, argparse

from .lox import Lox

def get_args():
    parser = argparse.ArgumentParser(description='loxPy')
    parser.add_argument('script', type=str, nargs='?', help='Script filename')
    return parser.parse_args()

def main():
    args = get_args()

    lox = Lox()
    if args.script:
        lox.run_file(args.script)
    else:
        lox.run_prompt()
    
    return lox.error_code()

if __name__=="__main__":
    sys.exit(main())

