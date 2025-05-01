from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from .models import User, FamilyGroup
from .validators import validate_secret_word_strength, validate_password_strength, validate_email_format


# グループ名と合言葉の組み合わせが重複しないようにチェック
def validate_unique_group_name_and_password(name, password):
    try:
        # 同じグループ名のグループが存在するか確認
        existing_group = FamilyGroup.objects.get(name=name)

        # 合言葉のハッシュを比較
        if check_password(password, existing_group.secret_key):
            raise ValidationError("そのグループ名と合言葉の組み合わせは既に存在します。")
    except FamilyGroup.DoesNotExist:
        # グループ名が存在しない場合は新規作成可能
        pass


# グループ作成
def create_group(name, password):

    # グループ名と合言葉の重複チェック
    validate_unique_group_name_and_password(name, password)

    # 合言葉のハッシュ化
    hashed_password = make_password(password)

    # グループ作成
    group = FamilyGroup.objects.create(
        name=name,
        secret_key=hashed_password
    )
    return group


# グループ参加
def join_group(name, password):
    """
    既存のグループに参加する処理
    """
    try:
        group = FamilyGroup.objects.get(name=name)
        if check_password(password, group.secret_key):
            return group
        else:
            raise ValidationError("合言葉が間違っています。")
    except FamilyGroup.DoesNotExist:
        raise ValidationError("グループが見つかりません。")


# サインアップのバリデーションエラー
def collect_signup_errors(name, email, password, password_confirm):
    errors = []

    if not name:
        errors.append("名前を入力してください。")
    if not email:
        errors.append("メールアドレスを入力してください。")
    if not password:
        errors.append("パスワードを入力してください。")
    if not password_confirm:
        errors.append("確認用パスワードを入力してください。")

    if email:
        try:
            validate_email_format(email)
        except ValidationError as e:
            errors.extend([f"メールアドレスエラー: {m}" for m in e.messages])
        if User.objects.filter(email=email).exists():
            errors.append("そのメールアドレスは既に登録されています。")

    if password:
        try:
            validate_password_strength(password)
        except ValidationError as e:
            errors.extend([f"パスワードエラー: {m}" for m in e.messages])

    if password != password_confirm:
            errors.append("パスワードと確認用パスワードが一致しません。")

    return errors