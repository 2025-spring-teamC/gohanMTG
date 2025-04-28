from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import User, FamilyGroup
from .validators import validate_password_strength, validate_email_format


#グループ選択機能
def group_select_view(request):
    context = {
        "action": request.POST.get("action", ""),  # "join" or "create"
        "group_name": request.POST.get("group_name", ""),
        "new_group_name": request.POST.get("new_group_name", ""),
    }

    if request.method == "POST":
        action = context["action"]

        if action not in ["join", "create"]:
            messages.error(request, "無効なアクションです")
            return render(request, "group_select.html", context)

        #グループに参加する場合
        if action == "join":
            name = context["group_name"]
            password = request.POST.get("group_password")

            try:
                group = FamilyGroup.objects.get(name=name)
                #ハッシュ化されたパスワードのチェック
                if check_password(password, group.password):
                    request.session["group_action"] = "join"
                    request.session["group_name"] = name
                    request.session["group_password"] = password
                    return redirect("signup")
                else:
                    messages.error(request, "合言葉が間違っています")

            except FamilyGroup.DoesNotExist:
                messages.error(request, "グループが見つかりません")
                context["group_name"] = ""


        #グループを作成する場合
        elif action == "create":
            name = context["new_group_name"]
            password = request.POST.get("new_group_password")

            existing_groups = FamilyGroup.objects.filter(name=name)
            group_exists = False
            for group in existing_groups:
                if check_password(password, group.password):
                    group_exists = True
                    break

            if group_exists:
                messages.error(request, "そのグループ名と合言葉の組み合わせは既に存在します")

            else:
                request.session["group_action"] = "create"
                request.session["group_name"] = name
                request.session["group_password"] = password
                return redirect("signup")

    return render(request, "group_select.html", context)


#サインアップ機能
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

        # 入力エラーをまとめて集める
        errors = []

        #入力項目チェック
        if not name:
            errors.append("名前を入力してください。")
        if not email:
            errors.append("メールアドレスを入力してください。")
        if not password:
            errors.append("パスワードを入力してください。")
        if not password_confirm:
            errors.append("確認用パスワードを入力してください。")

        # バリデーションエラーをまとめて集める
        try:
            validate_email_format(email)
        except ValidationError as e:
            errors.append(f"メールアドレスエラー: {str(e)}")

        try:
            validate_password_strength(password)
        except ValidationError as e:
            errors.append(f"パスワードエラー: {str(e)}")

        if password != password_confirm:
            errors.append("パスワードと確認用パスワードが一致しません。")

        # エラーが1つ以上あったら、すべて表示して戻す
        if errors:
            for error in errors:
                messages.error(request, error)
            context.update({
                "name": name,
                "email": email,
            })
            return render(request, "signup.html", context)

        # グループの作成または参加
        if group_action == "create":
            group = FamilyGroup.objects.create(
                name=group_name,
                password=make_password(group_password)
            )
        elif group_action == "join":
            try:
                group = FamilyGroup.objects.get(name=group_name)
            except FamilyGroup.DoesNotExist:
                messages.error(request, "グループが見つかりません")
                return redirect("group_select")
        else:
            messages.error(request, "不正なグループアクションです")
            return redirect("group_select")

        #ユーザー作成
        user = User.objects.create_user(email=email, password=password, name=name, familygroup=group)
        messages.success(request, "ユーザー登録が完了しました。ログインしてください。")

        #セッションクリア
        for key in ["group_action", "group_name", "group_password"]:
            if key in request.session:
                del request.session[key]

        return redirect("login")

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