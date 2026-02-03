# Eventdebugger Manual

The Eventdebugger allows to listen to the internal event traffic. It also allows to send own events and queries.

This works by communicating with the build-in application web server and its websocket by exchanging json objects.

Basically each tool, which can communicate via websocket, can generate these debug messages.

E.g. a Chrome browser extension, which allows predefined messages and an easy handling, would be the [Browser WebSocket Client](https://chromewebstore.google.com/detail/browser-websocket-client/mdmlhchldhfnfnkfmljgeinlffmdgkjo).

The websocket, where all these tools needs to connect to would be `ws://<your_host><:your_port>/ws`

After connect, the tool needs to send a defined message to become registered as debugging connection:

```
{
  "type": "_join",
  "config": {
    "name": "wasdebugger"
  }
}
```

After this the debugger can send events and queries.

## Send Events

```
{
  "wasdebug": {
    "query": false,
    "event": {
      "name": null or <the_receiver_user_name>
      "type": <your_message_type>,  # the name of the message type, 
      "config": <your_event_payload> # what you would like to send with this event
    }
  }
}
```

A event is just send without waiting for any response

## Send Queries


```
{
  "wasdebug": {
    "query": true,
    "unlimited": true,
    "query_start_page" : 0
    "event": {
      "name": null,
      "type": "qrcoderaw",
      "config": "MT1PN:ABCDEF\u0000"
    }
  }
}
```

When a query is send, the debugger waits for the answers and returns the answer, which is always an array.

If `unlimited` is set to false, the result is splitted in pages, and the `query_start_page` parameter defines which of the result pages is returned as result.


