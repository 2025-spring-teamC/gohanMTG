from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.db import transaction
from account import models, helpers, validators
from account.errors import add_error
from django.contrib.auth.decorators import login_required

# グループ選択画面
def group_select_view(request):
    context = {
        "action": request.POST.get("action", ""),  # "join" or "create"
        "group_name": request.POST.get("group_name", ""),
        "new_group_name": request.POST.get("new_group_name", ""),
    }
    errors = []

    if request.method == "POST":
        action = context["action"]

        if action not in ["join", "create"]:
            errors = add_error(errors, "invalid_action")
            return render(request, "group_select.html", context)

        #グループに参加する場合
        if action == "join":
            name = context["group_name"]
            password = request.POST.get("group_password")

            # 入力チェック
            if not name:
                errors = add_error(errors, "group_name_required")
            if not password:
                errors = add_error(errors, "group_password_required")

            try:
                group = models.FamilyGroup.objects.get(name=name)
                #ハッシュ化されたパスワードのチェック
                if check_password(password, group.secret_key):
                    request.session["group_action"] = "join"
                    request.session["group_name"] = name
                    request.session["group_password"] = password
                    return redirect("signup")
                else:
                    errors = add_error(errors, "secret_key_mismatch")

            except models.FamilyGroup.DoesNotExist:
                errors = add_error(errors, "group_not_found")

        #グループを作成する場合
        elif action == "create":
            name = context["new_group_name"]
            password = request.POST.get("new_group_password")

            # 入力チェック
            if not name:
                errors = add_error(errors, "group_name_required")
            if not password:
                errors = add_error(errors, "group_password_required")

            # バリデーションチェック
            if password:
                errors = validators.validate_secret_word_strength(password, errors)

            # グループ名と合言葉の重複チェック
            errors = helpers.validate_unique_group_name_and_password(name, password, errors)

            # 成功した場合
            if not errors:
                request.session["group_action"] = "create"
                request.session["group_name"] = name
                request.session["group_password"] = password
                return redirect("signup")

        if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, "group_select.html", context)

    return render(request, "group_select.html", context)


# サインアップ画面
@transaction.atomic
def signup_view(request):
    context = {
        "name": request.POST.get("name", ""),
        "email": request.POST.get("email", ""),
    }
    errors = []

    group_action = request.session.get("group_action")
    group_name = request.session.get("group_name")
    group_password = request.session.get("group_password")

    if not (group_action and group_name and group_password):
        messages.error(request, "グループ情報が無効です")
        return redirect("group_select")

    #サインアップ処理
    if request.method == "POST":
        name = context["name"]
        email = context["email"]
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # サインアップのバリデーションエラー
        errors = helpers.collect_signup_errors(name, email, password, password_confirm, errors)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "signup.html", context)

        # グループの作成または参加
        try:
            if group_action == "create":
                group, errors = helpers.create_group(group_name, group_password, errors)
            elif group_action == "join":
                group, errors = helpers.join_group(group_name, group_password, errors)
            else:
                errors = add_error(errors, "invalid_action")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect("group_select")

        except Exception as e:
            messages.error(request, f"予期しないエラーが発生しました: {str(e)}")
            for key in ["group_action", "group_name", "group_password"]:
                request.session.pop(key, None)
            return redirect("group_select")

        #ユーザー作成
        icon_code = helpers.get_unique_icon_for_group(group)

        try:
            user = models.User.objects.create_user(
                email=email,
                password=password,
                name=name,
                familygroup=group,
                icon_code=icon_code,
            )

            helpers.clear_group_session(request.session)
            login(request, user)
            return redirect("want_to_eat")

        except Exception as e:
            transaction.set_rollback(True)
            messages.error(request, f"ユーザー登録中にエラーが発生しました: {str(e)}")
            helpers.clear_group_session(request.session)
            return redirect("group_select")

    return render(request, "signup.html", context)


#ログイン画面処理
def login_view(request):

    context = {
        "email": request.POST.get("email", ""),
    }
    errors = []

    if request.method == "POST":
        email = context["email"]
        password = request.POST.get("password", "")

        if not email or not password:
            errors = add_error(errors, "email_and_password_required")
            return render(request, "login.html", context)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("want_to_eat")
        else:
            errors = add_error(errors, "invalid_credentials")

        if errors:
            for error in errors:
                messages.error(request, error)

    return render(request, "login.html", context)


# ログアウト画面処理
def logout_view(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('login')


# # マイページ画面処理
# @login_required
# def mypage_view(request):
#     user = request.user
#     context = {
#         "name": user.name,
#         "email": user.email,
#     }
#     errors = []

#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()
#         email = request.POST.get("email", "").strip()
#         current_password = request.POST.get("current_password", "")
#         new_password = request.POST.get("new_password", "")
#         new_password_confirm = request.POST.get("new_password_confirm", "")

#         # 各更新処理を呼び出し
#         errors = helpers.update_name(user, name, errors)
#         errors = helpers.update_email(user, email, errors)

#         if new_password or new_password_confirm:
#             errors = helpers.update_password(user, current_password, new_password, new_password_confirm, errors)

#         if errors:
#             for error in errors:
#                 messages.error(request, error)
#             context.update({"name": name, "email": email})
#             return render(request, "mypage.html", context)

#         # 変更保存
#         user.save()
#         if new_password:
#             update_session_auth_hash(request, user)

#         messages.success(request, "ユーザー情報を更新しました。")
#         return redirect("mypage")

#     return render(request, "mypage.html", context)


#追い出し処理
# @login_required
# def kick_member_view(request, user_id):
#     # 追い出す対象のユーザー
#     target_user = get_object_or_404(User, id=user_id)

#     # 今ログインしているユーザー
#     current_user = request.user

#     # 同じグループに所属しているかチェック（念のため）
#     if target_user.familygroup != current_user.familygroup:
#         messages.error(request, "同じグループのメンバーしか削除できません")
#         return redirect("home")

#     # 追い出す
#     target_user.familygroup = None
#     target_user.save()

#     messages.success(request, f"{target_user.name} をグループから退出させましました")
#     return redirect("home")