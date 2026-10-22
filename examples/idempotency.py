"""Run with Python 3. No dependencies or external services."""
receipts = {}


def issue_receipt(order_id):
    if order_id not in receipts:
        receipts[order_id] = {"receipt_id": f"receipt-{len(receipts) + 1}", "order_id": order_id}
    return dict(receipts[order_id])


if __name__ == "__main__":
    for attempt in range(1, 4):
        print(f"Attempt {attempt}: {issue_receipt('order-123')}")
    print(f"Receipts created: {len(receipts)}")
