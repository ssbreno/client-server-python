from socket import *
from threading import Thread

class ConsumerServer:
    def __init__(self, conexao):

        print('Iniciando...\n')

        self.estoque = 1000
        self.conexao = conexao
        self.socket = socket()
        self.clientes = []

        self.AbrirConexao(self.conexao, 100)
        
    
    def AbrirConexao(self, conexao, limite):
        
        host = self.conexao['host']
        porta = int(self.conexao['porta'])

        self.socket.bind((host, porta))
        self.socket.listen(limite)

    def Escutar(self, estado):
        print('Aguardando transmissão ...\n')

        while estado:
            conexao, cliente = self.socket.accept()
            print("Recebi a conexao de " + str(cliente))
            thread = Thread(target=self.Atender,args=(conexao, cliente))
            self.clientes.append({'Thread': thread, 'requisitado_total': 0})
            print ("Criando Thread " + str(len(self.clientes)))
            self.clientes[-1]['Thread'].start()

    def Atender(self, socket, cliente):
        while True:
            try:
                data = socket.recv(4096)
                socket.send(str.encode ("Servidor:" + "Ok", "UTF-8"))
            except ConnectionError:
                print('Fim da transmissão com', str(cliente))
                break
            
            recebido = list(map(str, data.decode("utf-8").split(' ')))
            
            if len(recebido) == 3:
                consumidor, index_pedido, valor = map(int, recebido)

                self.clientes[int(consumidor-1)]['requisitado_total'] += valor
                self.estoque += valor * -1

                if self.estoque < 100:
                    self.estoque += 1000

                    print('Consumidor\tProdutos')
                    for cliente, total in enumerate(self.clientes):
                        msg_estoque = '{cliente}\t\t{total}'.format(
                            cliente = cliente,
                            total = total['requisitado_total']
                            )

                        print(msg_estoque)

                debug_msg = "Consumidor {consumidor} está solicitando {valor} produtos".format(
                    consumidor = consumidor,
                    valor = valor
                    )

                print (debug_msg)

servidor = ConsumerServer({'host': '127.0.0.1', 'porta': '8792'})

servidor.Escutar(True)