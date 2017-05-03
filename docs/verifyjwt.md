# Verify JWT Token
When the message is posted to your server from microsoft the only way to be sure it came from microsoft is to verify the signature on the JWT Token in the header. To do this we need to install the PyJWT and cryptography libraries. This can be a little tricky on some platforms.

## Before you Start
On your local dev machine using the emulator you will have to disable the JWT validation. Pass the verify_jwt_signature argument to the MsBot object.
```python
bot = MsBot(verify_jwt_signature=False)
```

## Ubuntu Install
Install the required python libs. You can remove python-dev of python3-dev depending on which version of python you are using. or install both.
```sh
apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev
```

You should then be able to install cryptography
```sh
pip install cryptography PyJWT
```

## Windows Install
On windows you should just be able to use the following pip command.
You should then be able to install cryptography
```sh
pip install cryptography PyJWT
```

## Heroku Setup
To enable the JWT validation on Heorku update the requirements.txt to include the cryptography and PyJWT libs.

```
microsoftbotframework
cryptography
PyJWT
```
