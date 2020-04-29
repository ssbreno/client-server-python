from socket import  *

class Consumidor:
    def __init__(self, index, qtd_produto, conexao):
        self.index = index
        self.qtd_produto = qtd_produto
        self.conexao = conexao
        
        resto = qtd_produto/10 % int(qtd_produto/10)
        lista_de_pedidos = [int(qtd_produto/10) for x in range(10)]
        lista_de_pedidos.append(int(resto*10+.1))

        self.lista_de_pedidos = lista_de_pedidos
        self.proximo_pedido = iter(lista_de_pedidos)
        self.index_ultimo_pedido = 0

        self.conectaSocket()

    def conectaSocket(self):
        servidor = self.conexao['servidor']
        porta = int(self.conexao['porta'])
        self.socket = socket()
        self.socket.connect((servidor, porta))

    def comunicar(self):
        self.index_ultimo_pedido += 1

        try:
            valor_do_pedido = next(self.proximo_pedido)
        except StopIteration:
            return False
        except IndexError:
            return False

        debug_msg = "Consumidor {index_consumidor}: Pedido {index_pedido} de {valor} produtos realizados com sucesso".format(
            index_consumidor=self.index,
            index_pedido=self.index_ultimo_pedido,
            valor=valor_do_pedido,
            )

        send_msg = "{index_consumidor} {numero_pedido} {valor_pedido}".format(
            index_consumidor=self.index,
            numero_pedido=self.index_ultimo_pedido,
            valor_pedido=valor_do_pedido
            )

        msg_buffer = str.encode(send_msg, "UTF-8")

        self.socket.send(msg_buffer)
        response = (self.socket.recv(1024)).decode("UTF-8")

        print(debug_msg)
        return True
    
    def quantidadeTotalDePedidos(self):
        return len(self.lista_de_pedidos)
