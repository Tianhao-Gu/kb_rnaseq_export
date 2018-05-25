# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
from kb_rnaseq_export.RNASeqExportUtils import RNASeqExportUtils
#END_HEADER


class kb_rnaseq_export:
    '''
    Module Name:
    kb_rnaseq_export

    Module Description:
    A KBase module: kb_rnaseq_export
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        #END_CONSTRUCTOR
        pass


    def export_rna_seq_alignment_as_bam_to_staging(self, ctx, params):
        """
        :param params: instance of type "ExportStagingParams" -> structure:
           parameter "input_ref" of String, parameter "destination_dir" of
           String
        :returns: instance of type "ExportStagingOutput" -> structure:
           parameter "path" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_rna_seq_alignment_as_bam_to_staging
        modulen = "kb_rnaseq_export"
        methodn = "export_rna_seq_alignment_as_bam_to_staging"
        print '--->Running %s.%s\n\nparams:' % (modulen, methodn)
        params['rna_seq_type'] = 'RNASeqAlignment'
        params['download_file_type'] = 'bam'
        if 'destination_dir' not in params:
            raise ValueError("Missing destination directory")
        print json.dumps(params, indent=1)

        rna_seq_downloader = RNASeqExportUtils(self.config)
        output = rna_seq_downloader.download_RNASeq_Alignment_BAM(params)
        #END export_rna_seq_alignment_as_bam_to_staging

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_rna_seq_alignment_as_bam_to_staging return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
