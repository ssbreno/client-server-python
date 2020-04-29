import time
import random

from socket import  *
from client import Consumidor


lista_de_consumidores = []

quantidade_de_consumidores = int(input('Quantos consumidores?\n'))

lista_de_consumidores_estados = [True for i in range(quantidade_de_consumidores)]

for index in range(1, quantidade_de_consumidores + 1):

    valor = random.randint(100, 1000)
    consumer = Consumidor(index, valor, {'servidor': '127.0.0.1', 'porta': '8792'})
    lista_de_consumidores.append(consumer)

while any(lista_de_consumidores_estados):
    posicao = random.randint(0, quantidade_de_consumidores - 1)
    lista_de_consumidores_estados[posicao] = lista_de_consumidores[posicao].comunicar()

    time.sleep(.3)