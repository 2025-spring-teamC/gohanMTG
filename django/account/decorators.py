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
    def _wrapped_view(request, group_id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ログインし直してください。")
            return redirect("login")

        if int(request.user.familygroup_id) != int(group_id):
            messages.error(request, "このグループにはアクセスできません。")
            return redirect("login")

        return view_func(request, group_id, *args, **kwargs)
    return _wrapped_view