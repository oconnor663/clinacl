#! /bin/bash

set -e
set -o pipefail

cd $(dirname "$BASH_SOURCE")

venv_two=/tmp/clinacl_venv_python2
if [[ ! -e "$venv_two" ]] ; then
  echo === creating Python 2 virtualenv ===
  virtualenv -p python2 "$venv_two"
  (source "$venv_two/bin/activate" && pip install .)
fi

venv_three=/tmp/clinacl_venv_python3
if [[ ! -e "$venv_three" ]] ; then
  echo === creating Python 3 virtualenv ===
  virtualenv -p python3 "$venv_three"
  (source "$venv_three/bin/activate" && pip install .)
fi

runtests() {
  key=$(clinacl secretgen)
  nonce=$(head -c 24 /dev/zero | xxd -p)
  echo with nonce | clinacl encrypt $key --nonce $nonce | clinacl decrypt $key
  echo without nonce | clinacl encrypt $key | clinacl decrypt $key

  signingkey=$(clinacl signinggen)
  verifykey=$(clinacl verifygen $signingkey)
  echo verified | clinacl sign $signingkey | clinacl verify $verifykey

  link='g6Rib2R5hqhkZXRhY2hlZMOpaGFzaF90eXBlCqNrZXnEIwEgb0QEGch1mSRBwXnmm+ElpwHWSpGF4Y5wGq9Wz1BEOsYKp3BheWxvYWTFA5x7ImJvZHkiOnsiZGV2aWNlIjp7ImlkIjoiZjRmZTNkMWYwYzgxM2QxMzBiZDUwNTllMWFkMzI4MTgiLCJzdGF0dXMiOjIsInR5cGUiOiJkZXNrdG9wIn0sImtleSI6eyJlbGRlc3Rfa2lkIjoiMDEwMTA0ZTcyNDM2MmU3YmE2NjMzOTgwYTYyNTdmMDQzZjdjM2Q4NzMzNTUwNTk0YTc5MmFhY2Y2YzZkNDY3N2RkOTQwYSIsImhvc3QiOiJrZXliYXNlLmlvIiwia2lkIjoiMDEyMDZmNDQwNDE5Yzg3NTk5MjQ0MWMxNzllNjliZTEyNWE3MDFkNjRhOTE4NWUxOGU3MDFhYWY1NmNmNTA0NDNhYzYwYSIsInVpZCI6ImJmNjUyNjZkMGQ4ZGYzYWQ1ZDFiMzY3ZjU3OGU2ODE5IiwidXNlcm5hbWUiOiJyYWxwaCJ9LCJyZXZva2UiOnsia2lkcyI6WyIwMTIwNWVkYzAwYTE3M2E1NDMyNGFkNTIzN2M5MzlhNmFiYmY5ZmY2MTIxMDk0NjY4OWRhMWQ3MjEzMjlhY2RhYjlkZTBhIiwiMDEyMWE1M2MyMzcxMGUxODUwYTMyODJhMWFhZDZmNTM4NjczZDA3OGMxMTJmMWYyM2UyYjE3MTE5NDFiZTFjM2RkNGIwYSJdfSwidHlwZSI6InJldm9rZSIsInZlcnNpb24iOjF9LCJjbGllbnQiOnsibmFtZSI6ImtleWJhc2UuaW8gZ28gY2xpZW50IiwidmVyc2lvbiI6IjAuMS43In0sImN0aW1lIjoxNDI5NjUxNDk5LCJleHBpcmVfaW4iOjMxNTM2MDAwMCwibWVya2xlX3Jvb3QiOnsiY3RpbWUiOjE0Mjk2NTEzOTIsImhhc2giOiIyZGVhODhjMjNiYjc0OWY5ZGQ5OWNlYjAyYzQ2MGM2NTgxYzc4NjVhMmFiZTU0Y2ZkNDVmZmU2OWZlODA0MWFjY2UyOWJmOGMwMzcxZjgwZGZlZWMwNWY4NmY5MWVhYzMxN2RhY2JjMmU1MDM2NmIxNGJkOTg2ZjZhMjVmNDZhMiIsInNlcW5vIjoyNTd9LCJwcmV2IjoiNTgwOGQ2OTRlOWFjNDFhMDEwZjMwNTk5YmRmNGM4MDdlNzc4Mjg2YWYyMmZkNWY0NWExMmJjZWM3NDBjMGEzNiIsInNlcW5vIjoxNSwidGFnIjoic2lnbmF0dXJlIn2jc2lnxEAaomeO/0vh2uEtIo1HQ6lQW07IKoSqfLyYnpbbks3tYxo+a7VXMC/NgzdUExivyhira4cUzk43Q7EboDF2EDEMqHNpZ190eXBlIKN0YWfNAgKndmVyc2lvbgE='
  echo $link | clinacl keybase
  echo
}

echo === testing Python 2 ===
(source "$venv_two/bin/activate" && runtests)

echo === testing Python 3 ===
(source "$venv_three/bin/activate" && runtests)
