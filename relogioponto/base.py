# -*- coding: utf-8 -*-
import socket
from threading import Thread
import time

class Colaborador(object):
    
    def __init__(self, relogio):
        self.relogio = relogio
        self.matriculas = []
        self.nome = None
        self.pis = None
        self.verificar_digital = None
        self.id = None
        
    def save(self):
        self.relogio.gravar_colaborador(self)
        
    
    def delete(self):
        self.relogio.apagar_colaborador(self)
    
    def __str__(self, *args, **kwargs):
        return str( {'id': self.id, 'nome': self.nome, 'pis': self.pis, 'matriculas': self.matriculas} )

    @property
    def digitais(self):
        return self.relogio.get_digitais(self)
    
    
class RelogioPonto(object):
        
    def __init__(self, endereco, porta=3000):
        self.tcp_socket = None
        self.endereco = endereco
        self.porta = porta
        self.conectado = None
        self.callback_func = []
    
    def conectar(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
        self.conectado = None
        rpself = self
        def run_thread():
            dest = (self.endereco, self.porta) 
            try:
                result = self.tcp_socket.connect_ex(dest) 
            except:
                result = None
            self.status_conexao = result             
            if result:
                self.conectado = False                                        
            else:              
                self.conectado = True
            while self.conectado:
                try:                    
                    data = rpself.tcp_socket.recv(64000)
                    rpself.receber_comando(data)                
                except:
                    self.conectado = False                    
                    break
                finally:
                    self.desconectar() 
        self.thread_conexao = Thread(target=run_thread)
        self.thread_conexao.start()
              
        while self.conectado is None:             
            time.sleep(0.2)

            
        if not self.conectado:
            raise Exception("Falha na conexao. Codigo de erro %s." % (self.status_conexao))   
    
    def __exit__(self, *err):
        self.desconectar()
    
    def __del__(self):
        self.desconectar()
    
    def apagar_colaborador(self, colaborador):
        raise NotImplementedError('Implementacao ausente')
        
    def desconectar(self):
        try:
            self.tcp_socket.shutdown(1)
            self.tcp_socket.close()
        except:
            pass
        self.tcp_socket = None
    
    @property    
    def colaboradores(self):
        raise NotImplementedError('Implementacao ausente na classe filha de RelogioPonto (colaboradores)')
    
    def gravar_colaborador(self, colaborador):
        raise NotImplementedError('Implementacao ausente na classe filha de RelogioPonto (gravar_colaborador)')
    
    def get_digitais(self, colaborador):
        raise NotImplementedError('Implementacao ausente na classe filha de RelogioPonto (get_digitais)')
    
    def enviar_comando(self, data):
        self.tcp_socket.send(data)
        time.sleep(0.5)
    
    def receber_comando(self, data):
        for cmd in self.callback_func:
            cmd(data)
        
    def add_listener(self, callback_func):
        self.callback_func.append(callback_func)   
        
    @property
    def data_hora(self):
        raise NotImplementedError('Implementacao ausente na classe filha de RelogioPonto (data_hora)')
    
    @data_hora.setter
    def data_hora(self, value):
        raise NotImplementedError('Implementacao ausente na classe filha de RelogioPonto (data_hora)')
    
        
