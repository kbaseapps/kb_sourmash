
import time
import os
import subprocess
import uuid
import json
import shutil

from KBaseReport.KBaseReportClient import KBaseReport
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from AssemblyUtil.baseclient import ServerError as AssemblyUtilError
from DataFileUtil.DataFileUtilClient import DataFileUtil


SOURMASH_COMPUTE = "sourmash compute"
KSIZE = 31


def log(message, prefix_newline=False):
    """
    Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time())
          + ': ' + str(message))


class SourmashUtils:

    SOURMASH_COMPUTE = "sourmash compute"
    SOURMASH_COMPARE = "sourmash compare"
    SOURMASH_PLOT = "sourmash plot"
    SOURMASH_SEARCH = "sourmash search"
    SOURMASH_GATHER = "sourmash gather"
    SOURMASH_CLASSIFY = "sourmash lca classify"
    SOURMASH_SUMMARIZE = "sourmash lca summarize"
    SOURMASH_LCA_GATHER = "sourmash lca gather"

    KSIZE = 31

    def __init__(self, config):
        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']

    def _validate_sourmash_compare_params(self, params):
        """
        simple validation for required parameters
        """
        log('Start paramter validation.')

        for p in ['object_list', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _validate_sourmash_search_params(self, params):
        """
        very simple validation for required paramteres
        """
        log('Start parameter validation.')

        for p in ['input_assembly_upa', 'workspace_name', 'search_db']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _validate_sourmash_gather_params(self, params):
        """
        right now, the params are the same as search
        """
        self._validate_sourmash_search_params(params)

    def _validate_sourmash_lca_classify_params(self, params):
        """
        very simple validation for required paramteres
        """
        log('Start parameter validation.')

        for p in ['input_assembly_upa', 'workspace_name', 'lca_search_db']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _validate_sourmash_lca_summarize_params(self, params):
        """
        very simple validation for required paramteres
        """
        self._validate_sourmash_lca_classify_params(params)

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _stage_assembly_files(self, object_list):
        """
        _stage_assembly_files: download the fasta files to the scratch area
        return list of file names
        """
        log('Processing assembly object list: {}'.format(object_list))

        # Sourmash uses the sequence filename as the default label for the signatures
        # this includes the complete file path. So keeping the sequence file name as close
        # to the desired label as possible is the reason not to place each file under
        # a 'fasta' directory or inlude the '.fa' file extension

        auc = AssemblyUtil(self.callbackURL)
        staged_file_list = []

        for assembly_upa in object_list:
            try:
                file = auc.get_assembly_as_fasta({'ref': assembly_upa})['path']
            except AssemblyUtilError as assembly_error:
                print(str(assembly_error))
                raise
            filename = os.path.basename(file).replace('.fa', '')
            to_upper_command = "awk '{ if ($0 !~ />/) {print toupper($0)} else {print $0} }' " \
                               + file + ' > tmp.fa ' + '&& mv tmp.fa ' + filename
            self._run_command(to_upper_command)
            staged_file_list.append(filename)

        log('Created file list: {}'.format(staged_file_list))
        return staged_file_list

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed command:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running command:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _build_signatures(self, assembly_files_list, scaled, track_abundance):
        """
        _build_signatures: take list of fasta files, run sourmash compute, save
        output signature file
        """

        signatures_file = 'signatures'

        compute_command = [self.SOURMASH_COMPUTE, '-k', str(self.KSIZE), '--scaled', str(scaled),
                           '-o', signatures_file, track_abundance] + assembly_files_list

        self._run_command(" ".join(compute_command))
        return signatures_file

    def _set_search_db(self, searchdb_label):
        """
        label to search db file path
        """
        if (searchdb_label == "Ecoli"):
            search_db = '/kb/module/test/data/ecolidb.sbt.json'
        elif searchdb_label == "Genbank":
            search_db = "/data/genbank-k31.sbt.json"
        elif searchdb_label == "img_bact_mags":
            search_db = "/data/img_bact_mags.sbt.json"
        elif searchdb_label == "img_arch_isol":
            search_db = "/data/img_arch_isol.sbt.json"
        elif searchdb_label == "img_bact_isol":
            search_db = "/data/img_bact_isol.sbt.json"
        elif searchdb_label == "img_arch_mags":
            search_db = "/data/img_arch_mags.sbt.json"
        elif searchdb_label == "img_bact_sags":
            search_db = "/data/img_bact_sags.sbt.json"
        elif searchdb_label == "img_arch_sags":
            search_db = "/data/img_arch_sags.sbt.json"
        elif search_db_label == "img_metag_metat_no_raw":
            search_db = "/data/metaG_metaT_no_raw.sbt.json"
        else:
            raise ValueError('search_db not valid')

        return search_db

    def _generate_report(self, compare_outfile, workspace_name):
        """
        _generate_report: uses the basename to add the pngs to the html report
        """
        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)

        report_html_file = os.path.join(output_directory, 'index.html')

        shutil.copy(compare_outfile, output_directory)
        shutil.copy(compare_outfile + '.labels.txt', output_directory)
        shutil.copy(compare_outfile + '.dendro.png', output_directory)
        shutil.copy(compare_outfile + '.hist.png', output_directory)
        shutil.copy(compare_outfile + '.matrix.png', output_directory)

        base = os.path.basename(compare_outfile)

        html_file = open(report_html_file, 'w')

        html_file.write('<HTML><BODY>')
        html_file.write('<img src="{}"><img src="{}"><img src="{}">'.
                        format(base+'.dendro.png', base+'.hist.png', base+'.matrix.png'))
        html_file.write('</BODY></HTML>')

        html_file.close()

        dfu = DataFileUtil(self.callbackURL)
        shock = dfu.file_to_shock({'file_path': output_directory,
                                  'make_handle': 0, 'pack': 'zip'})

        report_params = {
            'message': '',
            'workspace_name': workspace_name,
            'html_links': [{'path': report_html_file,
                            'shock_id': shock['shock_id'],
                            'name': os.path.basename(report_html_file),
                            'label': os.path.basename(report_html_file),
                            'description': 'HTML report for sourmash compare'}],
            'direct_html_link_index': 0,
            'html_window_height': 266,
            'report_object_name': 'kb_sourmash_compare_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callbackURL)
        output = kbase_report_client.create_extended_report(report_params)

        return output

    def run_sourmash_compare(self, params):
        """
        run sourmash compare app
        """
        log('--->\nrunning run_sourmash_compare\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        if 'scaled' not in params:
            params['scaled'] = 1000

        track_abundance = ''

        self._validate_sourmash_compare_params(params)
        os.chdir(self.scratch)

        assembly_files_list = self._stage_assembly_files(params.get('object_list'))

        # build signatures from fasta files
        signatures_file = self._build_signatures(assembly_files_list, params['scaled'],
                                                 track_abundance)

        # run compare command
        compare_outfile = 'compare.out'
        compare_command = [self.SOURMASH_COMPARE, '-k', str(self.KSIZE), '-o',
                           compare_outfile, signatures_file]

        self._run_command(" ".join(compare_command))

        # make plots
        plot_command = [self.SOURMASH_PLOT, compare_outfile, '--labels']
        self._run_command(" ".join(plot_command))

        # make report

        report = self._generate_report(compare_outfile, params['workspace_name'])

        results = {'report_name': report['name'], 'report_ref': report['ref']}
        return results

    def run_sourmash_search(self, params):
        """
        given an input assembly, run sourmash search against selected signature
        database and return report including list of hits
        """
        log('--->\nrunning run_sourmash_search\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_sourmash_search_params(params)

        if 'scaled' not in params:
            params['scaled'] = 1000

        if 'search_db' not in params:
            raise ValueError('search_db parameter is required')
        else:
            search_db = self._set_search_db(params['search_db'])

        if params.get('containment'):
            containment_flag = '--containment'
        else:
            containment_flag = ''

        track_abundance = ''

        os.chdir(self.scratch)

        assembly_file = self._stage_assembly_files([params['input_assembly_upa']])

        signature_file = self._build_signatures(assembly_file, params['scaled'], track_abundance)

        # run search
        search_command = [self.SOURMASH_SEARCH, signature_file, search_db,
                          '-n', str(20), containment_flag]
        self._run_command(' '.join(search_command))

        results = {'report_name': '', 'report_ref': ''}
        return results

    def run_sourmash_gather(self, params):
        """
        input assembly, run gather against selected database return report
        """
        log('--->\nrunning run_sourmash_gather\nparams:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_sourmash_gather_params(params)

        if 'scaled' not in params:
            params['scaled'] = 1000

        if 'search_db' not in params:
            raise ValueError('search_db parameter is required')
        else:
            search_db = self._set_search_db(params['search_db'])

        if 'track_abundance' not in params:
            params['track_abundance'] = ''
        elif params['track_abundance'] == 0:
            params['track_abundance'] = ''
        elif params['track_abundance'] == 1:
            params['track_abundance'] = '--track-abundance'
        else:
            raise ValueError('track_abundance should be 0 or 1, got '
                             + str(params['track_abundance']))

        os.chdir(self.scratch)

        assembly_file = self._stage_assembly_files([params['input_assembly_upa']])

        signature_file = self._build_signatures(assembly_file, params['scaled'],
                                                params['track_abundance'])

        # run gather
        gather_command = [self.SOURMASH_GATHER, '-k', str(self.KSIZE), signature_file, search_db]
        self._run_command(' '.join(gather_command))

        results = {'report_name': '', 'report_ref': ''}
        return results

    def run_sourmash_lca_classify(self, params):
        """
        input assembly and classify using lca db return report
        """
        log('--->\nrunning run_sourmash_lca_classify\nparams:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_sourmash_lca_classify_params(params)

        if 'scaled' not in params:
            params['scaled'] = 1000

        if 'lca_search_db' not in params:
            raise ValueError('lca_search_db parameter is required')
        elif params['lca_search_db'] == 'Genbank':
            lca_search_db = "/data/genbank-k31.lca.json"
        else:
            raise ValueError('invalid lca_search_db name')

        os.chdir(self.scratch)

        assembly_file = self._stage_assembly_files([params['input_assembly_upa']])

        signature_file = self._build_signatures(assembly_file, params['scaled'],
                                                params.get('track_abundance', ''))

        classify_command = [self.SOURMASH_CLASSIFY, '--query',
                            signature_file, '--db', lca_search_db]
        self._run_command(' '.join(classify_command))

        results = {'report_name': '', 'report_ref': ''}
        return results

    def run_sourmash_lca_summarize(self, params):
        """
        input assembly and summarize taxonomy using lca db returns report
        """
        log('--->\nrunning run_sourmash_lca_summarize\nparams:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_sourmash_lca_summarize_params(params)

        if 'scaled' not in params:
            params['scaled'] = 1000

        if 'lca_search_db' not in params:
            raise ValueError('lca_search_db parameter is required')
        elif params['lca_search_db'] == 'Genbank':
            lca_search_db = "/data/genbank-k31.lca.json"
        else:
            raise ValueError('invalid lca_search_db name')

        os.chdir(self.scratch)

        assembly_file = self._stage_assembly_files([params['input_assembly_upa']])

        signature_file = self._build_signatures(assembly_file, params['scaled'],
                                                params.get('track_abundance', ''))

        summarize_command = [self.SOURMASH_SUMMARIZE, '--scaled', str(params['scaled']),
                             '--query', signature_file, '--db', lca_search_db]
        self._run_command(' '.join(summarize_command))

        results = {'report_name': '', 'report_ref': ''}
        return results

    def run_sourmash_lca_gather(self, params):
        """
        input assembly run lca gather and return report
        """
        log('--->\nrunning run_sourmash_lca_gather\nparams:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_sourmash_lca_summarize_params(params)

        if 'scaled' not in params:
            params['scaled'] = 1000

        if 'lca_search_db' not in params:
            raise ValueError('lca_search_db parameter is required')
        elif params['lca_search_db'] == 'Genbank':
            lca_search_db = "/data/genbank-k31.lca.json"
        else:
            raise ValueError('invalid lca_search_db name')

        os.chdir(self.scratch)

        assembly_file = self._stage_assembly_files([params['input_assembly_upa']])

        signature_file = self._build_signatures(assembly_file, params['scaled'],
                                                params.get('track_abundance', ''))

        gather_command = [self.SOURMASH_LCA_GATHER, signature_file, lca_search_db]
        self._run_command(' '.join(gather_command))

        results = {'report_name': '', 'report_ref': ''}
        return results
