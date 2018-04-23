# -*- coding: utf-8 -*-
import math
def add(*numbers):
    sum = 0
    print type(numbers)
    for n in numbers:
        sum = sum + n * n
    return sum

add()