# Cosmo Device Web API
Documentation for those whom wish to use the web api in apps

#### What is the Web Api?
The web API is a HTTP based request system that allows the client to interact, setup and 
control their cosmo-home device. The API is used in discovery, and communication and is primarily
designed for the setup process and controlling the CosmoHome from our Consumer App. However, this
api can be used for development, and other app purposes such as scripts.

##### Implementations
There are no Implemtatons of API Wrappers for the API Yet. A Java/Android and a Python are 
planned in the future.

-----

#### The Protocol
##### Request Format
The Cosmo Web api uses the HTTP Protocol using the following methods:
 - `GET` (For Retrieving Data)
 - `POST` (For Setting Data)
 - `PUT` (For sending commands)
 
Using Multiple HTTP methods to send commands, allows the api to a single endpoint, with multiple
methods, giving the api a smoother look.

Request Data is provided in 4 ways:

 - GET Arguments
 - POST Form Arguments
 - POST Json Data
 - In Url Arguments
 
 Authentication Tokens are used to restrict access to most endpoints. This allows the customers
 product to remain secure. 
 The Token itself is sent with each request within the `Authentication` Header in 
 this such manner:
 
 `Authentication: Basic <token>`
 
##### Response Format

Once a request is send, the API should response (No shit sherlock). 
The Response is contained in the HTTP response body in the JSON format. 

**JSON Response Table**

| Key | Type | Description |
| --- | ---- | ----------- |
| `status` | object | Request status information |
| `status.success` | boolean | Whether the Request was successful as a simple true/false |
| `status.code` | int | A HTTP status code of the request e.g. 200 |
| `status.msg` | string | A Message respecting the status code of the request e.g. Not Found |
| `data` | object | Response Data |

The Response Object contains two main Objects. The `status` object, containing the request 
response status and the `data` object the contains request response body.

When the `status.success` is `true` we are confiable able to presume that the request has been
successfully. In this case, you are able to use the `data` object has per endpoint


**Handling Response Errors**

If the `status.success` is `false` something has gone wrong. This may be client error or 
server error. The nature of the error can be found within the `status.code` error. These
correspond with the [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status). 
For Example a `200` is a success response and a `400` is a Bad Request (Client Error) and a
 `500` is a Server Error. The `status.msg` is a message that corosponds with the `status.code` 
and can be used to display and error, *or to understand what the status code means if your a lazy*

An Additional Error Information may be provided though `data.error` however is optional and
may not be provided

To standardize how errors are delivered to the user through API Wrappers we suggest you use this
format: `[{data.code}]{data.msg}: {data.error}`

##### API Location
By Default the API is hosted on port `12890` and is hosted on `0.0.0.0` so all devices on the local
network can access. We do not recommend port forwarding this port due to security reasons.

Each Section of the API (e.g. Device Info) is under the first url directory (e.g. /info)

-----
#### Endpoints

##### Device Info

###### /info

**Required Params:** None

**Response Params:** None

| Key | Type | Description |
| --- | ---- | ----------- |
| `name` | string(null) | Device Formal Name |
| `serial` | string | Device Serial Number |
| `ip` | string | Local Network IP |
| `setup` | boolean | Is the devices registered as setup |

