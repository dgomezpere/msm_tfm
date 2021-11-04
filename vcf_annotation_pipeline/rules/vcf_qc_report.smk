#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from scripts.vt_report_parser import vt_report_parser
#from ..scripts.vt_report_parser import vt_report_parser

rule vt_reports_to_json:
    input:
        vt_decompose_report = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'],
            report_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.vt_decompose_report')).name,
        ),
        vt_normalize_report = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'],
            report_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.vt_normalize_report')).name,
        ),
    output:
        vt_decompose_report_json = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'],
            report_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.vt_decompose_report.json')).name,
        ),
        vt_normalize_report_json = '{report_dirpath}/{report_filename}'.format(
            report_dirpath = config['workdir_tree']['qc_data_dirpath'],
            report_filename = Path(config['input_vcf'].replace(''.join(Path(config['input_vcf']).suffixes), '.vt_normalize_report.json')).name,
        ),
    run:
        # Parse vt decompose
        vt_report_parser(input_filepath=input.vt_decompose_report, output_filepath=output.vt_decompose_report_json)
        # Parse vt normalize
        vt_report_parser(input_filepath=input.vt_normalize_report, output_filepath=output.vt_normalize_report_json)
