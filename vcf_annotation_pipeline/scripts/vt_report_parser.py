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
    output_re = re.compile('output VCF file\s+(?P<ofile>\S+)')
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

def parse_vt_normalize_report(report_filepath: str) -> dict:
    """
    <PENDING>
    """

    # Regex
    version_re = re.compile('normalize (?P<version>\S+$)')
    input_re = re.compile('input VCF file\s+(?P<ifile>\S+)')
    output_re = re.compile('output VCF file\s+(?P<ofile>\S+)')
    sws_re = re.compile('sorting window size\s+(?P<sws>\d+)')
    nfmri_re = re.compile('no fail on masked reference inconsistency\s+(?P<nfmri>\S+)')
    nfri_re = re.compile('no fail on reference inconsistency\s+(?P<nfri>\S+)')
    quiet_re = re.compile('quiet\s+(?P<quiet>\S+)')
    debug_re = re.compile('debug\s+(?P<debug>\S+)')
    rFf_re = re.compile('reference FASTA file\s+(?P<rFf>/\S+)')
    nlt_re = re.compile('no. left trimmed\s+: (?P<nlt>\d+)')
    nrt_re = re.compile('no. right trimmed\s+: (?P<nrt>\d+)')
    nlrt_re = re.compile('no. left and right trimmed\s+: (?P<nlrt>\d+)')
    nrtla_re = re.compile('no. right trimmed and left aligned\s+: (?P<nrtla>\d+)')
    nla_re = re.compile('no. left aligned\s+: (?P<nla>\d+)')
    tnbn_re = re.compile('total no. biallelic normalized\s+: (?P<tnbn>\d+)')
    tnmn_re = re.compile('total no. multiallelic normalized\s+: (?P<tnmn>\d+)')
    tnvn_re = re.compile('total no. variants normalized\s+: (?P<tnvn>\d+)')
    tnvn_ro = re.compile('total no. variants observed\s+: (?P<tnvo>\d+)')
    tnrn_ro = re.compile('total no. reference observed\s+: (?P<tnro>\d+)')
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
            if line.startswith('normalize'):
                capture_value = version_re.search(line).groupdict()["version"]
                report['version'] = f"vt_normalize_{capture_value}"

            elif line.startswith('options'):
                capture_value = input_re.search(line).groupdict()['ifile']
                report['options']['input_vcf'] = capture_value

            elif line.startswith('[o] output VCF'):
                capture_value = output_re.search(line).groupdict()['ofile']
                report['options']['output_vcf'] = capture_value

            elif line.startswith('[w] sorting window size'):
                capture_value = sws_re.search(line).groupdict()['sws']
                report['options']['sorting_window_size'] = capture_value

            elif line.startswith('[m] no fail on masked reference inconsistency'):
                capture_value = nfmri_re.search(line).groupdict()['nfmri']
                report['options']['no_fail_on_masked_reference_inconsistency'] = capture_value

            elif line.startswith('[n] no fail on reference inconsistency'):
                capture_value = nfri_re.search(line).groupdict()['nfri']
                report['options']['no_fail_on_reference_inconsistency'] = capture_value

            elif line.startswith('[q] quiet'):
                capture_value = quiet_re.search(line).groupdict()['quiet']
                report['options']['quiet'] = capture_value

            elif line.startswith('[d] debug'):
                capture_value = debug_re.search(line).groupdict()['debug']
                report['options']['debug'] = capture_value

            elif line.startswith('[r] reference FASTA file'):
                capture_value = rFf_re.search(line).groupdict()['rFf']
                report['options']['rFf'] = capture_value

            elif line.startswith('no. left trimmed'):
                capture_value = nlt_re.search(line).groupdict()['nlt']
                if stats['n_biallelic_left_trimmed']:
                    report['stats']['n_multiallelic_left_trimmed'] = int(capture_value)
                else:
                    report['stats']['n_biallelic_left_trimmed'] = int(capture_value)

            elif line.startswith('no. right trimmed'):
                capture_value = nrt_re.search(line).groupdict()['nrt']
                if stats['n_biallelic_right_trimmed']:
                    report['stats']['n_multiallelic_right_trimmed'] = int(capture_value)
                else:
                    report['stats']['n_biallelic_right_trimmed'] = int(capture_value)

            elif line.startswith('no. left and right trimmed'):
                capture_value = nlrt_re.search(line).groupdict()['nlrt']
                if stats['n_biallelic_left_right_trimmed']:
                    report['stats']['n_multiallelic_left_right_trimmed'] = int(capture_value)
                else:
                    report['stats']['n_biallelic_left_right_trimmed'] = int(capture_value)

            elif line.startswith('no. right trimmed and left aligned'):
                capture_value = nrtla_re.search(line).groupdict()['nrtla']
                if stats['n_biallelic_left_right_aligned']:
                    report['stats']['n_multiallelic_left_right_aligned'] = int(capture_value)
                else:
                    report['stats']['n_biallelic_left_right_aligned'] = int(capture_value)

            elif line.startswith('no. left aligned'):
                capture_value = nla_re.search(line).groupdict()['nla']
                if stats['n_biallelic_left_aligned']:
                    report['stats']['n_multiallelic_left_aligned'] = int(capture_value)
                else:
                    report['stats']['n_biallelic_left_aligned'] = int(capture_value)

            elif line.startswith('total no. biallelic normalized'):
                capture_value = tnbn_re.search(line).groupdict()['tnbn']
                report['stats']['n_variants'] = int(capture_value)

            elif line.startswith('total no. multiallelic normalized'):
                capture_value = tnmn_re.search(line).groupdict()['tnmn']
                report['stats']['n_variants'] = int(capture_value)

            elif line.startswith('total no. variants normalized'):
                capture_value = tnvn_re.search(line).groupdict()['tnvn']
                report['stats']['n_variants'] = int(capture_value)

            elif line.startswith('total no. variants observed'):
                capture_value = nvo_re.search(line).groupdict()['nvo']
                report['stats']['n_variants'] = int(capture_value)

            elif line.startswith('total no. reference observed'):
                capture_value = tnro_re.search(line).groupdict()['tnro']
                report['stats']['n_variants'] = int(capture_value)

            elif line.startswith('Time elapsed'):
                capture_value = time_re.search(line).groupdict()['time']
                report['time_elapsed'] = capture_value

    return report

def get_report_type(report_filepath: str):
    """
    normalize
    decompose
    """

    with open(report_filepath, 'r') as fh:
        report_type = fh.readline().split( )[0]
    return report_type

# Dispatcher

def parse_vt_report(input_filepath: str) -> dict:

    """
    """

    parser_dispatcher = {
        'decompose': parse_vt_decompose_report(input_filepath),
        'normalize': parse_vt_normalize_report(input_filepath)
    }

    report_type = get_report_type(input_filepath)

    return parser_dispatcher[report_type]

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
    # # Parse arguments from CLI
    args = get_args()
    args.input_filepath = "vt_decompose_report.txt"
    args.output_filepath = "vt_decompose_report.json"
    print(args.input_filepath)
    print(args.output_filepath)
    # Parse report
    report_data = parse_vt_report(input_filepath=args.input_filepath)
    # Export report
    export_json(data=report_data, output_filepath=args.output_filepath)

if __name__ == '__main__':
    main()
