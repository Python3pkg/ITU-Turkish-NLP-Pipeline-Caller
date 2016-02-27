#!/usr/bin/python3

name = "ITU Turkish NLP Pipeline Caller"
__copyright__ = "__copyright__ 2015 Ferit Tunçer"

__license__ = "GPLv2\n\
This program is free software; you can redistribute it and/or \
modify it under the terms of the GNU General Public __license__ version 2 \
as published by the Free Software Foundation. \
This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public __license__ for more details. \
You should have received a copy of the GNU General Public __license__ \
along with this program.  If not, see <http://www.gnu.org/__license__s/>."

__author__ = "Ferit Tunçer"
email = "ferit.tuncer@autistici.org"
website = "https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller"

version = "2.2.0"

import sys
import urllib.request
import urllib.parse
import time
import os.path
import argparse
import re
import locale

TOKEN_PATH = "pipeline.token"
DEFAULT_ENCODING = locale.getpreferredencoding(False)
DEFAULT_OUTPUT_DIR = "output"

class PipelineCaller:

    API_URL = "http://tools.nlp.itu.edu.tr/SimpleApi"
    PIPELINE_ENCODING = 'UTF-8'

    DEFULT_SENTENCE_SPLIT_DELIMITER_CLASS = "[\.\?:;!]"


    def __init__(self, tool='pipelineNoisy', text ='example', token='invalid', processing_type='whole'):
        self.tool = tool
        self.text = text
        self.token = token
        self.processing_type = processing_type


    def call(self):

        if self.processing_type=='whole':

            params = urllib.parse.urlencode({'tool': self.tool, 'input': self.text, 'token': self.token}).encode(self.PIPELINE_ENCODING)
            try:
                result = urllib.request.urlopen(self.API_URL, params)
                return result.read().decode(self.PIPELINE_ENCODING)
            except:
                raise

        if processing_type=='sentence':

            output = ""
            for sentence in self.getSentences():
                params = urllib.parse.urlencode({'tool': self.tool, 'input': sentence, 'token': self.token}).encode(self.PIPELINE_ENCODING)
                try:
                    result = urllib.request.urlopen(self.API_URL, params)
                    output += result.read().decode(self.PIPELINE_ENCODING)
                except:
                    raise
            return output

        if processing_type=='word':

            output = ""
            for word in self.getWords():
                params = urllib.parse.urlencode({'tool': self.tool, 'input': word, 'token': self.token}).encode(self.PIPELINE_ENCODING)
                try:
                    result = urllib.request.urlopen(self.API_URL, params)
                    output += result.read().decode(self.PIPELINE_ENCODING)
                except:
                    raise
            return output

    def getSentences(self):
        r = re.compile(r'(?<=(?:{}))\s+'.format(DEFULT_SENTENCE_SPLIT_DELIMITER_CLASS))
        sentences = r.split(self.text)
        sentence_count = len(sentences)
        if re.match("^\s*$", sentences[sentence_count-1]):
            sentences.pop(sentence_count-1)
        sentence_count = len(sentences)
        return sentences

    def getWords(self):
        return self.getSentences().split()



def __readInput(path, encoding):
    try:
        with open(path, encoding=encoding) as input_file:
            text = ""
            for line in input_file:
                text += line
        return text
    except:
        raise

def __readToken():
    try:
        token_file = open(TOKEN_PATH)
        token = token_file.readline().strip()
        return token
    except:
        raise

def __getOutputPath(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, "output{0}".format(str(time.time()).split('.')[0]))
        return filepath
    except:
        raise

def __conditional_info(to_be_printed, quiet):
    if quiet == 0:
        print(to_be_printed)

def __parseArguments():
    #epilog section is free now
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="ITU Turkish NLP Pipeline Caller v{}\n{} <{}>\n{}".format(version, __author__, email, website),
    add_help=True)
    parser.add_argument("filename", help="relative input filepath")
    parser.add_argument('-p', '--processing-type', dest='processing_type', choices=['word', 'sentence', 'whole'], default='whole', help='Switches processing type, default is whole text at once. Alternatively, word by word or sentence by sentence processing can be selected.')
    parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="no info during process")
    parser.add_argument("--tool", dest="tool", default="pipelineNoisy", choices=["ner", "morphanalyzer", "isturkish",  "morphgenerator", "tokenizer", "normalize", "deasciifier", "Vowelizer", "DepParserFormal", "DepParserNoisy", "spellcheck", "disambiguator", "pipelineFormal", "pipelineNoisy"], help="Switches pipeline tool which is \"pipelineNoisy\" by default")
    parser.add_argument("-e", "--encoding", dest="encoding", metavar="E", default=DEFAULT_ENCODING, help="force I/O to use given encoding, instead of default locale")
    parser.add_argument("-o", "--output", metavar="O", dest="output_dir", default=DEFAULT_OUTPUT_DIR, help="change output directory, \"{}\" by default".format(DEFAULT_OUTPUT_DIR))
    parser.add_argument('--version', action='version', version='{} {}'.format(name, version), help="version information")
    parser.add_argument('--license', action='version', version='{}'.format(__license__), help="license information")


    return parser.parse_args()

def main(args=None):
    if args is None:
        args = sys.argv[1:]
        
    args = __parseArguments()
    text = __readInput(args.filename, args.encoding)
    output_path = __getOutputPath(args.output_dir)
    token = __readToken()
    __conditional_info("[INFO] Pipeline tool: {}".format(args.tool), args.quiet)
    __conditional_info("[INFO] File I/O encoding: {}".format(args.encoding), args.quiet)
    __conditional_info("[INFO] Output destination: .{}{}".format(os.sep, output_path), args.quiet)
    start_time = time.time()

    caller = PipelineCaller(args.tool, text, token, args.processing_type)
    with open(output_path, 'w', encoding=args.encoding) as output_file:    
        output_file.write("{}\n".format(caller.call()))
    print("[DONE] It took {0} seconds to process whole text.".format(str(time.time()-start_time).split('.')[0]))


if __name__ == '__main__':
    main()

