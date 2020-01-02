from django.template import Library
from ..views import Errors

register = Library()

def errorGestionMultipleQuery (errors):
    toPrintNotAssociated = "The following provided SNP IDs are not associated:"
    toPrintNotValid = "The following provided SNP IDs are not valid:"
    notAssociated = False
    notValid = False

    for snp in errors:
        error = errors[snp]
        if error == Errors.NOT_VALID:
            toPrintNotValid = toPrintNotValid+"\n"+snp
            notValid = True
        elif error == Errors.NOT_ASSOCIATED:
            toPrintNotAssociated = toPrintNotAssociated+"\n"+snp
            notAssociated = True
    if notAssociated:
        toPrint = toPrintNotAssociated
        if notValid:
            toPrint = toPrint+"\n"+toPrintNotValid
    elif notValid:
        toPrint = toPrintNotValid

    return str(toPrint)
    
register.filter("errorGestionMultipleQuery",errorGestionMultipleQuery)