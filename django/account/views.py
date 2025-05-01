from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import User, FamilyGroup
from .validators import validate_secret_word_strength
from .helpers import validate_unique_group_name_and_password, create_group, join_group, collect_signup_errors

# グループ選択機能
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
            messages.error(request, "無効なアクションです")
            return render(request, "group_select.html", context)

        #グループに参加する場合
        if action == "join":
            name = context["group_name"]
            password = request.POST.get("group_password")

            # 入力チェック
            if not name:
                errors.append("グループ名を入力してください。")
            if not password:
                errors.append("合言葉を入力してください。")

            try:
                group = FamilyGroup.objects.get(name=name)
                #ハッシュ化されたパスワードのチェック
                if check_password(password, group.secret_key):
                    request.session["group_action"] = "join"
                    request.session["group_name"] = name
                    request.session["group_password"] = password
                    return redirect("signup")
                else:
                    errors.append("合言葉が間違っています。")

            except FamilyGroup.DoesNotExist:
                errors.append("グループが見つかりません。")
                context["group_name"] = name

        #グループを作成する場合
        elif action == "create":
            name = context["new_group_name"]
            password = request.POST.get("new_group_password")

            # 入力チェック
            if not name:
                errors.append("グループ名を入力してください。")
            if not password:
                errors.append("合言葉を入力してください。")

            # バリデーションチェック
            try:
                validate_secret_word_strength(password)
            except ValidationError as e:
                for message in e.messages:
                    errors.append(f"合言葉エラー: {message}")

            # グループ名と合言葉の重複チェック
            try:
                validate_unique_group_name_and_password(name, password)
            except ValidationError as e:
                for message in e.messages:
                    errors.append(message)

            if errors:
                # エラーがある場合、フォームの入力値を保持して再表示
                for error in errors:
                    messages.error(request, error)
                    context["new_group_name"] = name
                return render(request, "group_select.html", context)

            # 成功した場合
            else:
                request.session["group_action"] = "create"
                request.session["group_name"] = name
                request.session["group_password"] = password
                return redirect("signup")

        # エラーがあった場合表示
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "group_select.html", context)

    return render(request, "group_select.html", context)


# サインアップ機能
@transaction.atomic
def signup_view(request):
    context = {
        "name": request.POST.get("name", ""),
        "email": request.POST.get("email", ""),
    }

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
        errors = collect_signup_errors(name, email, password, password_confirm)

        # エラーが1つ以上あったら、すべて表示して戻す
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "signup.html", context)

        # グループの作成または参加
        try:
            if group_action == "create":
                group = create_group(group_name, group_password)
            elif group_action == "join":
                group = join_group(group_name, group_password)
            else:
                raise Exception("不正なグループアクションです")
        except ValidationError as e:
            for message in e.messages:
                messages.error(request, message)
            return render(request, "signup.html", context)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("group_select")

        #ユーザー作成
        User.objects.create_user(
            email=email,
            password=password,
            name=name,
            familygroup=group
        )

        messages.success(request, "ユーザー登録が完了しました。ログインしてください。")

        #セッションクリア
        for key in ["group_action", "group_name", "group_password"]:
            request.session.pop(key, None)

        return redirect("home")

    return render(request, "signup.html", context)


#ログイン機能
def login_view(request):

    context = {
        "email": request.POST.get("email", ""),
    }

    if request.method == "POST":
        email = context["email"]
        password = request.POST.get("password", "")

        if not email or not password:
            messages.error(request, "メールアドレスとパスワードを両方入力してください")
            return render(request, "login.html", context)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "メールアドレスまたはパスワードが間違っています")

    return render(request, "login.html", context)

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