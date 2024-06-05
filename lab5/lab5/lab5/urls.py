"""
URL configuration for lab5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('register', views.register, name='register'),
                  path('login', views.login_view, name='login'),
                  path('logout', views.logout_view, name='logout'),
                  path('products/', views.products_view, name='products'),
                  path('cart', views.user_cart_view, name='cart'),
                  path('add-to-cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
                  path('news', views.news_view, name='news'),
                  path('coupons', views.coupons_view, name='coupons'),
                  path('contacts', views.contacts_view, name='contacts'),
                  path('about', views.about_us_view, name='about'),
                  path('glossary', views.glossary_view, name='glossary'),
                  path('customer/orders/<int:order_id>', views.customer_order_details_view,
                       name='customer_order_details'),
                  path('employee/orders/<int:order_id>', views.employee_order_details_view,
                       name='employee_order_details'),
                  path('customer/orders', views.customer_orders_view, name='customer_orders'),
                  path('manage/orders', views.manage_orders_view, name='manage_orders'),
                  path('orders_statistics', views.order_statistics_view, name='orders_statistics'),
                  path('reviews', views.reviews_view, name='reviews'),
                  path('reviews/add', views.add_review_view, name='add_review'),
                  path('cart/remove/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
                  path('cart/update/<int:cart_item_id>', views.update_cart_item, name='update-cart-item'),
                  path('change_order_status/<int:order_id>', views.change_order_status, name='change_order_status'),
                  path('order_status_distribution', views.order_status_distribution, name='order_status_distribution')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
