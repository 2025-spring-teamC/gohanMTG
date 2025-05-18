import os, random, json, requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from django.shortcuts import render, redirect
from django.contrib import messages
from collections import defaultdict
from account.models import FamilyGroup, User
from search.models import Recipe, Group_recipe, User_recipe
from django.contrib.auth.decorators import login_required
from account.decorators import group_access_required



# レシピURLからimage, title, descriptionの情報を抽出する機能
def recipeURLscraping(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # image抽出
        recipe_image_tag = soup.find("meta", property="og:image")
        recipe_image_url = recipe_image_tag["content"] if recipe_image_tag else None

        # title抽出
        recipe_title_tag = soup.find("meta", property="og:title")
        recipe_title = recipe_title_tag["content"] if recipe_title_tag else soup.title.string if soup.title else ""
        # 投稿者名が入っているため除外
        if "by" in recipe_title:
            recipe_title = recipe_title.split("by")[0].strip()
        # 「レシピ・作り方」を除外
        recipe_title = recipe_title.replace("レシピ・作り方", "").strip()

        # description抽出
        recipe_description_tag = soup.find("meta", property="og:description")
        recipe_description = recipe_description_tag["content"] if recipe_description_tag else ""

        return {
            "image": recipe_image_url,
            "title": recipe_title,
            "description": recipe_description
        }

    except Exception as e:
        return {
            "image": None,
            "title": "",
            "description": ""
        }


#食べたいものリスト画面表示機能
@login_required
#@group_access_required
def wantToEat_view(request):

    user = request.user

    try:
        group = user.familygroup
    except FamilyGroup.DoesNotExist as e:
        messages.error(request, f"予期しないエラーが発生しました: {str(e)}")

    # POST処理
    if request.method == "POST":
        try:
            recipe_url = request.POST.get("recipe_url")
            action_source = request.POST.get("action_source", "")

            # モーダルウィンドウからレシピ追加
            if action_source == "modal":
                recipe, recipe_created = Recipe.objects.get_or_create(
                    user=user,
                    url=recipe_url
                )

            # 食べたいボタン押下時処理
            elif action_source == "detail":
                # 既存のレシピをURLで検索し、一番古いIDを持つレコードを取得
                recipe = Recipe.objects.filter(url=recipe_url).order_by("id").first()

            else:
                messages.error(request, "不正なリクエストです。")
                return redirect('want_to_eat')

            # Group_recipeに登録（共通）
            group_recipe, group_created = Group_recipe.objects.get_or_create(
                group=group,
                recipe=recipe,
                user=user
            )

            return redirect('want_to_eat')

        except Exception as e:
            messages.error(request, f"予期しないエラーが発生しました: {str(e)}")

    # GET処理
    # DBからデータ取得
    entries = Group_recipe.objects.filter(group=group).select_related("recipe", "user")

    # レシピごとにユーザー情報と登録日時まとめる
    recipe_info = defaultdict(list)
    for entry in entries:
        recipe_info[entry.recipe.url].append({
            "recipe_url": entry.recipe.url,
            "user": entry.user.name,
            "registered_at": entry.created_at,
        })

    # 表示しやすいように整形
    want_list = []
    for url, infos in recipe_info.items():
        scraping_data = recipeURLscraping(url)

        want_list.append({
            "url": url,
            "entries": infos,
            "image": scraping_data["image"],
            "title": scraping_data["title"],
            "description": scraping_data["description"]
        })

    context = {
        "group": group,
        "recipe_list": want_list,
    }

    return render(request, "want_eats.html", context)


def fetch_json(url):
    with urlopen(url) as response:
        return json.loads(response.read().decode())


# カテゴリー一覧を整形する機能
def category_hierarchy(json_data):
    parent_dict = {}
    category_list = []

    # 大カテゴリ
    for category in json_data['result']['large']:
        category_list.append({
            'category1': category['categoryId'],
            'category2': '',
            'category3': '',
            'categoryId': category['categoryId'],
            'categoryName': category['categoryName']
        })

    # 中カテゴリ
    for category in json_data['result']['medium']:
        full_id = f"{category['parentCategoryId']}-{category['categoryId']}"
        category_list.append({
            'category1': category['parentCategoryId'],
            'category2': category['categoryId'],
            'category3': '',
            'categoryId': full_id,
            'categoryName': category['categoryName']
        })
        parent_dict[str(category['categoryId'])] = category['parentCategoryId']

    # 小カテゴリ
    for category in json_data['result']['small']:
        parent_medium = category['parentCategoryId']
        parent_large = parent_dict.get(str(parent_medium), '')

        full_id = f"{parent_large}-{parent_medium}-{category['categoryId']}"
        category_list.append({
            'category1': parent_large,
            'category2': parent_medium,
            'category3': category['categoryId'],
            'categoryId': full_id,
            'categoryName': category['categoryName']
        })

    return category_list


# レシピ検索画面表示＆検索機能
@login_required
def searchRecipes_view(request):

    application_id = os.environ.get('RAKUTEN_APPLICATION_ID')
    hit = True
    foods = []

    # 楽天レシピカテゴリ一覧API
    category_url = f"https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId={application_id}"
    res = fetch_json(category_url)

    all_categories = category_hierarchy(res)
    search_query = request.GET.get("search", "")

    if search_query:
        # カテゴリ名に検索語を含むカテゴリを抽出
        categories_list = [
            cat for cat in all_categories
            if search_query in cat["categoryName"]
        ]

        if not categories_list:
            hit = False
        else:
            selected = random.choice(categories_list)
            category_id = selected["categoryId"]
            rank_url = f"https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId={application_id}&categoryId={category_id}"
            try:
                foods = fetch_json(rank_url)["result"]
            except Exception as e:
                print("[ERROR] Fetching ranking failed:", e)
                hit = False
    else:
        pop_url = f"https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId={application_id}&categoryId=30"
        foods = fetch_json(pop_url)["result"]

    request.session['foods'] = foods

    context = {
        "foods": foods,
        "hit": hit,
        "search": search_query,
        "categories": all_categories,
    }

    return render(request, "search_recipes.html", context)


# レシピ詳細画面表示機能
@login_required
def recipeDetail(request, recipe_id):

    user = request.user

    try:
        group = user.familygroup
    except FamilyGroup.DoesNotExist as e:
        messages.error(request, f"予期しないエラーが発生しました: {str(e)}")

    # POST処理
    if request.method == "POST":
        try:
            recipe_url = request.POST.get("recipe_url")

            # Recipeに登録
            recipe, recipe_created = Recipe.objects.get_or_create(
                user=user,
                url=recipe_url,
            )

            # Group_recipeに登録
            group_recipe, group_created = Group_recipe.objects.get_or_create(
                group=group,
                recipe=recipe,
                user=user
            )

            return redirect('want_to_eat')

        except Exception as e:
            messages.error(request, f"予期しないエラーが発生しました: {str(e)}")

    # GET処理
    foods = request.session.get('foods', [])

    recipe = next((food for food in foods if food["recipeId"] == recipe_id), None)

    if not recipe:
        return render(request, 'want_eats.html', status=404)

    return render(request, 'detail_recipes.html', {
        'recipe': recipe
    })