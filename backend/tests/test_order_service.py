import pytest
from app.services.order_service import OrderService

def test_verify_invoice_match():
    order_service = OrderService()
    # Simulate finding a match for order "PO-123" with total 150.00
    is_valid, message = order_service.verify_order("PO-123", 150.00)
    assert is_valid is True
    assert "erfolgreich abgeglichen" in message

def test_verify_invoice_no_match():
    order_service = OrderService()
    # Simulate a non-existing order
    is_valid, message = order_service.verify_order("PO-999", 100.00)
    assert is_valid is False
    assert "nicht gefunden" in message

def test_verify_invoice_wrong_amount():
    order_service = OrderService()
    # Simulate an existing order but with a different amount
    is_valid, message = order_service.verify_order("PO-123", 200.00)
    assert is_valid is False
    assert "Betrag stimmt nicht überein" in message
