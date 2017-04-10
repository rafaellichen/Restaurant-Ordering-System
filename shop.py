import pandas
import numpy

def check_quantity(input):
    if input.isdigit():
        if int(input) >0:
            return True
    else:
        return False