def shop_list_count(request):
    user = request.user
    count = user.purchases.all().count() if user.is_authenticated else 0
    return {'shop_list_count': count}
