from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('category/<int:category_id>/', views.category_items_view, name='category_items'),
    path('item/<int:item_id>/', views.item_details_view, name='item_details'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('buy-now/<int:item_id>/', views.buy_now, name='buy_now'),
    path('checkout/<int:item_id>/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('aboutus/', views.about, name='aboutus'),
    
]