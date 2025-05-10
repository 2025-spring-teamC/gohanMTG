from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

"""
適用させたい関数名の前に

@group_access_required

と記載すれば、ログインユーザーが所属しているページ以外にはアクセスできないようになる
"""

def group_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインし直してください。")
            return redirect("login")
        if not hasattr(request.user, "familygroup") or request.user.familygroup is None:
            messages.error(request, "所属グループがありません。")
            return redirect("login")  # 適切なページに変更してください

        return view_func(request, *args, **kwargs)
    return _wrapped_view