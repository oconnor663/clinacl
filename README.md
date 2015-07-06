clinacl
=======

A command line tool for playing with the [NaCl cryptography
library](http://nacl.cr.yp.to/). This is a toy, so please don't feed it
any important data.

Symmetric encryption example:

    $ plaintext="Release the hounds."
    $ key=$(./clinacl.py secretgen)
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

Public key signature example:

    $ signingkey=$(./clinacl.py signinggen)
    $ echo $signingkey
    95faf19820c827aae2959e01beb81195a14d23d70018d79c26976f027fc405ec
    $ verifykey=$(./clinacl.py verifygen $signingkey)
    $ echo $verifykey
    b83e67e7b5c2b35e09745bf559392e17dc960e18a39bec2adae8b97b5ab02fd9
    $ message="The truth, the whole truth, and nothing but the truth."
    $ echo message | ./clinacl.py sign $signingkey
    ec94d3a3c3aeac1d8361c4be719314f396815c7852706252698091034b42f75416bfafe203f61876d2f6185fd495ca656fe6fdb4a0b86ba9323efe77a8410c006d6573736167650a
    $ echo $message | ./clinacl.py sign $signingkey | ./clinacl.py verify $verifykey
    The truth, the whole truth, and nothing but the truth.
