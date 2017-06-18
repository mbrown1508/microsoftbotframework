# Response Object
The response object is used whenever responding to the Microsoft Bot API. It is extended by all of the conversation operations and the state operations in the future.

The Response Object takes the following arguments:

* app_client_id - You can set app_client_id via arguments although it is recomended you use environemnt vars to do so.
* app_client_secret - You can set app_client_secret via arguments although it is recomended you use environemnt vars to do so.
* auth - auth is enabled by default if app_client_id and app_client_secret are enabled. auth can be used to disable it. 
* redis_uri - This argument enables you to set the redis_uri to use to cache the jwt token
* http_proxy - This enables you to set a http_proxy for the response.
* https_proxy - This enables you to set a https_proxy for the response.