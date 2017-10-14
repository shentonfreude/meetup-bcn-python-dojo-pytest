# -*- coding: utf-8 -*-

from gilded_rose import GildedRose
from item import Item


def get_gilded_items(test_cases):
    items = [test_case[0] for test_case in test_cases]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    return items


def validate(items, test_cases):
    for i, item in enumerate(items):
        assert items[i].name == test_cases[i][1].name
        assert items[i].sell_in == test_cases[i][1].sell_in
        assert items[i].quality == test_cases[i][1].quality


def test_normal():
    """Decrement sell_in and adjust quality.

    If sell_in <= 0: q = q - 2
    If sell_in > 0: q = q - 1
    """
    test_cases = [              # (before, after)
        (Item("+5 Dexterity Vest", 2, 4),
         Item("+5 Dexterity Vest", 1, 3)),
        (Item('+5 Dexterity Vest', 0, 0),
         Item('+5 Dexterity Vest', -1, 0)),
        (Item('+5 Dexterity Vest', 1, 0),
         Item('+5 Dexterity Vest', 0, 0)),
        (Item('+5 Dexterity Vest', 0, 1),
         Item('+5 Dexterity Vest', -1, 0)),
        (Item('+5 Dexterity Vest', -1, 42),  # test si<0 gets q decremented by 2
         Item('+5 Dexterity Vest', -2, 40)),
        (Item('+5 Dexterity Vest', 1, -1),
         Item('+5 Dexterity Vest', 0, -1)),  # VIOLATES SPEC, Q should be >= 0
        (Item('+5 Dexterity Vest', 1, 500),
         Item('+5 Dexterity Vest', 0, 499)),  # VIOLATES SPEC, Q should be <= 50
        (Item("ñoqui", 1, 42),     # test unicode, not part of spec, not TDD
         Item("ñoqui", 0, 41)),
    ]
    items = get_gilded_items(test_cases)
    validate(items, test_cases)


def test_sulfuras():
    """sell_in and quality never change."""
    test_cases = [              # (before, after)
        (Item("Sulfuras, Hand of Ragnaros", 2, 4),
         Item("Sulfuras, Hand of Ragnaros", 2, 4)),
        (Item("Sulfuras, Hand of Ragnaros", -1, -1),
         Item("Sulfuras, Hand of Ragnaros", -1, -1)),
    ]
    items = get_gilded_items(test_cases)
    validate(items, test_cases)


def test_aged_brie():
    """sell_in decrements, quality increments.

    if sell_in <= 0, q decrements by 2;
    else q decrements by 1
    """
    test_cases = [
        (Item('Aged Brie', 1, 1),
         Item('Aged Brie', 0, 2),),
        (Item('Aged Brie', 0, 1),
         Item('Aged Brie', -1, 3),),
    ]
    items = get_gilded_items(test_cases)
    validate(items, test_cases)


def test_backstage_pass():
    """sell_in decrements, quality increments until after event.

    if sellin <= 10, q =+ 2;
    elif sellin <= 5, q =+ 3;
    elif sellin < 0: q = 0;
    else sellin =+ 1
    """
    test_cases = [
        (Item('Backstage passes to a TAFKAL80ETC concert', 20, 10),  # normal
         Item('Backstage passes to a TAFKAL80ETC concert', 19, 11),),
        (Item('Backstage passes to a TAFKAL80ETC concert', 10, 12),  # si <= 10
         Item('Backstage passes to a TAFKAL80ETC concert', 9, 14),),
        (Item('Backstage passes to a TAFKAL80ETC concert', 5, 12),  # si <= 5
         Item('Backstage passes to a TAFKAL80ETC concert', 4, 15),),
        (Item('Backstage passes to a TAFKAL80ETC concert', -1, 42),  # si < 0
         Item('Backstage passes to a TAFKAL80ETC concert', -2, 0),),
        # Test last day, sell_in==1 -> sell_in==0
        (Item('Backstage passes to a TAFKAL80ETC concert', 1, 12),  # si <= 5
         Item('Backstage passes to a TAFKAL80ETC concert', 0, 15),),
        # After last day, becomes worthless
        (Item('Backstage passes to a TAFKAL80ETC concert', 0, 12),  # next si < 0
         Item('Backstage passes to a TAFKAL80ETC concert', -1, 0),),
    ]
    items = get_gilded_items(test_cases)
    validate(items, test_cases)
