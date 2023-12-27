from django.shortcuts import render, get_object_or_404, redirect
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, wishlist_model, ProductImages, ProductReview, Address
from userauths.models import ContactUs, Profile
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Q


# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True)
    new_product = Product.objects.all().order_by("-id")[:3]
    product_ratings = {}
    feature_pro_ratings = {}

    for product in new_product:
        average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
        access_average = average_rating['rating']
        average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
        print(product.id)
        product_ratings[product.id] = {
            'average_rating_percentage': average_rating_percentage
        }

    for product in products:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
            print(product.id)
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }
    # Now product_ratings dictionary contains average ratings and percentages for each product
    print(product_ratings)

    context = {
        "products": products,
        "new_product":new_product,
        "product_ratings":product_ratings,
        "feature_pro_ratings":feature_pro_ratings
    }
    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")  
    tag = Tag.objects.all()  
    # product = Product.objects.all()

    feature_pro_ratings = {}
    for product in products:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
            print(product.id)
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }
    context = {
        "products": products,
        "feature_pro_ratings":feature_pro_ratings,
        "tag":tag,
        # "product":product
    }
    return render(request, 'core/product-list.html', context)

def category_list_view(request):
    categories = Category.objects.all().annotate(product_count=Count('category'))

    # categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    feature_pro_ratings = {}
    for product in products:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
            print(product.id)
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }

    context = {
            "category": category,
            "products": products,
            "feature_pro_ratings":feature_pro_ratings
        }
    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all().annotate(product_count=Count('vendor'))
    context={
        "vendors": vendors
    }
    return render(request, 'core/vendor-list.html', context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    feature_pro_ratings = {}
    total_average_percentage = 0
    count = 0
    for product in products:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0

            total_average_percentage += average_rating_percentage
            count += 1
            
    
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }
    
    if count > 0:
        average_of_averages = total_average_percentage / count
        avg_num = (average_of_averages/100)*5
        print(f"Average of average_rating_percentage: {average_of_averages}")
        vendor.avg_rating = average_of_averages
        vendor.save()
    else:
        print("No products to calculate the average.")

    context={
        "vendor": vendor,
        "products":products,
        "feature_pro_ratings":feature_pro_ratings,
        "average_of_averages":average_of_averages,
        "avg_num":avg_num
    }
    return render(request, 'core/vendor-detail.html', context)


