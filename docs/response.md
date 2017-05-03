# The Response Object
The response object is created by passing it the message recieved and then calling Response.reply_to_activity(message).
```python
response = Response(message)
response.reply_to_activity('This is my response.')
```
You don't have to pass the message to the Response object but you will have to set all of the required vars before you respond to microsoft.

If you haven't added 'Microsoft App ID' and 'Microsoft App Secret' to the global vars you will have to pass them to the response as follows.
```python
response = Response(message, microsoft_app_id='Microsoft App ID', microsoft_app_secret='Microsoft App Secret')
response.reply_to_activity('This is my response.')
```
