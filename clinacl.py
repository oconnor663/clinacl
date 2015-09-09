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
    clinacl keybase sign <signingkey>
    clinacl keybase verify
"""

NACL_SIG_LEN = 64


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


def keybase_sign(keyhex):
    signing_keybytes = from_hex(keyhex)
    signingkey = nacl.signing.SigningKey(signing_keybytes)
    verify_keybytes = signingkey.verify_key.encode()
    plainbytes = read_from_stdin()
    attached_sig = signingkey.sign(plainbytes)
    detatched_sig = attached_sig[:NACL_SIG_LEN]
    # This is the signature format currently used by Keybase's servers. See the
    # comments in keybase_verify().
    blob = {
        'body': {
            'payload': plainbytes,
            'key': b'\x01\x20' + verify_keybytes + b'\x0a',
            'sig': detatched_sig,
            'detached': True,
            'sig_type': 32,
            'hash_type': 10
        },
        'tag': 514,
        'version': 1,
    }
    sig_msgpack_bytes = umsgpack.packb(blob)
    sig_base64 = base64.b64encode(sig_msgpack_bytes)
    write_to_stdout(sig_base64)


def keybase_verify():
    # A Keybase NaCl signature is a Base64-encoded MessagePack blob containing
    # the payload, the signing KID, and the detatched signature bytes. We
    # decode, unpack, and then verify the signature. If it's valid, we print
    # the payload (which is usually a JSON blob).
    sig_base64 = sys.stdin.read()
    sig_msgpack_bytes = base64.b64decode(sig_base64)
    sig_obj = umsgpack.unpackb(sig_msgpack_bytes)
    keybytes_tagged = sig_obj['body']['key']
    # Keybase KIDs are just NaCl public keys type-tagged with two bytes at the
    # front and one byte in the back. Stripping these gives the key.
    keybytes = keybytes_tagged[2:-1]
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
    elif args['keybase']:
        if args['sign']:
            keybase_sign(args['<signingkey>'])
        elif args['verify']:
            keybase_verify()
    else:
        if args['sign']:
            sign(args['<signingkey>'])
        elif args['verify']:
            verify(args['<verifykey>'])


if __name__ == '__main__':
    main()