def product_detail_view(request, pid):
    # product = Product.objects.get(pid=pid)

    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category = product.category).exclude(pid=pid)[:4]
    #Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #Getting average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    access_average = average_rating['rating']
    average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
    ratings_count = {}
    total_reviews = ProductReview.objects.filter(product=product).count()
    for rating in range(1, 6):
        rating_count = ProductReview.objects.filter(product=product, rating=rating).count()
        percentage = (rating_count / total_reviews) * 100 if total_reviews > 0 else 0
        ratings_count[rating] = {'percentage': percentage}

    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False

    p_images = product.p_images.all()

    context={
        "product":product,
        "p_images":p_images,
        "reviews": reviews,
        "make_review": make_review,
        "products":products,
        'ratings_count': ratings_count,
        'review_form': review_form,
        "average_rating":average_rating,
        "average_rating_percentage":average_rating_percentage,
    }
    return render(request, 'core/product-detail.html', context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")

    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    feature_pro_ratings = {}
    for product in products:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
            print(product.id)
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }

    context={
        "products":products,
        "tag":tag,
        "feature_pro_ratings":feature_pro_ratings
    }
    return render(request, 'core/tag.html', context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    access_average = average_reviews['rating']
    average_rating_percentage = (access_average/5)*100 if access_average is not None else 0

    ratings_count = {}
    total_reviews = ProductReview.objects.filter(product=product).count()
    for rating in range(1, 6):
        rating_count = ProductReview.objects.filter(product=product, rating=rating).count()
        percentage = (rating_count / total_reviews) * 100 if total_reviews > 0 else 0
        ratings_count[rating] = {'percentage': percentage}
    reviews = ProductReview.objects.filter(product=product).count()
    print(reviews)
    return JsonResponse(
        {
        'bool': True,
        'context':context,
        'average_reviews':average_reviews,
        'ratings_count':ratings_count,
        'reviews':reviews,
        'average_rating_percentage':average_rating_percentage
        }
    )

def search_view(request):
    query = request.GET['q']
    print(query)
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by("-date")
    # products = Product.objects.all()
    print(products)
    context={
        "products":products,
        "query":query
    }
    return render(request, "core/search.html",context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    tag = request.GET.getlist("tag[]")
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    if len(tag) > 0:
        products = products.filter(tags__name__in=tag).distinct()

    products1 = Product.objects.filter(product_status="published")
    
    feature_pro_ratings = {}
    for product in products1:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
            print(product.id)
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }
    data = render_to_string("core/async/product-list.html",{"products":products,"feature_pro_ratings":feature_pro_ratings})
    return JsonResponse({"data": data})

def filter_product_home(request):
    categories = request.GET['categories']
    if categories == "0":
        products = Product.objects.filter(product_status="published",featured=True)
    else:
        products = Product.objects.filter(product_status="published",featured=True)
        products = products.filter(category__id__in=categories)
    
    feature_pro_ratings = {}
    for product in products:
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
            access_average = average_rating['rating'] if average_rating is not None else 0
            average_rating_percentage = (access_average/5)*100 if access_average is not None else 0
            print(product.id)
            feature_pro_ratings[product.id] = {
                'average_rating_percentage': average_rating_percentage,
                'access_average':access_average
            }

    data = render_to_string("core/async/product-list-homepage.html",{"products":products, "feature_pro_ratings":feature_pro_ratings})
    return JsonResponse({"data": data})

def filter_category(request):
    categories = request.GET['cat']
    # categories_count = Category.objects.filter.annotate(product_count=Count('category'))

    cat = Category.objects.filter(title__icontains=categories).annotate(product_count=Count('category'))

    data = render_to_string("core/async/category-filter.html",{"cat":cat})
    return JsonResponse({"data": data})

def filter_item(request):
    product = request.GET['item']
    # categories_count = Category.objects.filter.annotate(product_count=Count('category'))

    item = Product.objects.filter(title__icontains=product).annotate(product_count=Count('category'))  
    data = render_to_string("core/async/item-filter.html",{"item":item})
    return JsonResponse({"data": data})

def filter_vendor(request):
    vendor = request.GET['vendor']
    # categories_count = Category.objects.filter.annotate(product_count=Count('category'))

    vendor = Vendor.objects.filter(title__icontains=vendor).annotate(product_count=Count('vendor'))  
    data = render_to_string("core/async/filter-vendor.html",{"vendors":vendor})
    return JsonResponse({"data": data})

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])]={
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'], 
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, "totalcartitems": len(request.session['cart_data_obj'])})
    
def update_from_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, "totalcartitems": len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    #Checking if cart_data_obj session exists
    if 'cart_data_obj' in request.session:
        #Getting total amount for paypal amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        #Create Order object
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,
        )

        #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no = "INVOICE_NO-" + str(order.id),
                item = item['title'],
                image= item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )

    host = request.get_host()
    paypal_dic = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': "Order-No" + str(order.id),
        'invoice': 'INV-'+str(order.id),
        'currency_code': "USD",
        'notify_url': 'http://{}{}'.format(host, reverse('core:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('core:payment-completed')),
        'cancel_url': 'http://{}{}'.format(host, reverse('core:payment-failed')),

    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dic)
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple addresses, only one should be ACTIVATED.")
        active_address= None

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items(): 
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/checkout.html', {'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'paypal_payment_button':paypal_payment_button,'active_address':active_address})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")

@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items(): 
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'core/payment-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    try: 
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None

    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month","count")
    month = []
    total_orders = []

    for o in orders:
        month.append(calendar.month_name[o["month"]])
        total_orders.append(o["count"])
        
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address added successfully.")
        return redirect("core:dashboard")
    
    context={
        "orders_list": orders_list,
        "address": address,
        "orders": orders,
        "month": month,
        "total_orders": total_orders,
        "profile": profile,
    }
    return render(request, 'core/dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)
    context={
        "products": products,
    }
    return render(request, 'core/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})

def wishlist_view(request): 
    # try:
    wishlist = wishlist_model.objects.all()
    # except:
    #     wishlist = None
    context = {
        "w": wishlist
    }
    return render(request, 'core/wishlist.html', context)

@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {

    }
    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context={
            "bool": True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            product=product,
            user=request.user,
        )
        context={
            "bool": True
        }

    return JsonResponse(context)

def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_d = wishlist_model.objects.get(id=pid)
    delete_product = wishlist_d.delete()
    context = {
            "bool":True,
            "w":wishlist,
        }
    qs_json = serializers.serialize('json', wishlist) 
    t = render_to_string('core/async/wishlist-list.html', context) 
    return JsonResponse({'data':t,'w':qs_json})

#Other pages
def contact(request):
    return render(request, "core/contact.html")

def about(request):
    return render(request, "core/about.html")

def ajax_contact(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data": data})