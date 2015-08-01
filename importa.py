#!/usr/local/bin/python
# encoding: utf-8
'''
Importa CSVs governamentais para o sistema Erario

@author:     Ivan Stoiev

@copyright:  Ivan Stoiev

@license:    MIT license

@contact:    ivan.stoiev@gmail.com
@deffield    updated: Updated
'''

import sys
import os
import gettext
import argparse
import traceback
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from erariodwh.etl.uniao import GastosDiretos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def convertArgparseMessages(s):
    subDict = \
    {'positional arguments':'Argumento obrigatório',
    'optional arguments':'Argumentos opcionais',
    'show this help message and exit':'mostra ajuda',
    'usage: ': 'uso: '
    }
    if s in subDict:
        s = subDict[s]
    return s
gettext.gettext = convertArgparseMessages



class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]


    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            dest="caminho",
            help="caminho do arquivo a ser importado",
            type=argparse.FileType('r', encoding="ISO-8859-1")
        )
        parser.add_argument(
            dest="dsn",
            help="configuracao de aceso a base de dados"
        )

        # Process arguments
        args = parser.parse_args()


        engine = create_engine(args.dsn, echo=True)
        engine.connect();
        sessionmaker(bind=engine)
                
        gd = GastosDiretos(args.caminho)
        gd.processa()
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  para ajuda, use --help")
        traceback.print_exc()
        return 2

if __name__ == "__main__":
    sys.exit(main())