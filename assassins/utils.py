from assassins.models import Player, Quote
from assassins.addison_encrypt import decrypt

def get_quote():
    # Get random quote
    quote = Quote.objects.order_by('?')[0]
    return quote


def get_sunetid(request):
    # URL string had encrypted sunetid in it
    if 'usr' in request.GET:
        # Get sunetid from URL
        encrypted_sunetid = request.GET.get('usr')

        # Decrypt it
        sunetid = decrypt_id(encrypted_sunetid)

        # Store it in the session
        request.session['usr'] = sunetid

        return sunetid

    # sunetid is saved in the session
    if 'usr' in request.session:
        return request.session['usr']

    # No sunetid found
    return None


def decrypt_id(encrypted_id):
    id_minus_padding = encrypted_id[:-10]
    #sunetid = rot13(id_minus_padding)
    sunetid = decrypt(id_minus_padding, "serrassic")
    return sunetid


def rot13(s):
    chars = "abcdefghijklmnopqrstuvwxyz"
    trans = chars[13:]+chars[:13]
    rot_char = lambda c: trans[chars.find(c)] if chars.find(c)>-1 else c
    return ''.join( rot_char(c) for c in s ) 
