# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_sourmash.kb_sourmashImpl import kb_sourmash
from kb_sourmash.kb_sourmashServer import MethodContext
from kb_sourmash.authclient import KBaseAuth as _KBaseAuth
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil

class kb_sourmashTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_sourmash'):
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
                            {'service': 'kb_sourmash',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        suffix = int(time.time() * 1000)
        wsName = "test_kb_sourmash_" + str(suffix)
        cls.ws_info = cls.wsClient.create_workspace({'workspace': wsName})
        cls.serviceImpl = kb_sourmash(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.au = AssemblyUtil(os.environ['SDK_CALLBACK_URL'])
        cls.setup_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def setup_data(cls):
        tf = 'ecoliMG1655.fa'
        target = os.path.join(cls.scratch, tf)
        shutil.copy('data/' + tf, target)
        cls.ref = cls.au.save_assembly_from_fasta({'file': {'path': target},
                                                   'workspace_name': cls.ws_info[1],
                                                   'assembly_name': 'ecoliMG1655'})

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_sourmash_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def xtest_run_sourmash(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        params = {'input_assembly_upa': self.ref, 'workspace_name': self.getWsName(),
                  'search_db': "Ecoli"}
        self.getImpl().run_sourmash(self.getContext(), params)
        pass

    def xtest_run_sourmash_compare(self):
        tf = 'ecoliMG1655.fa'
        target = os.path.join(self.scratch, tf)
        ref2 = self.au.save_assembly_from_fasta(
            {'file': {'path': target},
             'workspace_name': self.getWsName(),
             'assembly_name': 'ecoliMG1655_2'})

        params = {'object_list': [self.ref, ref2], 'workspace_name': self.getWsName()}
        self.getImpl().run_sourmash_compare(self.getContext(), params)
        pass

    def test_run_sourmash_search(self):
        params = {'input_assembly_upa': self.ref, 'workspace_name': self.getWsName(),
                  'search_db': 'Ecoli', 'containment':"1"}
        self.getImpl().run_sourmash_search(self.getContext(), params)
        pass

    def test_run_sourmash_gather(self):
        params = {'input_assembly_upa': self.ref, 'workspace_name': self.getWsName(),
                  'search_db': 'Genbank'}
        self.getImpl().run_sourmash_gather(self.getContext(), params)
        pass
