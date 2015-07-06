clinacl
=======

A command line tool for playing with the [NaCl cryptography
library](http://nacl.cr.yp.to/). This is a toy, so please don't feed it
any important data.

The easiest way to install is to run

    pip install .

inside the project directory. You can use a
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to
avoid needing root permissions and dumping crap in your system
directories. You can also use pip's `--user` flag to install in your
home dir, if you add `~/.local/bin` to your `PATH`.

Symmetric encryption example:

    $ plaintext="Release the hounds."
    $ key=$(clinacl secretgen)
    $ echo $key
    5c6f65e7a9c2a8cb8107dcd0601a02285895e7c9dd60450f682003f82bd3aa39
    $ nonce="deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    $ echo $nonce
    deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
    $ ciphertext=$(echo $plaintext | clinacl encrypt $key --nonce $nonce)
    $ echo $ciphertext
    deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef52ab40194806e3c4dec342a6aebf456bde3d50773ec977b8bcd3db3f07c86391d778ba97
    $ echo $ciphertext | clinacl decrypt $key
    Release the hounds.

Public key signature example:

    $ signingkey=$(clinacl signinggen)
    $ echo $signingkey
    95faf19820c827aae2959e01beb81195a14d23d70018d79c26976f027fc405ec
    $ verifykey=$(clinacl verifygen $signingkey)
    $ echo $verifykey
    b83e67e7b5c2b35e09745bf559392e17dc960e18a39bec2adae8b97b5ab02fd9
    $ message="The truth, the whole truth, and nothing but the truth."
    $ echo message | clinacl sign $signingkey
    ec94d3a3c3aeac1d8361c4be719314f396815c7852706252698091034b42f75416bfafe203f61876d2f6185fd495ca656fe6fdb4a0b86ba9323efe77a8410c006d6573736167650a
    $ echo $message | clinacl sign $signingkey | clinacl verify $verifykey
    The truth, the whole truth, and nothing but the truth.

Verifying a Keybase sigchain link:

    $ link="g6Rib2R5hqhkZXRhY2hlZMOpaGFzaF90eXBlCqNrZXnEIwEgb0QEGch1mSRBwXnmm+ElpwHWSpGF4Y5wGq9Wz1BEOsYKp3BheWxvYWTFA5x7ImJvZHkiOnsiZGV2aWNlIjp7ImlkIjoiZjRmZTNkMWYwYzgxM2QxMzBiZDUwNTllMWFkMzI4MTgiLCJzdGF0dXMiOjIsInR5cGUiOiJkZXNrdG9wIn0sImtleSI6eyJlbGRlc3Rfa2lkIjoiMDEwMTA0ZTcyNDM2MmU3YmE2NjMzOTgwYTYyNTdmMDQzZjdjM2Q4NzMzNTUwNTk0YTc5MmFhY2Y2YzZkNDY3N2RkOTQwYSIsImhvc3QiOiJrZXliYXNlLmlvIiwia2lkIjoiMDEyMDZmNDQwNDE5Yzg3NTk5MjQ0MWMxNzllNjliZTEyNWE3MDFkNjRhOTE4NWUxOGU3MDFhYWY1NmNmNTA0NDNhYzYwYSIsInVpZCI6ImJmNjUyNjZkMGQ4ZGYzYWQ1ZDFiMzY3ZjU3OGU2ODE5IiwidXNlcm5hbWUiOiJyYWxwaCJ9LCJyZXZva2UiOnsia2lkcyI6WyIwMTIwNWVkYzAwYTE3M2E1NDMyNGFkNTIzN2M5MzlhNmFiYmY5ZmY2MTIxMDk0NjY4OWRhMWQ3MjEzMjlhY2RhYjlkZTBhIiwiMDEyMWE1M2MyMzcxMGUxODUwYTMyODJhMWFhZDZmNTM4NjczZDA3OGMxMTJmMWYyM2UyYjE3MTE5NDFiZTFjM2RkNGIwYSJdfSwidHlwZSI6InJldm9rZSIsInZlcnNpb24iOjF9LCJjbGllbnQiOnsibmFtZSI6ImtleWJhc2UuaW8gZ28gY2xpZW50IiwidmVyc2lvbiI6IjAuMS43In0sImN0aW1lIjoxNDI5NjUxNDk5LCJleHBpcmVfaW4iOjMxNTM2MDAwMCwibWVya2xlX3Jvb3QiOnsiY3RpbWUiOjE0Mjk2NTEzOTIsImhhc2giOiIyZGVhODhjMjNiYjc0OWY5ZGQ5OWNlYjAyYzQ2MGM2NTgxYzc4NjVhMmFiZTU0Y2ZkNDVmZmU2OWZlODA0MWFjY2UyOWJmOGMwMzcxZjgwZGZlZWMwNWY4NmY5MWVhYzMxN2RhY2JjMmU1MDM2NmIxNGJkOTg2ZjZhMjVmNDZhMiIsInNlcW5vIjoyNTd9LCJwcmV2IjoiNTgwOGQ2OTRlOWFjNDFhMDEwZjMwNTk5YmRmNGM4MDdlNzc4Mjg2YWYyMmZkNWY0NWExMmJjZWM3NDBjMGEzNiIsInNlcW5vIjoxNSwidGFnIjoic2lnbmF0dXJlIn2jc2lnxEAaomeO/0vh2uEtIo1HQ6lQW07IKoSqfLyYnpbbks3tYxo+a7VXMC/NgzdUExivyhira4cUzk43Q7EboDF2EDEMqHNpZ190eXBlIKN0YWfNAgKndmVyc2lvbgE="
    $ echo $link | clinacl keybase
    {"body":{"device":{"id":"f4fe3d1f0c813d130bd5059e1ad32818","status":2,"type":"desktop"},"key":{"eldest_kid":"010104e724362e7ba6633980a6257f043f7c3d8733550594a792aacf6c6d4677dd940a","host":"keybase.io","kid":"01206f440419c875992441c179e69be125a701d64a9185e18e701aaf56cf50443ac60a","uid":"bf65266d0d8df3ad5d1b367f578e6819","username":"ralph"},"revoke":{"kids":["01205edc00a173a54324ad5237c939a6abbf9ff61210946689da1d721329acdab9de0a","0121a53c23710e1850a3282a1aad6f538673d078c112f1f23e2b1711941be1c3dd4b0a"]},"type":"revoke","version":1},"client":{"name":"keybase.io go client","version":"0.1.7"},"ctime":1429651499,"expire_in":315360000,"merkle_root":{"ctime":1429651392,"hash":"2dea88c23bb749f9dd99ceb02c460c6581c7865a2abe54cfd45ffe69fe8041acce29bf8c0371f80dfeec05f86f91eac317dacbc2e50366b14bd986f6a25f46a2","seqno":257},"prev":"5808d694e9ac41a010f30599bdf4c807e778286af22fd5f45a12bcec740c0a36","seqno":15,"tag":"signature"}
