# Manual Tests
Once deployed run the following statements to get the expected response.

### Conversation Update
There is no command but when a update happens the result should be the following:
```text
Conversation Update: Added person was {Name}
```
If there were no members added it will be
```text
Conversation Update: No members added
```

### Synchronous Response
Test
```text
synchronous
```
Response
```text
Synchronous Test: synchronous
```

### Asynchronous Response
Test
```text
asynchronous
```
Response
```text
Synchronous Test: asynchronous
```

### Personal Message
If this is in a group chat you should get a personal message from the bot. 

Test
```text
personal
```
Response
```text
Personal Test: personal
```

### Get Members

Test
```text
members
```
Personal response
```text
Conversation: [{"id":"29:1S..."}]; Activity: [{"id":"29:1SPw4..."}]
```

### Post Image
Test
```text
image
```
The bot should respond with a cat image

### Get Members

Test
```text
delete
```
Response, which should be delete after 5 seconds (doesn't work in all channels)
```text
Delete Test: delete
```