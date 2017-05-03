apt-get install build-essential libssl-dev libffi-dev python-dev

use python3-dev if using python3-dev

pip install cryptography PyJWT

*note remove cryptography and PyJWT from setup.py
*they may want to add verify_jwt_signature=False if they are on their local


#### Enable Cryptography
This is a optional requriement as it can be hard to install the crpytography library
```sh
pip install git+git://github.com/jpadilla/pyjwt@master
pip isntall cryptography
```
