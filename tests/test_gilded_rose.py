from glided_rose import Item, GildedRose


def test_item_normal_reduz_qualidade_e_sell_in():
    item = Item("Item Normal", 5, 10)
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == 4
    assert item.quality == 9


def test_item_normal_vencido_degrada_duas_vezes_mais():
    item = Item("Item Normal", -1, 10)
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == -2
    assert item.quality == 8


def test_aged_brie_aumenta_qualidade():
    item = Item("Aged Brie", 5, 10)
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == 4
    assert item.quality == 11


def test_aged_brie_vencido_aumenta_qualidade_duas_vezes():
    item = Item("Aged Brie", -1, 10)
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == -2
    assert item.quality == 12


def test_sulfuras_nao_sofre_alteracoes():
    item = Item("Sulfuras, Hand of Ragnaros", 5, 80)
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == 5
    assert item.quality == 80


def test_passagem_backstage_com_mais_de_10_dias():
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        11,
        10,
    )
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == 10
    assert item.quality == 11


def test_passagem_backstage_com_10_dias():
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        10,
        10,
    )
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == 9
    assert item.quality == 12


def test_passagem_backstage_com_5_dias():
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        5,
        10,
    )
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == 4
    assert item.quality == 13


def test_passagem_backstage_com_0_dias():
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        0,
        10,
    )
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == -1
    assert item.quality == 0


def test_passagem_backstage_vencida():
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        -1,
        10,
    )
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.sell_in == -2
    assert item.quality == 0


def test_item_normal_nao_fica_com_qualidade_negativa():
    item = Item("Item Normal", 5, 0)
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.quality == 0


def test_passagem_backstage_nao_ultrapassa_qualidade_50():
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        5,
        50,
    )
    gilded_rose = GildedRose([item])

    gilded_rose.att()

    assert item.quality == 50
