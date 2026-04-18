from typing import Tuple

class OrderService:
    def __init__(self):
        # Dummy order data (Simulating a database or ERP system)
        self.dummy_orders = {
            "PO-123": {"amount": 150.00, "status": "open"},
            "PO-456": {"amount": 599.99, "status": "shipped"},
            "PO-789": {"amount": 42.50, "status": "delivered"}
        }

    def verify_order(self, order_id: str, invoice_amount: float) -> Tuple[bool, str]:
        """
        Verifies if an invoice matches an existing order.
        Returns (is_valid, message)
        """
        order = self.dummy_orders.get(order_id)
        
        if not order:
            return False, f"Bestellung {order_id} wurde im System nicht gefunden."
            
        if abs(order["amount"] - invoice_amount) > 0.01:
            return False, f"Betrag stimmt nicht überein (Bestellt: {order['amount']:.2f}, Rechnung: {invoice_amount:.2f})."
            
        return True, f"Rechnung für Bestellung {order_id} über {invoice_amount:.2f} erfolgreich abgeglichen."
