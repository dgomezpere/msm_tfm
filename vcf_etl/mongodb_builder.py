#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from pymongo import MongoClient
import pymongo
from header import VcfHeader
from record import VcfRecord
import vcfpy
import argparse

def get_args() -> argparse.ArgumentParser:
    """
    Get args from CLI
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--vcf','-i',
        action='store',
        dest='vcf_filepath',
        type=str,
        help='path/to/input.vcf(.gz)'
    )
    parser.add_argument(
        '--annotation_field','-af',
        action='store',
        dest='annotation_field',
        type=str,
        default='CSQ',
        help="VEP annotation record field ID in record INFO field (usually the string 'CSQ')"
    )
    parser.add_argument(
        '--annotation_sep','-as',
        action='store',
        dest='annotation_sep',
        type=str,
        default='|',
        help="Record VEP annotations separator (usually the char '|')"
    )
    parser.add_argument(
        '--db_name','-db',
        action='store',
        dest='db_name',
        type=str,
        help='The DB name to store the VCF data'
    )
    parser.add_argument(
        '--buffersize_records','-bs',
        action='store',
        dest='buffersize_records',
        type=int,
        help='The size of records buffer to process and load to the DB at once'
    )
    return parser.parse_args()

def create_db(db_name:str) -> pymongo.database.Database:
    """
    Initializes the mongo client, creates de MongoDB and returns the MongoDB
    """
    c = MongoClient()
    db = c[db_name]
    return db

def create_collections(db: pymongo.database.Database) -> dict:
    """
    Creates the collections required of the MongoDB
    """
    collections = {
        'vcf_header': db['vcf_header'],
        'vcf_contigs': db['vcf_contigs'],
        'vcf_samples': db['vcf_samples'],
        'vcf_record_fields': db['vcf_record_fields'],
        'vcf_record_fixed': db['vcf_record_fixed'],
        'vcf_record_info': db['vcf_record_info'],
        'vcf_record_calls': db['vcf_record_calls'],
        'vcf_record_annotations': db['vcf_record_annotations'],
    }
    return collections

def load_header_to_db(vcf_header_dict: dict, collections: dict) -> None:
    """
    Load the VcfHeader dict in the MongoDB collections
    """
    # Insert vcf header document
    wanted_header_keys = [
        'file_format',
        'file_date',
        'variant_caller',
        'reference',
    ]
    vcf_header_document = {key: vcf_header_dict[key] for key in wanted_header_keys}
    collections['vcf_header'].insert_one(vcf_header_document)
    # VCF header contigs collection
    collections['vcf_contigs'].insert_many(vcf_header_dict['contigs'])
    # VCF header record_fields collection
    collections['vcf_record_fields'].insert_many(vcf_header_dict['record_fields'])
    # VCF header samples collection
    collections['vcf_samples'].insert_many(vcf_header_dict['samples'])

def load_records_to_db(reader: vcfpy.Reader, collections: dict, record_fields: list, annotation_field: str, annotation_sep: str, annotation_keys: list, buffersize_records: int) -> None:
    """
    Load VcfRecord objects in the MongoDB collections
    """
    wanted_record_fixed_keys = [
        'id',
        'chrom',
        'pos',
        'start',
        'end',
        'ref',
        'alt',
        'type',
        'qual'
    ]

    # Load records data in the db
    vcf_record_fixed_documents = []
    vcf_record_info_documents = []
    vcf_record_calls_documents = []
    vcf_record_annotations_documents = []

    for i, record in enumerate(reader):
        # Get VCF record dict data
        vcf_record = VcfRecord(
            record=record,
            record_fields=record_fields,
            annotation_field=annotation_field,
            annotation_keys=annotation_keys,
            annotation_sep=annotation_sep
        )
        vcf_record_dict = vcf_record.to_dict()
        # Append documents to list of documents
        vcf_record_fixed_documents.append({key: vcf_record_dict[key] for key in wanted_record_fixed_keys})
        vcf_record_info_documents.append(vcf_record_dict['info'])
        vcf_record_calls_documents += vcf_record_dict['calls']
        vcf_record_annotations_documents += vcf_record_dict['annotations']
        if (i+1) % buffersize_records == 0:
            # Insert documents
            collections['vcf_record_fixed'].insert_many(vcf_record_fixed_documents)
            collections['vcf_record_info'].insert_many(vcf_record_info_documents)
            collections['vcf_record_calls'].insert_many(vcf_record_calls_documents)
            collections['vcf_record_annotations'].insert_many(vcf_record_annotations_documents)
            # Reset list of documents
            vcf_record_fixed_documents = []
            vcf_record_info_documents = []
            vcf_record_calls_documents = []
            vcf_record_annotations_documents = []

    if len(vcf_record_fixed_documents) != 0:
        collections['vcf_record_fixed'].insert_many(vcf_record_fixed_documents)
        collections['vcf_record_info'].insert_many(vcf_record_info_documents)
        collections['vcf_record_calls'].insert_many(vcf_record_calls_documents)
        collections['vcf_record_annotations'].insert_many(vcf_record_annotations_documents)

def main():
    """
    Running as a script
    """
    args = get_args()
    db = create_db(db_name=args.db_name)
    collections = create_collections(db=db)
    # Generate VCF header dict
    vcf_header = VcfHeader(filepath=args.vcf_filepath)
    vcf_header_dict = vcf_header.to_dict()
    # Load VCF header dict to the MongoDB
    load_header_to_db(vcf_header_dict=vcf_header_dict, collections=collections)
    # Load VCF record dicts to the MongoDB
    annotation_keys = vcf_header.get_annotation_keys(annotation_field=args.annotation_field)
    reader = vcfpy.Reader.from_path(args.vcf_filepath)
    load_records_to_db(
        reader=reader,
        collections=collections,
        record_fields=vcf_header.record_fields,
        annotation_field=args.annotation_field,
        annotation_sep=args.annotation_sep,
        annotation_keys=annotation_keys,
        buffersize_records=args.buffersize_records
    )

if __name__ == '__main__':
    main()
