# Microsoft Bot Framework
Microsoft Bot Framework is a wrapper for the Microsoft Bot API by Microsoft

## To run this app
1. Create a microsoft chatbot - https://dev.botframework.com/bots
2. Generate <Microsoft App ID> and <Microsoft App Secret> then update config.ini
```
[DEFAULT]
app_client_id: <Microsoft App ID>
app_client_secret: <Microsoft App Secret>
```
3. in shell prompt run
```sh
sudo pip install requirements.txt
```
4. python main.py
5. to use celery install and configure celery and run
```sh
celery -A microsoftbotframework.msbot.celery worker --loglevel=info
```