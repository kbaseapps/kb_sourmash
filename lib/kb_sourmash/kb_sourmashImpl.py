# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import subprocess
import uuid

from KBaseReport.KBaseReportClient import KBaseReport
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
    GIT_COMMIT_HASH = "8002280c5b5730018cd6768195ad457918da5c0b"

    #BEGIN_CLASS_HEADER
    SOURMASH = "sourmash"
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
           String
        :returns: instance of type "SourmashResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_sourmash

        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')

        workspace_name = params['workspace_name']

        run_dir = "/kb/module/test/data/"

        print("quick test of sourmash\n")
        # make index
        print("Making sourmash index:\n")
        sourmash_index_cmd = [self.SOURMASH, 'index', '-k', str(31),
                                'ecolidb', 'ecoli_many_sigs/*.sig']

        print('     ' + ' '.join(sourmash_index_cmd))

        p=subprocess.Popen(" ".join(sourmash_index_cmd), cwd=run_dir, shell=True)
        retcode = p.wait()

        if p.returncode != 0:
            raise ValueError('Error running sourmash index, return code: ' + str(retcode) + "\n")

        #make ecoli genome sig
        print("Making ecoli genome sig.\n")
        sourmash_compute_cmd = [self.SOURMASH, 'compute', '--scaled', str(2000),
                                '-k', str(31), 'ecoliMG1655.fa',
                                '-o', 'ecoli-genome.sig']

        print('     ' + ' '.join(sourmash_compute_cmd))
        p=subprocess.Popen(" ".join(sourmash_compute_cmd), cwd=run_dir, shell=True)
        retcode = p.wait()

        if p.returncode != 0:
            raise ValueError('Error running sourmash compute, return code: ' + str(retcode) + "\n")

        # search using sourmash index
        sourmash_cmd = [self.SOURMASH, 'search', 'ecoli-genome.sig',
                        'ecolidb.sbt.json', '-n', str(20) ]

        print("Searching index...\n")
        print('     ' + ' '.join(sourmash_cmd))

        p=subprocess.Popen(" ".join(sourmash_cmd), cwd=run_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        retcode = p.wait()

        if p.returncode != 0:
            raise ValueError('Error running sourmash search, return code: ' + str(retcode) + "\n")

        results, err = p.communicate()
        message = err + "\n" + results

        print("Results\n", results, "\nErr:\n", err)

        #save report
        kbr = KBaseReport(self.callbackURL)
        try:
            report_info = kbr.create_extended_report(
                {
                'message': message,
                #'objects_created': [],
                'workspace_name':workspace_name,
                #'direct_html_link_index':0,
                'report_object_name': 'sourmash_report_' + str(uuid.uuid4())
                })
        except:
            print("exception from saving report")
            raise

        results = {'report_name': report_info['name'], 'report_ref': report_info['name']}
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
