def validate_password(password: str) -> bool:
    if len(password) < 6:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|`~" for char in password):
        return False
    return True
