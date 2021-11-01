#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import json
import argparse

def get_args():
    """
    Get args from CLI
    :return: argparse object
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input','-i',
        action='store',
        dest='input_filepath',
        type=str,
        help='path/to/vt_decompose_report.txt'
    )
    parser.add_argument(
        '--output','-o',
        action='store',
        dest='output_filepath',
        type=str,
        help='path/to/vt_decompose_report.json'
    )

    return parser.parse_args()


def parse_vt_decompose_report(report_filepath: str) -> dict:
    """
    <PENDING>
    """

    # Regex
    version_re = re.compile('decompose (?P<version>\S+$)')
    input_re = re.compile('input VCF file\s+(?P<ifile>\S+)')
    output_re = re.compile('.+output VCF file\s+(?P<ofile>\S+)')
    sdec_re = re.compile('smart decomposition\s+(?P<sdec>\S+ \S+)')
    nvar_re = re.compile('no. variants\s+: (?P<nvar>\d+)')
    nbia_re = re.compile('no. biallelic variants\s+: (?P<nbia>\d+)')
    nmul_re = re.compile('no. multiallelic variants\s+: (?P<nmul>\d+)')
    nadd_re = re.compile('no. additional biallelics\s+: (?P<nadd>\d+)')
    tbv_re = re.compile('total no. of biallelics\s+: (?P<tbv>\d+)')
    time_re = re.compile('Time elapsed: (?P<time>\d\S+)')

    # Report data structure
    report = {
        'version': None,
        'options': {},
        'stats': {},
        'time_elapsed': None,
    }

    options = report['options']
    stats = report['stats']

    with open(report_filepath, 'r') as fh:
        for line in fh:
            line = line.lstrip(' ')
            if line.startswith('decompose'):
                capture_value = version_re.search(line).groupdict()["version"]
                report['version'] = f"vt_decompose_{capture_value}"

            elif line.startswith('options'):
                capture_value = input_re.search(line).groupdict()['ifile']
                report['options']['input_vcf'] = capture_value

            elif line.startswith('[o] output VCF'):
                capture_value = output_re.search(line).groupdict()['ofile']
                report['options']['output_vcf'] = capture_value

            elif line.startswith('[s] smart decomposition'):
                capture_value = sdec_re.search(line).groupdict()['sdec']
                report['options']['smart_decomposition'] = capture_value

            elif line.startswith('stats'):
                capture_value = nvar_re.search(line).groupdict()['nvar']
                report['stats']['n_variants'] = int(capture_value)

            elif line.startswith('no. biallelic variants'):
                capture_value = nbia_re.search(line).groupdict()['nbia']
                report['stats']['n_biallelic_variants'] = int(capture_value)

            elif line.startswith('no. multiallelic variants'):
                capture_value = nmul_re.search(line).groupdict()['nmul']
                report['stats']['n_multiallelic_variants'] = int(capture_value)

            elif line.startswith('no. additional biallelics'):
                capture_value = nadd_re.search(line).groupdict()['nadd']
                report['stats']['n_additional_biallelic_variants'] = int(capture_value)

            elif line.startswith('total no. of biallelics'):
                capture_value = tbv_re.search(line).groupdict()['tbv']
                report['stats']['total_biallelic_variants'] = int(capture_value)

            elif line.startswith('Time elapsed'):
                capture_value = time_re.search(line).groupdict()['time']
                report['time_elapsed'] = capture_value

    return report

def export_json(data: dict, output_filepath: str) -> None:
    """
    <PENDING>
    """
    with open(output_filepath,"w") as fh:
        fh.write(json.dumps(data, indent=4))

def main():
    """
    <PENDING>
    """

    # Parse arguments from CLI
    args = get_args()
    # Parse report
    report_data = parse_vt_decompose_report(report_filepath=args.input_filepath)
    # Export report
    export_json(data=report_data, output_filepath=args.output_filepath)

if __name__ == '__main__':
    main()
