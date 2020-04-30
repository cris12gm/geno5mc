from django.template import Library
from ..views import Errors

register = Library()

def errorGestionGene (error):
    if error == Errors.NOT_VALID:
        toPrint = "The provided ID is not a valid Gene ID or is not in our DB."
    elif error == Errors.NOT_ASSOCIATED:
        toPrint = "The provided Gene ID is not associated."
    return str(toPrint)
register.filter("errorGestionGene",errorGestionGene)