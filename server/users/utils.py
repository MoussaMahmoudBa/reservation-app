from typing import Optional
import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

COUNTRY_CODE = "+222"


def normalize_phone(phone_raw: str) -> str:
    """Normalise un numéro en format +222######## (8 chiffres).
    - Supprime espaces et séparateurs
    - Accepte formats: ########, 0########, 222########, +222 ########
    - Retourne le format canonique +222########
    """
    if not phone_raw:
        return ""
    digits = ''.join(ch for ch in phone_raw if ch.isdigit())

    # Retirer préfixes 00, 0, ou 222
    if digits.startswith('00'):
        digits = digits[2:]
    if digits.startswith('0'):
        digits = digits[1:]
    if digits.startswith('222'):
        digits = digits[3:]

    # Ne garder que les 8 derniers chiffres si plus long
    if len(digits) > 8:
        digits = digits[-8:]

    # Si moins de 8 chiffres, renvoyer tel quel (validation ailleurs)
    if len(digits) != 8:
        return f"{COUNTRY_CODE}{digits}" if digits else ""

    return f"{COUNTRY_CODE}{digits}"


def generate_otp(length: int = 6) -> str:
    """Génère un OTP numérique de longueur donnée."""
    length = max(4, min(8, length))
    start = 10 ** (length - 1)
    end = (10 ** length) - 1
    return str(random.randint(start, end))


def get_default_otp_expiry(minutes: int = 10):
    """Retourne l'échéance par défaut pour un OTP."""
    return timezone.now() + timedelta(minutes=minutes)


def send_sms(phone: str, message: str) -> None:
    """Envoie un SMS via Twilio si configuré, sinon fallback console."""
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_number = getattr(settings, 'TWILIO_FROM_NUMBER', '')

    if account_sid and auth_token and from_number:
        try:
            from twilio.rest import Client  # type: ignore
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=message,
                from_=from_number,
                to=phone
            )
        except Exception as exc:
            # En cas d'échec Twilio, on logge et fallback console
            print(f"[Twilio Error] {exc}")
            print(f"[SMS to {phone}] {message}")
    else:
        # Fallback dev
        print(f"[SMS to {phone}] {message}")


def extract_last8_digits(phone_raw: str) -> str:
    digits = ''.join(ch for ch in phone_raw if ch.isdigit())
    return digits[-8:] if len(digits) >= 8 else digits


def candidate_phone_variants(phone_raw: str) -> list[str]:
    """Retourne des variantes possibles de numéro pour recherche tolérante."""
    last8 = extract_last8_digits(phone_raw)
    variants = set()
    if last8:
        variants.add(f"{COUNTRY_CODE}{last8}")      # +222########
        variants.add(f"222{last8}")                 # 222########
        variants.add(f"0{last8}")                   # 0########
        variants.add(last8)                          # ########
    return list(variants)