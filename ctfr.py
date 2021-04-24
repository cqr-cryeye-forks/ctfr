#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
from typing import NoReturn

import requests
import urllib3

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help='Target domain.')
    parser.add_argument('-o', '--output', type=str, help='Output file.', default='output.json')
    parser.add_argument('-v', '--verbose', type=bool, help='Verbose print.', default=False)
    return parser.parse_args()


def clear_url(target: str) -> str:
    return target.replace('www.', '', 1) if target.startswith('www.') else target


def save_subdomains(subdomains: list, output_file: str) -> NoReturn:
    with open(output_file, 'w') as f:
        json.dump(subdomains, f, indent=2)


def main():
    print('Start!')
    args = parse_args()
    target = clear_url(target=args.domain)
    output = args.output
    subdomains = []
    resp = requests.get(f'https://crt.sh/?q=%.{target}&output=json', headers=headers, verify=False)
    if args.verbose:
        print(resp.status_code, resp.content.decode("UTF-8"))
    if resp.status_code == 200:
        subdomains = sorted(set([item['name_value'] for item in resp.json()]))
    save_subdomains(subdomains=subdomains, output_file=output)
    print("Done. Have a nice day! ;).")


if __name__ == '__main__':
    main()
