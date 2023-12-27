from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, wishlist_model, ProductImages, ProductReview, Address
from django.db.models import Min, Max
from django.contrib import messages
from django.db.models import Count
def default(request):
    # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count('category'))

    min_max_price = Product.objects.aggregate(Min("price"),Max("price"))
    
    try:
        wishlist = wishlist_model.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to login before accessing your wishlist.")
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    vendor = Vendor.objects.all()
    return{
        'wishlist': wishlist,
        'categories': categories,
        'address':address,
        'vendor':vendor,
        'min_max_price':min_max_price,
    }