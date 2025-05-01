from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from .errors import add_error


# 合言葉のバリデーション
def validate_secret_word_strength(value, errors):
    """パスワードの強度をチェックするカスタムバリデータ"""
    if len(value) < 8:
        errors = add_error(errors, "secret_key_too_short")

    return errors

# パスワードのバリデーション
def validate_password_strength(value, errors):
    """パスワードの強度をチェックするカスタムバリデータ"""
    if len(value) < 8:
        errors = add_error(errors, "password_too_short")

    # if not re.search(r'[a-z]', value):
    #     errors = add_error(errors, "password_missing_lowercase")
    # if not re.search(r'[A-Z]', value):
    #     errors = add_error(errors, "password_missing_uppercase")
    # if not re.search(r'[0-9]', value):
    #     errors = add_error(errors, "password_missing_number")
    # if not re.search(r'[@$!%*?&]', value):
    #     errors = add_error(errors, "password_missing_special")

    return errors

# メールアドレスのバリデーション
def validate_email_format(email, errors):
    """メールアドレスの形式をチェック"""
    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        errors = add_error(errors, "invalid_email")
    return errors