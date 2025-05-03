import os, random, json, unicodedata
from urllib.request import urlopen
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from account.models import FamilyGroup, User
from search.models import Recipes, Group_recipes, User_recipes



#食べたいものリスト画面表示機能
def wantToEat_view(request, group_id):

    # DBからデータ取得
    group = get_object_or_404(FamilyGroup, id=group_id)
    entries = Group_recipes.objects.filter(group=group)

    # レシピごとにユーザー情報と登録日時まとめる
    recipe_info = defaultdict(list)
    for entry in entries:
        recipe_info[entry.recipe.url].append({
            "recipe_name": entry.recipe.name,
            "user": entry.user.name,
            "registered_at": entry.created_at,
        })

    # 表示しやすいように整形
    want_list = [
        {
            "url": url,
            "recipe_name": infos[0]["recipe_name"],
            "entries": infos
        }
        for url, infos in recipe_info.items()
    ]

    context = {
        "group": group,
        "recipe_list": want_list,
    }

    return render(request, "want_eats.html", context)


def fetch_json(url):
    with urlopen(url) as response:
        return json.loads(response.read().decode())

# カテゴリー一覧を整形
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
            print(f"選択されたカテゴリ: {selected['categoryName']} ({selected['categoryId']})")
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
def recipeDetail(request, recipe_id):
    foods = request.session.get('foods', [])

    recipe = next((food for food in foods if food["recipeId"] == recipe_id), None)

    if not recipe:
        return render(request, 'want_eats.html', status=404)

    return render(request, 'detail_recipes.html', {
        'recipe': recipe
    })