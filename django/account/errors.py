#エラー文
ERROR_MESSAGES = {
    "invalid_action": "無効なアクションです",

    # group_select
    "group_name_required": "グループ名を入力してください。",
    "group_password_required": "合言葉を入力してください。",
    "group_not_found": "グループが見つかりません。",
    "secret_key_mismatch": "合言葉が間違っています。",
    "group_exists": "そのグループ名と合言葉の組み合わせは既に存在します。",

    # signup
    "name_required": "名前を入力して下さい。",
    "email_required": "メールアドレスを入力してください。",
    "password_required": "パスワードを入力してください。",
    "password_confirm_required": "確認用パスワードを入力してください。",
    "password_mismatch": "パスワードと確認用パスワードが一致しません。",
    "password_strength": "パスワードは強力である必要があります。",
    "email_taken": "そのメールアドレスは既に登録されています。",

    # login
    "email_and_password_required": "メールアドレスとパスワードを両方入力してください",
    "invalid_credentials": "メールアドレスまたはパスワードが間違っています",

    # バリデーション
    "secret_key_too_short": "合言葉は8文字以上でなければなりません。",
    "password_too_short": "パスワードは8文字以上でなければなりません。",
    "password_missing_lowercase": "パスワードには少なくとも1つの小文字を含めてください。",
    "password_missing_uppercase": "パスワードには少なくとも1つの大文字を含めてください。",
    "password_missing_number": "パスワードには少なくとも1つの数字を含めてください。",
    "password_missing_special": "パスワードには少なくとも1つの特殊文字（例: @$!%*?&）を含めてください。",
    "invalid_email": "無効なメールアドレス形式です。",
}


# エラーキーを受け取ってエラーメッセージを追加する関数
def add_error(errors, error_key):

    if error_key in ERROR_MESSAGES:
        errors.append(ERROR_MESSAGES[error_key])
    else:
        errors.append("予期しないエラーが発生しました。")

    return errors