#! /usr/bin/env python

import base64
import binascii
import docopt
import nacl.secret
import nacl.signing
import nacl.utils
from six import print_
import sys
import umsgpack

__doc__ = """\
Usage:
    clinacl secretgen
    clinacl encrypt <secretkey> [--nonce <nonce>]
    clinacl decrypt <secretkey>
    clinacl signinggen
    clinacl verifygen <signingkey>
    clinacl sign <signingkey>
    clinacl verify <verifykey>
    clinacl keybase
"""


def to_hex(bytes):
    return binascii.hexlify(bytes).decode('ascii')


def from_hex(hex):
    return binascii.unhexlify(hex.strip())


def read_from_stdin():
    # Python 2 has no sys.stdin.buffer.
    if sys.version_info.major == 2:
        return sys.stdin.read()
    else:
        return sys.stdin.buffer.read()


def write_to_stdout(bytes):
    # Python 2 has no sys.stdout.buffer.
    if sys.version_info.major == 2:
        return sys.stdout.write(bytes)
    else:
        return sys.stdout.buffer.write(bytes)


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
    plainbytes = read_from_stdin()
    cipherbytes = secretbox.encrypt(plainbytes, noncebytes)
    cipherhex = to_hex(cipherbytes)
    print_(cipherhex)


def decrypt(keyhex):
    keybytes = from_hex(keyhex.strip())
    secretbox = nacl.secret.SecretBox(keybytes)
    cipherhex = sys.stdin.read()
    cipherbytes = from_hex(cipherhex.strip())
    plainbytes = secretbox.decrypt(cipherbytes)
    write_to_stdout(plainbytes)


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
    plainbytes = read_from_stdin()
    attached_sig = signingkey.sign(plainbytes)
    print_(to_hex(attached_sig))


def verify(keyhex):
    keybytes = from_hex(keyhex)
    verifykey = nacl.signing.VerifyKey(keybytes)
    attached_sig_hex = sys.stdin.read()
    attached_sig_bytes = from_hex(attached_sig_hex)
    plainbytes = verifykey.verify(attached_sig_bytes)
    write_to_stdout(plainbytes)


def keybase():
    sig_base64 = sys.stdin.read()
    sig_msgpack_bytes = base64.b64decode(sig_base64)
    sig_obj = umsgpack.unpackb(sig_msgpack_bytes)
    keybytes_tagged = sig_obj['body']['key']
    # Keybase KIDs are type-tagged with two bytes at the front and
    # one byte in the back.
    keybytes = keybytes_tagged[2:34]
    verifykey = nacl.signing.VerifyKey(keybytes)
    detatched_sig_bytes = sig_obj['body']['sig']
    sig_payload = sig_obj['body']['payload']
    attached_sig_bytes = detatched_sig_bytes + sig_payload
    write_to_stdout(verifykey.verify(attached_sig_bytes))


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
    elif args['keybase']:
        keybase()


if __name__ == '__main__':
    main()
