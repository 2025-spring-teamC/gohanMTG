from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from .models import User, FamilyGroup


#グループ選択機能
def group_select_view(request):

    context = {
        "action": request.POST.get("action", ""), # "join" or "create"
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
                if group.password == password:
                    request.session["group_id"] = group.id
                    return redirect("signup")
                else:
                    messages.error(request, "合言葉が間違っています")
            except FamilyGroup.DoesNotExist:
                    messages.error(request, "グループが見つかりません")

        #グループを作成する場合
        elif action == "create":
            name = context["new_group_name"]
            password = request.POST.get("new_group_password")
            if FamilyGroup.objects.filter(name=name).exists():
                messages.error(request, "そのグループ名は既に使われています")
            else:
                group = FamilyGroup.objects.create(name=name, password=password)
                request.session["group_id"] = group.id
                return redirect("signup")

    return render(request, "group_select.html", context)


#サインアップ機能
def signup_view(request):

    group_id = request.session.get("group_id")
    if not group_id:
        messages.error(request, "グループIDが無効です。もう一度グループ選択を行ってください。")
        return redirect("group_select")
    try:
        group = FamilyGroup.objects.get(id=group_id)
    except FamilyGroup.DoesNotExist:
        messages.error(request, "指定されたグループが見つかりません")
        return redirect("group_select")

    context = {
        "group": group,
        "name": request.POST.get("name", ""),
        "email": request.POST.get("email", ""),
    }

    #サインアップ処理
    if request.method == "POST":
        name = context["name"]
        email = context["email"]
        password = request.POST.get("password")

        if not (name and email and password and group_id):
            messages.error(request, "全ての項目を入力してください")
            return render(request, "signup.html", context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "このメールアドレスは既に使われています")
            return render(request, "signup.html", context)

        user = User.objects.create_user(email=email, password=password, name=name, familygroup=group)
        messages.success(request, "ユーザー登録が完了しました。ログインしてください。")
        del request.session["group_id"]
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
            return redirect("dashboard")
        else:
            messages.error(request, "メールアドレスまたはパスワードが間違っています")

    return render(request, "login.html", context)