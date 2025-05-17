from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from account.models import User, FamilyGroup
from account.validators import validate_password_strength, validate_email_format
from account.errors import add_error

# グループ名と合言葉の組み合わせが重複しないようにチェック
def validate_unique_group_name_and_password(name, password, errors):

        # 同じグループ名のグループが存在するか確認
    existing_groups = FamilyGroup.objects.filter(name=name)

    # 合言葉のハッシュを比較
    for group in existing_groups:
        if check_password(password, group.secret_key):
            errors = add_error(errors, "group_exists")
            break

    return errors


# グループ作成
def create_group(name, password, errors):

    # グループ名と合言葉の重複チェック
    errors = validate_unique_group_name_and_password(name, password, errors)
    if errors:
        return None, errors

    # グループ作成
    group = FamilyGroup.objects.create(
        name=name,
        secret_key=password
    )

    return group, errors


# グループ参加
def join_group(name, password, errors):

    try:
        group = FamilyGroup.objects.get(name=name)
        if check_password(password, group.secret_key):
            return group, errors
        else:
            errors = add_error(errors, "secret_key_mismatch")
    except FamilyGroup.DoesNotExist:
        errors = add_error(errors, "group_not_found")

    return None, errors


# サインアップのバリデーションエラー
def collect_signup_errors(name, email, password, password_confirm, errors):

    if not name:
        errors = add_error(errors, "name_required")
    if not email:
        errors = add_error(errors, "email_required")
    if not password:
        errors = add_error(errors, "password_required")
    if not password_confirm:
        errors = add_error(errors, "password_confirm_required")

    if email:
        try:
            errors = validate_email_format(email, errors)
        except ValidationError as e:
            errors.extend([f"メールアドレスエラー: {m}" for m in e.messages])
        if User.objects.filter(email=email).exists():
            errors = add_error(errors, "email_taken")

    if password:
        try:
            errors = validate_password_strength(password, errors)
        except ValidationError as e:
            errors.extend([f"パスワードエラー: {m}" for m in e.messages])

    if password != password_confirm:
        errors = add_error(errors, "password_mismatch")

    return errors

# セッションクリア
def clear_group_session(session):
    for key in ["group_action", "group_name", "group_password"]:
        session.pop(key, None)


# # 名前の更新
# def update_name(user, name, errors):
#     if not name:
#         errors = add_error(errors, "name_required")
#     else:
#         user.name = name
#     return errors


# # メールアドレスの更新
# def update_email(user, email, errors):
#     if not email:
#         errors = add_error(errors, "email_required")
#     elif User.objects.exclude(pk=user.pk).filter(email=email).exists():
#         errors = add_error(errors, "email_taken")
#     else:
#         user.email = email
#     return errors


# # パスワード更新
# def update_password(user, current_password, new_password, new_password_confirm, errors):
#     if not current_password:
#         errors = add_error(errors, "current_password_required")
#     elif not check_password(current_password, user.password):
#         errors = add_error(errors, "current_password_incorrect")
#     elif new_password != new_password_confirm:
#         errors = add_error(errors, "password_mismatch")
#     else:
#         errors = validate_password_strength(new_password, errors)

#     if not errors:
#         user.set_password(new_password)
#     return errors