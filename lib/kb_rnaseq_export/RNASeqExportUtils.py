import os
import shutil
import re

from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils


def log(message):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(message)


class RNASeqExportUtils:
    STAGING_FILE_PREFIX = '/staging/'

    def __init__(self, ctx, config):
        log('--->\nInitializing RNASeqDownloaderUtils instance:\n config: %s' % config)
        self.scratch = config['scratch']
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.ctx = ctx
        self.staging_base = os.path.join(self.STAGING_FILE_PREFIX, ctx['user_id'])

        self.rau = ReadsAlignmentUtils(self.callback_url, token=self.token)


    def download_RNASeq_Alignment_BAM(self, params):
        """
        download_RNASeq: download RNASeq Alignment/Expression/DifferentialExpression zip file

        params:
        input_ref: RNASeq object reference ID
        rna_seq_type: 'RNASeqAlignment'
        download_file_type: one of 'bam', 'sam' or 'bai'

        return:
        shock_id: Shock ID of stored zip file

        """
        log('--->\nrunning RNASeqDownloaderUtils.download_RNASeq_Alignment:\nparams: %s' % params)

        # Validate params
        self.validate_download_rna_seq_alignment_parameters(params)

        input_ref = params.get('input_ref')
        returnVal = dict()

        tmp_dir = self.rau.download_alignment({'source_ref': input_ref,
                                               'downloadBAI': True})['destination_dir']
        files = os.listdir(tmp_dir)
        destination_dir = os.path.join(self.staging_base, params['destination_dir'])
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)

        for fn in files:
            print self.staging_base
            shutil.move(os.path.join(tmp_dir, fn), destination_dir)

        returnVal['path'] = destination_dir
        return returnVal

    def download_RNASeq_Alignment_SAM(self, params):
        """
        download_RNASeq: download RNASeq Alignment/Expression/DifferentialExpression zip file

        params:
        input_ref: RNASeq object reference ID
        rna_seq_type: 'RNASeqAlignment'

        return:

        """
        log('--->\nrunning RNASeqDownloaderUtils.download_RNASeq_Alignment:\nparams: %s' % params)
        destination_dir = self.rau.download_alignment({'source_ref': input_ref,
                                                       'downloadSAM': True,
                                                       'downloadBAI': True})['destination_dir']
        files = os.listdir(destination_dir)
        bam_files = [x for x in files if re.match('.*\.bam', x)]
        for bam_file in bam_files:
            log('removing file: {}'.format(bam_file))
            os.remove(os.path.join(destination_dir, bam_file))
        files = os.listdir(destination_dir)
        for fn in files:
            shutil.move(os.path.join(destination_dir, fn),
                        params['destination_dir'])
        return {'path': params['destination_dir']}

    def validate_download_rna_seq_alignment_parameters(self, params):
        """
        validate_download_rna_seq_alignment_parameters:
                        validates params passed to download_rna_seq_alignment method

        """

        # check required parameters
        for p in ['input_ref', 'destination_dir']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

        # check supportive RNASeq types
        valid_rnaseq_types = ['RNASeqAlignment',
                              'RNASeqExpression',
                              'RNASeqDifferentialExpression']
        if params['rna_seq_type'] not in valid_rnaseq_types:
            raise ValueError('Unexpected RNASeq type: %s' % params['rna_seq_type'])
