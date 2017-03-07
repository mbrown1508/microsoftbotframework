celery -A microsoftbotframework.msbot.celery worker --loglevel=info

# Microsoft-chatbot
Microsoft chatbot build using NLTK-Chatbot and django

## To run this app
1. Create a microsoft chatbot - [https://dev.botframework.com/bots](https://dev.botframework.com/bots)
2. Generate <Microsoft App ID> and <Microsoft App Secret> then update config.ini
  ```python
  [DEFAULT]
  app_client_id: <Microsoft App ID>
  app_client_secret: <Microsoft App Secret>
  ```
3. in shell prompt run
  ```sh
  sudo pip install requirements.txt
  ```
4. run main.py
5. to use celery install and configure celery and run
  ```sh
  celery -A microsoftbotframework.msbot.celery worker --loglevel=info
  ```