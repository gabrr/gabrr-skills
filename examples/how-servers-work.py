"""A small browser/server example. Run: python3 examples/how-servers-work.py"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MENU = {"soup": 9, "salad": 12}
PAGE = b'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Two bowls of soup</title><style>
body{max-width:480px;margin:15vh auto;padding:24px;font:18px/1.6 system-ui;background:#f6f7f4;color:#172a2c}
button{font:inherit;background:#1b6972;color:white;border:0;border-radius:8px;padding:12px 20px;cursor:pointer}
pre{white-space:pre-wrap;background:white;border-radius:8px;padding:20px;font-size:14px}
</style><h1>Two bowls of soup</h1><p>Your browser asks the server to calculate the price.</p>
<button id="quote">Get price</button><p id="total" aria-live="polite"></p>
<details><summary>See the response</summary><pre id="response"></pre></details>
<script>
document.getElementById('quote').onclick=async()=>{
  const output=document.getElementById('total');output.textContent='Requesting...';
  try{
    const response=await fetch('/quote',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({item:'soup',quantity:2})});
    const data=await response.json();
    document.getElementById('response').textContent=JSON.stringify(data,null,2);
    output.textContent=response.ok?`Total: $${data.total}`:data.error;
  }catch{output.textContent='Could not reach the server.'}
};
</script></html>'''


class App(BaseHTTPRequestHandler):
    def respond_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/":
            self.respond_json(404, {"error": "Not found"})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.end_headers()
        self.wfile.write(PAGE)

    def do_POST(self):
        # Route: choose the handler for this method and path.
        if self.path != "/quote":
            self.respond_json(404, {"error": "Not found"})
            return
        self.quote()

    def quote(self):
        # Read and parse the request body.
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 2048:
                raise ValueError("Invalid body size")
            order = json.loads(self.rfile.read(size))
        except (ValueError, UnicodeError):
            self.respond_json(400, {"error": "Send a small JSON request"})
            return
        # Validate before using the input.
        if not isinstance(order, dict):
            self.respond_json(400, {"error": "Send an object"})
            return
        item, quantity = order.get("item"), order.get("quantity")
        if not isinstance(item, str) or type(quantity) is not int or not 1 <= quantity <= 10:
            self.respond_json(400, {"error": "Use an item name and a quantity from 1 to 10"})
            return
        # Look up data, calculate, then send a response.
        price = MENU.get(item)
        if price is None:
            self.respond_json(404, {"error": "Item not on the menu"})
            return
        total = price * quantity
        self.respond_json(200, {"item": item, "quantity": quantity, "total": total, "currency": "USD"})


if __name__ == "__main__":
    print("Open http://127.0.0.1:8765 — Ctrl+C to stop.")
    with ThreadingHTTPServer(("127.0.0.1", 8765), App) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
