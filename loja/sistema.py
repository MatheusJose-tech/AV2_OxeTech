from estoque.armazem import Normal
from estoque.constante import PRODUTOS

class Loja:  

    def __init__(self):
        self.produtos = []


    def adicionar_produtos(self, produtos):

        for produto in produtos:
            classe_produto = PRODUTOS.get(produto.nome, Normal)

            novo_produto = classe_produto(
                produto.nome,
                produto.dias_vendas,
                produto.qualidade
            )

            self.produtos.append(novo_produto)

    def atualizar_produtos(self):

        for produto in self.produtos:
            produto.atualizar()
