from django.template import Library
from ..views import Errors

register = Library()

def errorGestionSNP (error):
    toPrint = ""
    if error == Errors.NOT_VALID:
        toPrint = "The provided ID is not a valid SNP ID, please try a new one"
    elif error == Errors.NOT_ASSOCIATED:
        toPrint = "The provided SNP ID is not associated"
    return str(toPrint)
register.filter("errorGestionSNP",errorGestionSNP)