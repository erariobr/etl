'''
Created on Jul 17, 2015

@author: ivan
'''
from erariodwh.etl.base import Importador

class GastosDiretos(Importador):
    '''
    Importa gastos diretos
    '''


    def __init__(self, arquivo):
        '''
        Constructor
        '''
        super(self.__class__, self).__init__(arquivo)
        
        
    