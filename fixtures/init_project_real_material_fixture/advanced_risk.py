class RiskManager:
    """Central bank style risk gate."""

    def approve_action(self, intent: dict) -> bool:
        return bool(intent)
