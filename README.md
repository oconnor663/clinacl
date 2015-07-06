clinacl
=======

A command line tool for playing with the [NaCl cryptography
library](http://nacl.cr.yp.to/). This is a toy, so please don't feed it
any important data.

Example:

    $ plaintext="Release the hounds."
    $ key=$(./clinacl.py keygen)
    $ echo $key
    5c6f65e7a9c2a8cb8107dcd0601a02285895e7c9dd60450f682003f82bd3aa39
    $ nonce="deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    $ echo $nonce
    deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
    $ ciphertext=$(echo $plaintext | ./clinacl.py encrypt $key --nonce $nonce)
    $ echo $ciphertext
    deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef52ab40194806e3c4dec342a6aebf456bde3d50773ec977b8bcd3db3f07c86391d778ba97
    $ echo $ciphertext | ./clinacl.py decrypt $key
    Release the hounds.
