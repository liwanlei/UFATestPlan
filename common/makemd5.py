import hashlib


def make_md5(make):
    md5make = hashlib.new('md5', make.encode('utf-8')).hexdigest()
    return md5make


def checkout_md5(check_md5, yuan_md5):
    md5check = hashlib.new('md5', check_md5.encode('utf-8')).hexdigest()
    if yuan_md5 == md5check:
        return True
    else:
        return False
