# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import mock

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_rnaseq_export.kb_rnaseq_exportImpl import kb_rnaseq_export
from kb_rnaseq_export.kb_rnaseq_exportServer import MethodContext
from kb_rnaseq_export.authclient import KBaseAuth as _KBaseAuth

class rau_mock(object):
    def __init__(self, callback, ver='dev', token=None):
       pass

    def download_alignment(self, params):
        ddir = '/kb/module/work/tmp'
        with open(ddir+'/accepted_hits.bam', 'w') as f:
            f.write("bogus")
        return {'destination_dir': ddir}



class kb_rnaseq_exportTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_rnaseq_export'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_rnaseq_export',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_rnaseq_export(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_rnaseq_export_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @mock.patch('kb_rnaseq_export.RNASeqExportUtils.ReadsAlignmentUtils', rau_mock)
    def test_export_rna_seq_alignment_as_bam_to_staging(self):
        self.alignment_ref_1 = '1/2/3'
        params = {
            'input_ref': self.alignment_ref_1,
            'destination_dir': '/staging'
        }
        ret = self.getImpl().export_rna_seq_alignment_as_bam_to_staging(
              self.getContext(), params)
        self.assertTrue('path' in ret[0])
        self.assertTrue(os.path.exists('/staging/accepted_hits.bam'))
