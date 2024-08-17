import argparse
from scanner.scanner import Scanner
from scanner.utils import help

def parse_args():
    parser = argparse.ArgumentParser(description='Scanner')
    parser.add_argument('--domain', type=str, required=True, help='Domain name')
    return parser.parse_args()

def main():
    args = parse_args()
    domain = args.domain

    if domain:
        scanner = Scanner(domain)
        scanner.start_scan()
    else:
        help()

if __name__ == "__main__":
    main()
