#!/usr/bin/env python3
import argparse
import json
import itertools
from typing import NoReturn

import requests
import urllib3

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help='Target domain.')
    parser.add_argument('-o', '--output', type=str, help='Output file.', default='output.json')
    return parser.parse_args()


def clear_url(target: str) -> str:
    target = target.strip()
    return target.replace('www.', '', 1) if target.startswith('www.') else target


def clear_subdomains(subdomains: dict) -> list:
    sd = [item['name_value'].split('\n') for item in subdomains]
    return sorted(set(itertools.chain.from_iterable(sd)))


def save_subdomains(subdomains: list, output_file: str) -> NoReturn:
    with open(output_file, 'w') as f:
        json.dump(subdomains, f, indent=2)


def main():
    print('Start!')
    args = parse_args()
    target = clear_url(target=args.domain).strip()
    print(target)
    output = args.output
    resp = requests.get(f'https://crt.sh/?q={target}&output=json', headers=headers, verify=False)
    print(resp.status_code)
    subdomains = clear_subdomains(subdomains=resp.json()) if resp.status_code == 200 else []
    [print(s) for s in subdomains]
    save_subdomains(subdomains=subdomains, output_file=output)
    print("Done. Have a nice day! ;).")


if __name__ == '__main__':
    main()
