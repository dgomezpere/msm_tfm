#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import vcfpy
import pandas as pd
import gzip
from collections import OrderedDict

class RecordAnnotation:
    def __init__(self, annotation, header):
        """
        """
        self._annotation = []
        self._header =[]
        self._record_annotation = {}

        if annotation and header:
            self._annotation = annotation
            self._header = header
            self._record_annotation = OrderedDict(zip(self._header, self._annotation))

    #Getters and setters
    @property
    def record_annotation(self):
        """
        """
        return self._record_annotation

class RecordAnnotations:
    def __init__(self, filepath=None):
        """
        """
        # Initialize all properties to None
        self._vcf_filepath = None
        self._vcf_file = None
        self._annotation_header = []
        self._annotations = []

        # Populate RecordAnnotations from VCF vcf_filepath
        if filepath:
            self._vcf_filepath = filepath
            self._load_vcf_file_from_vcf_filepath(self._vcf_filepath)
            self._load_annotation_header_from_vcf_filepath(self._vcf_file)
            self._populate_object()

    # Private methods
    def _load_vcf_file_from_vcf_filepath(self, filepath: str):
        """
        """
        self._vcf_file = vcfpy.Reader.from_path(filepath)

    def _load_annotation_header_from_vcf_filepath(self, vcf_file: vcfpy.reader.Reader):
        """
        """
        for line in vcf_file.header.lines:
            if type(line) == vcfpy.InfoHeaderLine and line.id == "CSQ":
                self._annotation_header = line.description.split(": ")[1].split("|")

    def _populate_object(self):
        """
        """
        for record in self._vcf_file:
            self._annotations.append(RecordAnnotation(annotation=record.INFO["CSQ"][0].split("|"), header=self._annotation_header))

    #Getters and setters
    @property
    def annotations(self):
        """
        """
        return self._annotations

    @property
    def annotation_fields(self):
        """
        """
        return self._annotation_header

def main():
    vcf_filepath = "/Users/segarmond/Documents/Science/Bioinfo/TFM/old_msm_tfm/msm_tfm-main/test_data/20200908_GISTomics_chr22_variants.decomp.norm.annot.vcf.gz"
    vcf_anotation = RecordAnnotations(vcf_filepath)
    print(vcf_anotation.annotation_fields)
    print(vcf_anotation.annotations[1].record_annotation['Allele'])

if __name__ == '__main__':
    main()

































        # Initialize all properties to None
    #     self._allele = None
    #     self._consequence = None
    #     self._impact = None
    #     self._symbol = None
    #     self._gene = None
    #     self._feature_type = None
    #     self._feature = None
    #     self._biotype = None
    #     self._exon = None
    #     self._intron = None
    #     self._hgvsc = None
    #     self._hgvsp = None
    #     self._cdna_position = None
    #     self._cds_position = None
    #     self._protein_position = None
    #     self._amino_acids = None
    #     self._codons = None
    #     self._existing_variation = None
    #     self._distance = None
    #     self._strand = None
    #     self._flags = None
    #     self._symbol_source = None
    #     self._hgnc_id = None
    #     self._canonical = None
    #     self._mane_select = None
    #     self._mane_plus_clinical = None
    #     self._ccds = None
    #     self._ensp = None
    #     self._refseq_match = None
    #     self._source = None
    #     self._refseq_offset = None
    #     self._given_ref = None
    #     self._used_ref = None
    #     self._bam_edit = None
    #     self._domains = None
    #     self._hgvs_offset = None
    #     self._hgvsg = None
    #     self._clin_sig = None
    #     self._somatic = None
    #     self._pheno = None
    #
    #
    #
    #
    # # def _populate_objects(self):
    # #     """
    # #     """
    # #
    # #             self._get_record_allele()
    # #             self._get_record_consequence()
    # #             self._get_record_impact()
    # #             self._get_record_symbol()
    # #             self._get_record_gene()
    # #             self._get_record_feature_type()
    # #             self._get_record_feature()
    # #             self._get_record_biotype()
    # #             self._get_record_exon()
    # #             self._get_record_intron()
    # #             self._get_record_hgvsc()
    # #             self._get_record_hgvsp()
    # #             self._get_record_cdna_position()
    # #             self._get_record_cds_position()
    # #             self._get_record_protein_position()
    # #             self._get_record_amino_acids()
    # #             self._get_record_codons()
    # #             self._get_record_existing_variation()
    # #             self._get_record_distance()
    #             self._get_record_strand()
    #             self._get_record_flags()
    #             self._get_record_symbol_source()
    #             self._get_record_hgnc_id()
    #             self._get_record_canonical()
    #             self._get_record_mane_select()
    #             self._get_record_mane_plus_clinical()
    #             self._get_record_ccds()
    #             self._get_record_ensp()
    #             self._get_record_refseq_match()
    #             self._get_record_source()
    #             self._get_record_refseq_offset()
    #             self._get_record_given_ref()
    #             self._get_record_used_ref()
    #             self._get_record_bam_edit()
    #             self._get_record_domains()
    #             self._get_record_hgvs_offset()
    #             self._get_record_hgvsg()
    #             self._get_record_clin_sig()
    #             self._get_record_somatic()
    #             self._get_record_pheno()
