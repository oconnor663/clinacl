#! /usr/bin/env python

import binascii
import docopt
import nacl.secret
import nacl.utils
from six import print_
import sys

__doc__ = """\
Usage:
    clinacl keygen
    clinacl encrypt <key> [--nonce <nonce>]
    clinacl decrypt <key>
"""


def to_hex(bytes):
    return binascii.hexlify(bytes).decode('ascii')


def from_hex(hex):
    return binascii.unhexlify(hex.strip())


def keygen():
    keybytes = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    keyhex = to_hex(keybytes)
    print_(keyhex)


def encrypt(hexkey, noncehex):
    keybytes = from_hex(hexkey.strip())
    if noncehex:
        noncebytes = from_hex(noncehex)
    else:
        noncebytes = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    secretbox = nacl.secret.SecretBox(keybytes)
    plainbytes = sys.stdin.buffer.read()
    cipherbytes = secretbox.encrypt(plainbytes, noncebytes)
    cipherhex = to_hex(cipherbytes)
    print_(cipherhex)


def decrypt(hexkey):
    keybytes = from_hex(hexkey.strip())
    secretbox = nacl.secret.SecretBox(keybytes)
    cipherhex = sys.stdin.read()
    cipherbytes = from_hex(cipherhex.strip())
    plainbytes = secretbox.decrypt(cipherbytes)
    sys.stdout.buffer.write(plainbytes)


def main():
    args = docopt.docopt(__doc__)
    if args['keygen']:
        keygen()
    elif args['encrypt']:
        encrypt(args['<key>'], args['<nonce>'])
    elif args['decrypt']:
        decrypt(args['<key>'])


if __name__ == '__main__':
    main()
