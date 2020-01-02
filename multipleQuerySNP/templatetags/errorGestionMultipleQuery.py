from django.template import Library
from ..views import Errors

register = Library()

def errorGestionMultipleQuery (error):
    if error == Errors.NOT_VALID:
        toPrint = "NotValid"
    elif error == Errors.NOT_ASSOCIATED:
        toPrint = "Not_associated"
    return str(toPrint)
    
register.filter("errorGestionMultipleQuery",errorGestionMultipleQuery)