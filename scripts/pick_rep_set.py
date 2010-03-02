#!/usr/bin/env python
# File created on 09 Feb 2010
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Rob Knight","Greg Caporaso", "Kyle Bittinger"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Pre-release"

from qiime.util import parse_command_line_parameters
from optparse import make_option
from qiime.pick_rep_set import rep_set_picking_methods

script_info={}
script_info['brief_description'] = """Pick representative set of sequences"""
script_info['script_description'] = """After picking OTUs, you can then pick a representative set of sequences. For each OTU, you will end up with one sequence that can be used in subsequent analyses. By default, the representative sequence for an OTU is chosen as the most abundant sequence showing up in that OTU. This is computed by collapsing identical sequences, and choosing the one that was read the most times as the representative sequence (note that each of these would have a different sequence identifier in the FASTA provided as input)."""
script_info['script_usage'] = []
script_info['script_usage'].append(("""Simple example""", """The script pick_rep_set.py takes as input an 'OTU file' (via the \"-i\" parameter) which maps OTU identifiers to sequence identifiers. Typically, this will be the output file provided by pick_otus.py. Additionally, a FASTA file is required, via \"-f\", which contains all of the sequences whose identifiers are listed in the OTU file. The following command shows an example of this where the resulting file is output to the directory \"repr_set/\" and default parameters were used (choose most abundant, sort by OTU id and do not write a log file):""", """pick_rep_set.py -i seqs_otus.txt -f seqs.fna -o repr_set/"""))
script_info['script_usage'].append(("""Random selection example""", """Alternatively, if the user would like to choose the sequence by random \"-m random\" and then sort by the sequence identifier (\"-s seq_id\"), they could use the following command:""", """pick_rep_set.py -i seqs_otus.txt -f seqs.fna -o repr_set/ -m random -s seq_id"""))
script_info['output_description'] = """The output from pick_rep_set.py is a single FASTA file containing one sequence per OTU. The FASTA header lines will be the OTU identifier (from here on used as the unique sequence identifier) followed by a space, followed by the sequence identifier originally associated with the representative sequence. The name of the output FASTA file will be <input_sequences_filepath>_rep_set.fasta by default, or can be specified via the \"-o\" parameter.
"""
script_info['required_options'] = [\
 make_option('-i','--input_file',action='store',\
          type='string',dest='otu_fp',help='Path to '+\
          'input otu mapping file [REQUIRED]'),\
 make_option('-f','--fasta_file',action='store',\
          type='string',dest='fasta_fp',help='Path to input '+\
          'fasta file [REQUIRED]'),\
]
rep_set_picking_method_choices = rep_set_picking_methods.keys()
script_info['optional_options']=[\
 make_option('-m','--rep_set_picking_method',\
          type='choice',dest='rep_set_picking_method',
          help=('Method for picking representative sets.  Valid choices are ' +\
                ', '.join(rep_set_picking_method_choices) +\
                '[default: %default]'),\
          choices=rep_set_picking_method_choices,default='most_abundant'),\
 make_option('-o','--result_fp',action='store',\
          type='string',dest='result_fp',help='Path to store '+\
          'result file [default: <input_sequences_filepath>_rep_set.fasta]'),\
 make_option('-l','--log_fp',action='store',\
          type='string',dest='log_fp',help='Path to store '+\
          'log file [default: No log file created.]'),\
 make_option('-s', '--sort_by', action='store',\
            type='string', dest='sort_by', default='otu',
            help='sort by otu or seq_id [default: %default]')
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
      
    rep_set_picker =\
     rep_set_picking_methods[opts.rep_set_picking_method]
     
    input_seqs_filepath = opts.fasta_fp

    input_otu_filepath = opts.otu_fp
   
    result_path = opts.result_fp or\
     '%s_rep_set.fasta' % input_seqs_filepath
     
    log_path = opts.log_fp
    
    rep_set_picker(input_seqs_filepath, input_otu_filepath,
     result_path=result_path,log_path=log_path, sort_by=opts.sort_by)


if __name__ == "__main__":
    main()
