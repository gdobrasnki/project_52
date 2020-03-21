#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random

from .data import FOOD, SEX, WANTS

# TODO: depending on the source file, there might be a better
#   way to achieve this without these two functions


def get_names(source):
    """Retrieve all the names from the given dataset and put them
    into a list.

    Args:
        source: input dataset

    Returns:
        list of names
    """
    names = [row["name"] for row in source]
    return sorted(names)


def get_items(source):
    """Retrieve all the items from the given dataset and put them
    into a list.

    Args:
        source: input dataset

    Returns:
        list of items
    """
    items = [el for el in source]
    return sorted(items)


# TODO: this might be a proper class instead of a function

def make_person():
    person = "<p>age:{}</p><p>sex:{}</p><p>needs:{}</p><p>wants:{}<p>"
    age = random.randint(55, 95)
    sex = random.choice(SEX)
    needs = random.choice(FOOD)
    wants = [random.choice(WANTS) for _ in range(2)]

    person = person.format(age, sex, needs, ",".join(wants))
    person += '<a href="http://google.com">I can help in 4 hours or less</a>'
    person += '<div class="uber-google-maps-info-window-field"><a href="http://google.com">I can help in 12 hours or less</a></div>'

    return person

