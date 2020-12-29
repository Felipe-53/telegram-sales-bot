from dataclasses import dataclass
from typing import Optional, List


@dataclass
class WebhookData:
    """Webhook data model"""
    telegram_user_id: int
    chat_id: int
    first_name: str
    incoming_message_text: Optional[str] = None
    last_name: Optional[str] = ''
    reply_to_message: Optional[dict] = None
    location: Optional[List[str]] = None


@dataclass
class Address:
    number: str
    street: str
    neighborhood: str
    state: str
    city: str
    country: str
    details: Optional[str] = None
