from django.template import Library
from ..views import Errors

register = Library()

def errorGestionGene (error):
    if error == Errors.NOT_VALID:
        toPrint = "The provided ID is not a valid Gene ID, please try a new one"
    elif error == Errors.NOT_ASSOCIATED:
        toPrint = "The provided Gene ID is not associated or is not a valid Gene ID, please try a new one"
    return str(toPrint)
register.filter("errorGestionGene",errorGestionGene)