from loja.sistema import Loja
from estoque.armazem import Produto 

def test_item_normal_reduz_qualidade_e_dias_vendas():
    item = Produto("Normal", 5, 10)
    loja = Loja()
    loja.adicionar_produtos([item])
    
    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 4
    assert loja.produtos[0].qualidade == 9


def test_item_normal_vencido_degrada_duas_vezes_mais():
    item = Produto("Item Normal", -1, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == -2
    assert loja.produtos[0].qualidade == 8


def test_aged_brie_aumenta_qualidade():
    item = Produto("Aged Brie", 5, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 4
    assert loja.produtos[0].qualidade == 11


def test_aged_brie_vencido_aumenta_qualidade_duas_vezes():
    item = Produto("Aged Brie", -1, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == -2
    assert loja.produtos[0].qualidade == 12

def test_aged_brie_vencido_nao_ultrapassa_qualidade_50():
    item = Produto("Aged Brie", -1, 49)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].qualidade == 50

def test_sulfuras_nao_sofre_alteracoes():
    item = Produto("Sulfuras, Hand of Ragnaros", 5, 80)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 5
    assert loja.produtos[0].qualidade == 80


def test_passagem_backstage_com_mais_de_10_dias():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", 11, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 10
    assert loja.produtos[0].qualidade == 11


def test_passagem_backstage_com_10_dias():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", 10, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 9
    assert loja.produtos[0].qualidade == 12


def test_passagem_backstage_com_5_dias():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", 5, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 4
    assert loja.produtos[0].qualidade == 13


def test_passagem_backstage_com_0_dias():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", 0, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == -1
    assert loja.produtos[0].qualidade == 0


def test_passagem_backstage_vencida():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", -1, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == -2
    assert loja.produtos[0].qualidade == 0

def test_passagem_backstage_perto_do_show_nao_ultrapassa_qualidade_50():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", 5, 49)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].qualidade == 50

def test_item_normal_nao_fica_com_qualidade_negativa():
    item = Produto("Item Normal", 5, 0)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].qualidade == 0


def test_passagem_backstage_nao_ultrapassa_qualidade_50():
    item = Produto("Backstage passes to a TAFKAL80ETC concert", 5, 50)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].qualidade == 50

def test_item_conjurado_degrada_o_dobro():
    item = Produto("Conjured Mana Cake", 5, 10)
    loja = Loja()
    loja.adicionar_produtos([item])

    loja.atualizar_produtos()

    assert loja.produtos[0].dias_vendas == 4
    assert loja.produtos[0].qualidade == 8 