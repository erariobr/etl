'''
Created on Jul 17, 2015

@author: ivan
'''

from sqlalchemy.orm import Session

class Importador(object):
    '''
    Importador 
    '''

    def __init__(self, arquivo):
        '''
        Constructor
        '''
        self.arquivo = arquivo
        
        
    def processa(self):
        cabecalho  = self.arquivo.readline().strip()
        colunas = cabecalho.split('\t')
        num_colunas = len(colunas)
        num_linhas = 0;
        for linha in self.arquivo:
            dados = linha.strip().split('\t')
            while(len(dados) != num_colunas):
                print("Nova linha no meio de csv, trazendo + uma para completar")
                dados.append(self.arquivo.readline().strip().split('\t'))
                
            
            num_linhas += 1
            session = Session();
            session.execute(
                            "INSERT IGNORE INTO estado (sigla) VALUES (:sigla)" ,
                            {"sigla": dados[0]}
                            )
            
        