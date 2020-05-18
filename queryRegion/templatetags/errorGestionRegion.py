from django.template import Library
from ..views import Errors

register = Library()

def errorGestionRegion (error):
    toPrint = ""
    if error == Errors.VERY_LONG:
        toPrint = "Your region is too long to be analysed (1kb), please enter a shorter region."
    elif error == Errors.START_END:
        toPrint = "The start coordinate is greater than the end coordinate."
    return str(toPrint)
register.filter("errorGestionRegion",errorGestionRegion)