# How servers work

One request throughout: **two bowls of soup → $18**.

[Run the full example](how-servers-work.py) · Python 3, no dependencies.

## 1. A server is like a kitchen

![A server is like a kitchen; earlier parts remain visible](server-layers/01.png)

## 2. The browser sends a request

![The browser sends a request; earlier parts remain visible](server-layers/02.png)

## 3. The request arrives

![The request arrives; earlier parts remain visible](server-layers/03.png)

## 4. The route chooses a handler

![The route chooses a handler; earlier parts remain visible](server-layers/04.png)

## 5. Read the request body

![Read the request body; earlier parts remain visible](server-layers/05.png)

## 6. Check the input

![Check the input; earlier parts remain visible](server-layers/06.png)

## 7. Look up the price

![Look up the price; earlier parts remain visible](server-layers/07.png)

## 8. Calculate the total

![Calculate the total; earlier parts remain visible](server-layers/08.png)

## 9. Send the response

![Send the response; earlier parts remain visible](server-layers/09.png)

## 10. Display the result

![Display the result; earlier parts remain visible](server-layers/10.png)

## Try the complete example

```sh
python3 examples/how-servers-work.py
```

Open **http://127.0.0.1:8765** and select **Get price**. Stop with Ctrl+C.

<details>
<summary>See the request and response</summary>

```http
POST /quote
Content-Type: application/json

{"item":"soup","quantity":2}
```

```json
{"item":"soup","quantity":2,"total":18,"currency":"USD"}
```

The server routes, parses, validates, reads its in-memory menu, calculates, then responds. The browser renders the result. This example adds as many layers as these mechanisms require; other topics need different counts.

This is a local teaching server using Python’s standard library, not a production deployment.
</details>
