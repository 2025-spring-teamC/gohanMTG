import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

def validate_password_strength(value):
    """パスワードの強度をチェックするカスタムバリデータ"""
    if len(value) < 8:
        raise ValidationError(_('パスワードは8文字以上でなければなりません。'))

    if not re.search(r'[a-z]', value):
        raise ValidationError(_('パスワードには少なくとも1つの小文字を含めてください。'))

    if not re.search(r'[A-Z]', value):
        raise ValidationError(_('パスワードには少なくとも1つの大文字を含めてください。'))

    if not re.search(r'[0-9]', value):
        raise ValidationError(_('パスワードには少なくとも1つの数字を含めてください。'))

    if not re.search(r'[@$!%*?&]', value):
        raise ValidationError(_('パスワードには少なくとも1つの特殊文字（例: @$!%*?&）を含めてください。'))


def validate_email_format(email):
    """メールアドレスの形式をチェック"""
    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        raise ValidationError("無効なメールアドレス形式です。")