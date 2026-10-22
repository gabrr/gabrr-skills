# One request. One receipt.

![Idempotency, learned in five layers](../assets/learn-layered.gif)

1. **Visual:** three copies of one request lead to one receipt.
2. **Analogy:** show the cashier the same order number; get the existing receipt.
3. **Tiny:** remember whether an order was handled.
4. **Bigger:** save its result and return it on a retry.
5. **Complete:** [run the example](idempotency.py).

```sh
python3 examples/idempotency.py
```

Expected: three identical receipts, one receipt created.

This is an in-memory, single-process demonstration. A real service needs durable storage, concurrency protection, and checks that a reused key carries the same request.
