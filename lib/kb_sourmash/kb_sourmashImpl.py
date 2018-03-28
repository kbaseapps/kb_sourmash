# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import subprocess
import uuid

from KBaseReport.KBaseReportClient import KBaseReport
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from AssemblyUtil.baseclient import ServerError as AssemblyUtilError
#END_HEADER


class kb_sourmash:
    '''
    Module Name:
    kb_sourmash

    Module Description:
    A KBase module: kb_sourmash
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/psdehal/kb_sourmash.git"
    GIT_COMMIT_HASH = "bcb4d53d86e7c13fbdd6696dbed274638f9a267d"

    #BEGIN_CLASS_HEADER
    SOURMASH = "sourmash"

    def get_assembly(self, target_dir, assembly_upa):
        auc = AssemblyUtil(self.callbackURL)
        filename = os.path.join(target_dir, assembly_upa.replace('/', '_'))
        try:
            auc.get_assembly_as_fasta({'ref': assembly_upa, 'filename': filename})
        except AssemblyUtilError as assembly_error:
            print(str(assembly_error))
            raise
        return filename

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        #END_CONSTRUCTOR
        pass


    def run_sourmash(self, ctx, params):
        """
        :param params: instance of type "SourmashParams" (Insert your
           typespec information here.) -> structure: parameter
           "input_assembly_upa" of String, parameter "workspace_name" of
           String, parameter "search_db" of String, parameter "scaled" of Long
        :returns: instance of type "SourmashResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_sourmash

        data_dir = "/kb/module/test/data/"
        share_dir = "/kb/module/work/tmp/"

        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_assembly_upa' not in params:
            raise ValueError('input_assembly_upa parameter is required')

        if 'scaled' in params:
            if params['scaled']:
                scaled = params['scaled']
        else:
            scaled = 1000

        if 'search_db' not in params:
            raise ValueError('search_db parameter is required')
        elif params['search_db'] == "Ecoli":
            search_db = os.path.join(data_dir, 'ecolidb.sbt.json')
        elif params['search_db'] == "Genbank":
            search_db = "/data/genbank-k31.sbt.json"
        else:
            raise ValueError('search_db must be Ecoli or Genbank')

        workspace_name = params['workspace_name']
        input_assembly_upa = params['input_assembly_upa']

        # get assembly fasta file
        input_sequence_file = self.get_assembly(share_dir, input_assembly_upa)
        input_sequence_sig = input_assembly_upa.replace('/', '_') + ".sig"


        #make genome sig
        print("Making genome sig:\n")
        sourmash_compute_cmd = [self.SOURMASH, 'compute', '--scaled', scaled,
                                '-k', str(31), input_sequence_file,
                                '-o', input_sequence_sig]

        p=subprocess.Popen(" ".join(sourmash_compute_cmd), cwd=share_dir, shell=True)
        retcode = p.wait()

        if p.returncode != 0:
            raise ValueError('Error running sourmash compute, return code: ' + str(retcode) + "\n")

        # search using sourmash index
        sourmash_cmd = [self.SOURMASH, 'search', input_sequence_sig,
                        search_db, '-n', str(20) ]

        print("Searching index " + search_db + " ...\n")
        print('     ' + ' '.join(sourmash_cmd))

        p=subprocess.Popen(" ".join(sourmash_cmd), cwd=share_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        retcode = p.wait()

        if p.returncode != 0:
            #raise ValueError('Error running sourmash search, return code: ' + str(retcode) + "\n")
            print('Error running sourmash search, return code: ' + str(retcode) + "\n")

        results, err = p.communicate()
        message = err + "\n" + results

        print("Results\n", results, "\nErr:\n", err)

        sourmash_cmd = [self.SOURMASH, 'gather', input_sequence_sig,
                        search_db, '-k', str(31) ]

        print("gathering index " + search_db + " ...\n")
        print('     ' + ' '.join(sourmash_cmd))

        p=subprocess.Popen(" ".join(sourmash_cmd), cwd=share_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        retcode = p.wait()

        if p.returncode != 0:
            #raise ValueError('Error running sourmash search, return code: ' + str(retcode) + "\n")
            print('Error running sourmash gather, return code: ' + str(retcode) + "\n")

        results, err = p.communicate()
        message = message + err + "\n" + results

        print("Results\n", results, "\nErr:\n", err)

        #save report
        kbr = KBaseReport(self.callbackURL)
        try:
            report_info = kbr.create_extended_report(
                {
                'message': message,
                #'objects_created': [],
                'workspace_name': workspace_name,
                #'direct_html_link_index':0,
                'report_object_name': 'sourmash_report_' + str(uuid.uuid4())
                })
        except:
            print("exception from saving report")
            raise

        results = {'report_name': report_info['name'], 'report_ref': report_info['ref']}
        #END run_sourmash

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method run_sourmash return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
