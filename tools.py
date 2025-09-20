from database import get_orders

def tool_check_order(order_id: str = None) -> str:
    """Mengembalikan status pesanan berdasarkan ORDER ID."""
    status = get_orders(order_id)
    if status:
        return f"Pesanan {order_id} berstatus: {status}."
    else:
        return "Saya tidak menemukan pesananmu. Periksa kembali ORDER ID Anda."