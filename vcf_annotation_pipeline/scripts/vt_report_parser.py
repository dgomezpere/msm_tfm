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
    Example:
    // START //
    decompose v0.5

    options:     input VCF file        /opt/msm_tfm/test_data/20200908_GISTomics_chr22_variants.vcf.gz
             [s] smart decomposition   true (experimental)
             [o] output VCF file       -


    stats: no. variants                 : 17639
           no. biallelic variants       : 17639
           no. multiallelic variants    : 0

           no. additional biallelics    : 0
           total no. of biallelics      : 17639

    Time elapsed: 0.77s
    // END //
    """

    # Regex
    value_re = re.compile('(?P<value>(true\s){0,1}\S+)$')

    # Report data structure
    report = {
        'version': None,
        'options': {},
        'stats': {},
        'time_elapsed': None,
    }

    with open(report_filepath, 'r') as fh:
        for line in fh:
            line = line.lstrip() # Default stripping by whitespaces

            if not line: # Line is empty
                continue

            value = value_re.search(line).groupdict()['value']

            # Parsing version
            if line.startswith('decompose'):
                report['version'] = f"vt_decompose_{value}"

            # Parsing options
            elif line.startswith('options'):
                report['options']['input_vcf'] = value

            elif line.startswith('[o]'):
                report['options']['output_vcf'] = value

            elif line.startswith('[s]'):
                report['options']['smart_decomposition'] = value

            # Parsing stats
            elif line.startswith('stats'):
                report['stats']['n_variants'] = int(value)

            elif line.startswith('no. biallelic variants'):
                report['stats']['n_biallelic_variants'] = int(value)

            elif line.startswith('no. multiallelic variants'):
                report['stats']['n_multiallelic_variants'] = int(value)

            elif line.startswith('no. additional biallelics'):
                report['stats']['n_additional_biallelic_variants'] = int(value)

            elif line.startswith('total no. of biallelics'):
                report['stats']['total_biallelic_variants'] = int(value)

            # Parsing time elapsed
            elif line.startswith('Time elapsed'):
                report['time_elapsed'] = value

    return report

def parse_vt_normalize_report(report_filepath: str) -> dict:
    """
    <PENDING>
    Example:
    // START //
    normalize v0.5

    options:     input VCF file                                  vcf/20200908_GISTomics_chr22_variants.decomp.vcf.gz
             [o] output VCF file                                 -
             [w] sorting window size                             100000
             [m] no fail on masked reference inconsistency       false
             [n] no fail on reference inconsistency              true
             [q] quiet                                           false
             [d] debug                                           false
             [r] reference FASTA file                            /opt/msm_tfm/references/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fa


    stats: biallelic
              no. left trimmed                      : 0
              no. right trimmed                     : 0
              no. left and right trimmed            : 0
              no. right trimmed and left aligned    : 0
              no. left aligned                      : 0

           total no. biallelic normalized           : 0

           multiallelic
              no. left trimmed                      : 0
              no. right trimmed                     : 0
              no. left and right trimmed            : 0
              no. right trimmed and left aligned    : 0
              no. left aligned                      : 0

           total no. multiallelic normalized        : 0

           total no. variants normalized            : 0
           total no. variants observed              : 17639
           total no. reference observed             : 0

    Time elapsed: 0.93s
    // END //
    """

    # Regex
    value_re = re.compile('(?P<value>\S+)$')

    # Report data structure
    report = {
        'version': None,
        'options': {},
        'stats': {},
        'time_elapsed': None,
    }

    stats_section = None

    with open(report_filepath, 'r') as fh:
        for line in fh:
            line = line.lstrip() # Default stripping by whitespaces

            if not line: # Line is empty
                continue

            value = value_re.search(line).groupdict()['value']

            # Parsing version
            if line.startswith('normalize'):
                report['version'] = f"vt_normalize_{value}"

            #Parsing options
            elif line.startswith('options'):
                report['options']['input_vcf'] = value

            elif line.startswith('[o]'):
                report['options']['output_vcf'] = value

            elif line.startswith('[w]'):
                report['options']['sorting_window_size'] = value

            elif line.startswith('[m]'):
                report['options']['no_fail_on_masked_reference_inconsistency'] = value

            elif line.startswith('[n]'):
                report['options']['no_fail_on_reference_inconsistency'] = value

            elif line.startswith('[q]'):
                report['options']['quiet'] = value

            elif line.startswith('[d]'):
                report['options']['debug'] = value

            elif line.startswith('[r]'):
                report['options']['reference'] = value

            # Parsing stats
            # Assign stats section ['biallelic', 'multiallelic']
            elif line in ['stats: biallelic', 'multiallelic']:
                stats_section = line.replace('stats: ','')

            # Parse 'no.*' lines
            elif line.startswith('no. left trimmed'):
                report['stats'][f"n_{stats_section}_left_trimmed"] = int(value)

            elif line.startswith('no. right trimmed'):
                report['stats'][f"n_{stats_section}_right_trimmed"] = int(value)

            elif line.startswith('no. left and right trimmed'):
                report['stats'][f"n_{stats_section}_left_right_trimmed"] = int(value)

            elif line.startswith('no. right trimmed and left aligned'):
                report['stats'][f"n_{stats_section}_right_trimmed_left_aligned"] = int(value)

            elif line.startswith('no. left aligned'):
                report['stats'][f"n_{stats_section}_left_aligned"] = int(value)

            # Parse 'total no.*' lines
            elif line.startswith('total no. biallelic normalized'):
                report['stats']['n_biallelic_normalized'] = int(value)

            elif line.startswith('total no. multiallelic normalized'):
                report['stats']['n_multiallelic_normalized'] = int(value)

            elif line.startswith('total no. variants normalized'):
                report['stats']['n_variants_normalized'] = int(value)

            elif line.startswith('total no. variants observed'):
                report['stats']['n_variants_observed'] = int(value)

            elif line.startswith('total no. reference observed'):
                report['stats']['n_reference_observed'] = int(value)

            # Parsing time elapsed
            elif line.startswith('Time elapsed'):
                report['time_elapsed'] = value

    return report

def get_report_type(report_filepath: str):
    """
    <PENDING>
    """

    with open(report_filepath, 'r') as fh:
        report_type = fh.readline().split( )[0]
    if report_type not in ['decompose','normalize']:
        raise ValueError(f"Report type '{report_type}' not supported")
    return report_type

def parse_vt_report(input_filepath: str) -> dict:
    """
    <PENDING>
    """

    parser_dispatcher = {
        'decompose': parse_vt_decompose_report,
        'normalize': parse_vt_normalize_report
    }

    report_type = get_report_type(input_filepath)
    result = parser_dispatcher[report_type](input_filepath)

    return result

def export_json(data: dict, output_filepath: str) -> None:
    """
    <PENDING>
    """

    with open(output_filepath,"w") as fh:
        fh.write(json.dumps(data, indent=4))

def vt_report_parser(input_filepath: str, output_filepath: str) -> None:
    """
    <PENDING>
    """

    # Parse report
    report_data = parse_vt_report(input_filepath=input_filepath)
    # Export report
    export_json(data=report_data, output_filepath=output_filepath)

def main():
    """
    <PENDING>
    """

    # Parse arguments from CLI
    args = get_args()
    # Parse and export report
    vt_report_parser(input_filepath=args.input_filepath, output_filepath=args.output_filepath)

if __name__ == '__main__':
    main()
