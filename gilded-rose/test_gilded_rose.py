# -*- coding: utf-8 -*-

from gilded_rose import GildedRose
from item import Item


def test_normal():
    test_cases = [              # (before, after)
        (Item("+5 Dexterity Vest", 2, 4),
         Item("+5 Dexterity Vest", 1, 3)),
        (Item('normal', 0, 0),
         Item('normal', -1, 0)),
        (Item('normal', 1, 0),
         Item('normal', 0, 0)),
        (Item('normal', 0, 1),
         Item('normal', -1, 0)),
        (Item('normal', 1, -1),
         Item('normal', 0, -1)),  # VIOLATES SPEC, Q should be >= 0
        (Item('normal', 1, 500),
         Item('normal', 0, 499)),  # VIOLATES SPEC, Q should be <= 50
        (Item("ñoqui", 1, 42),
         Item("ñoqui", 0, 41)),
    ]
    items = [test_case[0] for test_case in test_cases]
    guilded_rose = GildedRose(items)
    guilded_rose.update_quality()
    for i, item in enumerate(items):
        assert items[i].name == test_cases[i][1].name
        assert items[i].sell_in == test_cases[i][1].sell_in
        assert items[i].quality == test_cases[i][1].quality



# def test_sulfurus_never_changes():
#     items = [Item("Sulfuras, Hand of Ragnaros","normal", 1, -1)]
#     gilded_rose = GildedRose(items)
#     gilded_rose.update_quality()
#     assert items[0].name == 'normal'
#     assert items[0].sell_in == 0
#     assert items[0].quality == 0  # FAILS

