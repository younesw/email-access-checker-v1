import base64
import hashlib
import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from src.utils.config import get_settings


def _derive_key(secret: Optional[str] = None) -> bytes:
    secret_material = (secret or get_settings().secret_key).encode("utf-8")
    return hashlib.sha256(secret_material).digest()


def encrypt_value(value: str, secret: Optional[str] = None) -> str:
    if value is None:
        return ""
    key = _derive_key(secret)
    nonce = os.urandom(12)
    encrypted = AESGCM(key).encrypt(nonce, value.encode("utf-8"), None)
    return base64.b64encode(nonce + encrypted).decode("utf-8")


def decrypt_value(value: str, secret: Optional[str] = None) -> str:
    if not value:
        return ""
    key = _derive_key(secret)
    raw = base64.b64decode(value.encode("utf-8"))
    nonce = raw[:12]
    ciphertext = raw[12:]
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


def mask_secret(value: str, visible_chars: int = 2) -> str:
    if not value:
        return ""
    if len(value) <= visible_chars:
        return "*" * max(len(value), 1)
    return value[:visible_chars] + "*" * (len(value) - visible_chars)

