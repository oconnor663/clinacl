#! /usr/bin/env python

import binascii
import docopt
import nacl.secret
import nacl.signing
import nacl.utils
from six import print_
import sys

__doc__ = """\
Usage:
    clinacl secretgen
    clinacl encrypt <secretkey> [--nonce <nonce>]
    clinacl decrypt <secretkey>
    clinacl signinggen
    clinacl verifygen <signingkey>
    clinacl sign <signingkey>
    clinacl verify <verifykey>
"""


def to_hex(bytes):
    return binascii.hexlify(bytes).decode('ascii')


def from_hex(hex):
    return binascii.unhexlify(hex.strip())


def secretgen():
    keybytes = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    print_(to_hex(keybytes))


def encrypt(keyhex, noncehex):
    keybytes = from_hex(keyhex.strip())
    if noncehex:
        noncebytes = from_hex(noncehex)
    else:
        noncebytes = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    secretbox = nacl.secret.SecretBox(keybytes)
    plainbytes = sys.stdin.buffer.read()
    cipherbytes = secretbox.encrypt(plainbytes, noncebytes)
    cipherhex = to_hex(cipherbytes)
    print_(cipherhex)


def decrypt(keyhex):
    keybytes = from_hex(keyhex.strip())
    secretbox = nacl.secret.SecretBox(keybytes)
    cipherhex = sys.stdin.read()
    cipherbytes = from_hex(cipherhex.strip())
    plainbytes = secretbox.decrypt(cipherbytes)
    sys.stdout.buffer.write(plainbytes)


def signinggen():
    signingkey = nacl.signing.SigningKey.generate()
    print_(to_hex(signingkey.encode()))


def verifygen(keyhex):
    keybytes = from_hex(keyhex)
    signingkey = nacl.signing.SigningKey(keybytes)
    print_(to_hex(signingkey.verify_key.encode()))


def sign(keyhex):
    keybytes = from_hex(keyhex)
    signingkey = nacl.signing.SigningKey(keybytes)
    plainbytes = sys.stdin.buffer.read()
    attached_sig = signingkey.sign(plainbytes)
    print_(to_hex(attached_sig))


def verify(keyhex):
    keybytes = from_hex(keyhex)
    verifykey = nacl.signing.VerifyKey(keybytes)
    attached_sig_hex = sys.stdin.read()
    attached_sig_bytes = from_hex(attached_sig_hex)
    plainbytes = verifykey.verify(attached_sig_bytes)
    sys.stdout.buffer.write(plainbytes)


def main():
    args = docopt.docopt(__doc__)
    if args['secretgen']:
        secretgen()
    elif args['encrypt']:
        encrypt(args['<secretkey>'], args['<nonce>'])
    elif args['decrypt']:
        decrypt(args['<secretkey>'])
    elif args['signinggen']:
        signinggen()
    elif args['verifygen']:
        verifygen(args['<signingkey>'])
    elif args['sign']:
        sign(args['<signingkey>'])
    elif args['verify']:
        verify(args['<verifykey>'])


if __name__ == '__main__':
    main()
