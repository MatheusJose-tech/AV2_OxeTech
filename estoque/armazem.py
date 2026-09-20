class Normal():
    def __init__(self, nome, dias_vendas, qualidade):
        self.nome = nome
        self.dias_vendas = dias_vendas
        self.qualidade = qualidade

    def atualizar(self):

        self.dias_vendas -= 1

        perca_qualidade = 2 if self.dias_vendas < 0 else 1
        nova_qualidade = self.qualidade - perca_qualidade

        self.qualidade = min(50, max(0, nova_qualidade))

class Queijo_envelhecido(Normal):

    def atualizar(self):
        self.dias_vendas -= 1

        aumento_qualidade = 2 if self.qualidade < 0 else 1
        nova_qualidade = self.qualidade + aumento_qualidade 

        self.qualidade = min(50, max(0, nova_qualidade))
        
class Sulfuras(Normal):

    def atualizar(self):
        self.qualidade = 80
        
class Ingressos_de_show(Normal):

    def atualizar(self):

        self.dias_vendas -= 1

        if self.dias_vendas < 0:

            self.qualidade = 0
            aumento_qualidade = 0 

        elif self.dias_vendas < 5:

            aumento_qualidade = 3

        elif self.dias_vendas < 10:

            aumento_qualidade = 2

        else:

            aumento_qualidade = 1

        self.qualidade = min(50, max(0, self.qualidade + aumento_qualidade))

