from django.urls import path, include
from core.views import index, category_list_view,product_list_view,category_product_list_view,vendor_list_view,vendor_detail_view,product_detail_view,tag_list,ajax_add_review,search_view,filter_product,add_to_cart,cart_view,delete_item_from_cart,update_from_cart,checkout_view,payment_completed_view,payment_failed_view,customer_dashboard,order_detail,make_address_default,wishlist_view,add_to_wishlist,remove_wishlist,contact,ajax_contact,filter_product_home,filter_category,filter_item,filter_vendor,about


app_name = "core"

urlpatterns = [
    #Homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("products/<pid>/", product_detail_view, name="product-detail"),

    #Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    #Vendor
    path("vendor/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),

    #Tag
    path("products/tags/<tag_slug>/", tag_list, name="tags"),

    #Add review
    path("ajax_add_review/<int:pid>/",ajax_add_review, name="ajax_add_review"),

    #Search
    path("search/",search_view, name="search"),

    #Filter product URL
    path("filter-product",filter_product, name="filter-product"),
    path("filter-product-homepage",filter_product_home, name="filter-product-home"),
    path("filter-category",filter_category, name="filter_category"),
    path("filter-item",filter_item, name="filter_item"),
    path("filter-vendor",filter_vendor, name="filter_vendor"),





    #Add to cart URL
    path("add-to-cart/",add_to_cart, name="add-to-cart"),

    #Cart Page URL
    path("cart/",cart_view, name="cart"),

    #Delete Item from Cart
    path("delete-from-cart/",delete_item_from_cart, name="delete-from-cart"),


    #Checkout 
    path("checkout/",checkout_view, name="checkout"),

    #Update Cart
    path("update-cart/",update_from_cart, name="update-cart"),

    #Paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    #Payment Successful
    path('payment-completed/', payment_completed_view, name="payment-completed"),

    #Payment Failed
    path('payment-failed/', payment_failed_view, name="payment-failed"),

    #Dashboard
    path('dashboard/', customer_dashboard, name="dashboard"),

    #Order detail
    path('dashboard/order/<int:id>', order_detail, name="order-detail"),

    #Making address default
    path("make-default-address/", make_address_default, name="make-default-address"),

    #Wishlist page
    path("wishlist/", wishlist_view, name="wishlist"),

    #Adding to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    #Removing from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),

    #Contact page
    path("contact/", contact, name="contact"),

    #Contact ajax page
    path("ajax-contact-form/", ajax_contact, name="ajax-contact-form"),

    path("about/", about, name="about"),
    
]
