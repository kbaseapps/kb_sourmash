
import time
import os
import subprocess
import uuid
import json
import shutil

from KBaseReport.KBaseReportClient import KBaseReport
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from AssemblyUtil.baseclient import ServerError as AssemblyUtilError

SOURMASH_COMPUTE = "sourmash compute"
KSIZE = 31

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class SourmashUtils:

    SOURMASH_COMPUTE = "sourmash compute"
    SOURMASH_COMPARE = "sourmash compare"
    SOURMASH_PLOT = "sourmash plot"
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
        _stage_assembly_files: download the fasta files to the scratch area in a 'fasta' directory and return list of file names
        """
        log('Processing assembly object list: {}'.format(object_list))

        output_directory = os.path.join(self.scratch, 'fasta')
        self._mkdir_p(output_directory)

        auc = AssemblyUtil(self.callbackURL)
        staged_file_list = []

        for assembly_upa in object_list:
            filename = os.path.join(output_directory, assembly_upa.replace('/', '_') + '.fa')
            try:
                auc.get_assembly_as_fasta({'ref': assembly_upa, 'filename': filename})
            except AssemblyUtilError as assembly_error:
                print(str(assembly_error))
                raise
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
            log('Executed commend:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running commend:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _build_signatures(self, assembly_files_list, scaled):
        """
        _build_signatures: take list of fasta files, run sourmash compute, save
        output signature file
        """

        signatures_file = os.path.join(self.scratch, 'signatures')

        compute_command = [self.SOURMASH_COMPUTE, '-k', str(self.KSIZE), '--scaled',
                str(scaled), '-o', signatures_file] + assembly_files_list

        self._run_command(" ".join(compute_command))
        return signatures_file

    def _generate_report(self, compare_outfile, workspace_name):
        """
        _generate_report: uses the basename to add the pngs to the html report
        """
        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)

        report_html_file = os.path.join(output_directory, 'report.html')

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

        report_params = {
            'message': '',
            'workspace_name': workspace_name,
            'html_links': [{'path': report_html_file,
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

        self._validate_sourmash_compare_params(params)
        os.chdir(self.scratch)

        assembly_files_list = self._stage_assembly_files(params.get('object_list'))

        #build signatures from fasta files
        signatures_file = self._build_signatures(assembly_files_list, params['scaled'])

        #run compare command
        compare_outfile = os.path.join(self.scratch, 'compare.out')
        compare_command = [self.SOURMASH_COMPARE, '-k', str(self.KSIZE), '-o',
            compare_outfile, signatures_file]

        self._run_command(" ".join(compare_command))

        #make plots
        plot_command = [self.SOURMASH_PLOT, compare_outfile, '--labels']
        self._run_command(" ".join(plot_command))

        #make report

        report = self._generate_report(compare_outfile, params['workspace_name'])

        results = {'report_name': report['name'], 'report_ref': report['ref']}
        return results
