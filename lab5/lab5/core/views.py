from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Count, Sum

from core.forms import *
from core.models import *


def register(request):
    current_time = getattr(request, 'current_time', None)
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            customer = Customer(
                user=user,
                age=form.cleaned_data['age']
            )
            customer.save()

            # Create a cart for the user
            cart = Cart.objects.create(user=customer)

            permission = Permission.objects.get(codename="customer")
            user.user_permissions.add(permission)

            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'auth/register.html', {'form': form, 'current_time': current_time})


def login_view(request):
    current_time = getattr(request, 'current_time', None)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('products')
            else:
                # Return an 'invalid login' error message.
                # messages.error(request, 'Invalid username or password.')
                return render(request, 'auth/login.html', {'form': form, 'current_time': current_time})
    else:

        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form, 'current_time': current_time})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    # Redirect to the homepage or any other page after logout.
    return redirect('products')  # todo: Replace 'home' with the name of your homepage URL pattern.


def products_view(request):
    current_time = getattr(request, 'current_time', None)
    # Get the query parameters
    product_name = request.GET.get('product_name')
    category_name = request.GET.get('category')

    # Filter products based on the search query and category
    products = Product.objects.all()
    if product_name:
        products = products.filter(name__icontains=product_name)
    if category_name:
        products = products.filter(category__name=category_name)

    categories = ProductCategory.objects.all()
    latest_news = News.objects.order_by('-created_at')[:1]

    context = {
        'current_time': current_time,
        'product_name': product_name,
        'category_name': category_name,
        'products': products,
        'categories': categories,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'latest_news': latest_news
    }
    return render(request, 'products.html', context)


@permission_required('core.customer', login_url='login/')
def user_cart_view(request):
    # current_time = getattr(request, 'current_time', None)
    discount = 0
    coupon_code = None
    total_price = 0

    # Get the current user's cart
    try:
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(user=customer)
        cart_items = cart.cartitem_set.all()
    except Cart.DoesNotExist:
        cart_items = []

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip()
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                discount = coupon.discount
            except Coupon.DoesNotExist:
                discount = 0

        if cart_items:
            # Create the order
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.create(user=customer)
            total_price = 0
            for cart_item in cart_items:
                # Create an order item for each cart item
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.product.price,
                    total_price=cart_item.product.price * cart_item.quantity
                )
                total_price += order_item.total_price
                cart_item.delete()

            # Apply discount
            if discount:
                total_price -= total_price * (discount / 100)

            # Update the total price of the order
            order.total_price = total_price
            order.save()

            # Redirect to the user's orders page or any other page as needed
            return redirect('customer_orders')

    # 'current_time': current_time,
    context = {

        'cart_items': cart_items,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'total_price': total_price,
        'discount': discount,
        'coupon_code': coupon_code,
    }
    return render(request, 'cart.html', context)


@permission_required('core.customer', login_url='login/')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        # Extract product ID and quantity from the request
        quantity = request.POST.get('quantity', 1)  # Default to 1 if quantity is not provided
        # Retrieve the product object based on the product ID
        product = get_object_or_404(Product, pk=product_id)

        # Check if the product exists and if the quantity is valid
        if product and int(quantity) > 0:
            # Get the user's cart or create a new one if it doesn't exist
            cart, created = Cart.objects.get_or_create(user=customer)

            # Add the item to the cart or update its quantity if it already exists
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()

            return redirect('cart')  # Redirect to the cart page
        else:
            # Handle invalid product or quantity
            return redirect('products')  # Redirect to the products page or display an error message
    else:
        # Handle non-POST requests
        return redirect('products')  # Redirect to the products page or display an error message


@permission_required('core.customer', login_url='login/')
def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=cart_item_id)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        return redirect('cart')
    else:
        return redirect('products')


@permission_required('core.customer', login_url='login/')
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return redirect('cart')
    else:
        return redirect('products')


def news_view(request):
    current_time = getattr(request, 'current_time', None)
    # Retrieve all news items from the database
    all_news = News.objects.all()

    context = {
        'all_news': all_news,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'news.html', context)


def coupons_view(request):
    current_time = getattr(request, 'current_time', None)
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'coupons.html', context)


def contacts_view(request):
    current_time = getattr(request, 'current_time', None)
    employees = Employee.objects.all()
    context = {
        'employees': employees,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'contacts.html', context)


def about_us_view(request):
    current_time = getattr(request, 'current_time', None)
    context = {
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'about.html', context)


def glossary_view(request):
    current_time = getattr(request, 'current_time', None)
    # Assuming GlossaryEntry is your model for glossary entries
    entries = GlossaryEntry.objects.all()
    context = {
        'entries': entries,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'glossary.html', context)


@permission_required('core.customer', login_url='login/')
def customer_order_details_view(request, order_id):
    current_time = getattr(request, 'current_time', None)
    # Assuming you have a model named OrderItem and order_id is passed in the URL
    order_items = OrderItem.objects.filter(order_id=order_id)
    context = {
        'order_items': order_items,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'orders/customer_order_details.html', context)


@permission_required('core.employee', login_url='/auth/login/')
def change_order_status(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        if new_status in dict(Order.OrderStatus.choices):
            order.order_status = new_status
            order.save()
            return redirect('employee_order_details', order_id=order_id)


@permission_required('core.employee', login_url='login/')
def employee_order_details_view(request, order_id):
    current_time = getattr(request, 'current_time', None)
    order = Order.objects.get(pk=order_id)
    form = ChangeOrderStatusForm(request.POST or None, instance=order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('order_details', order_id=order_id)
    context = {
        'order': order,
        'order_items': order.orderitem_set.all(),  # Assuming OrderItem model has a ForeignKey to Order
        'order_statuses': Order.OrderStatus.choices,  # Assuming OrderStatus is a Choices enum in Order model
        'form': form,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'orders/employee_order_details.html', context)


# todo: empty
@permission_required('core.customer', login_url='login/')
def customer_orders_view(request):
    current_time = getattr(request, 'current_time', None)
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(user=customer)
    context = {
        'orders': orders,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'orders/customer_orders.html', context)


@permission_required('core.employee', login_url='login/')
def manage_orders_view(request):
    current_time = getattr(request, 'current_time', None)
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }
    return render(request, 'orders/manage_orders.html', context)


@permission_required('core.employee', login_url='login/')
def order_statistics_view(request):
    current_time = getattr(request, 'current_time', None)
    total_orders = Order.objects.count()

    # Calculate the number of orders per status
    orders_per_status = Order.objects.values('order_status').annotate(count=Count('order_status'))

    # Calculate total revenue
    total_revenue = Order.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue']

    # Prepare context
    context = {
        'total_orders': total_orders,
        'orders_per_status': orders_per_status,
        'total_revenue': total_revenue,
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        'current_time': current_time
    }

    return render(request, 'orders/orders_statistics.html', context)


@permission_required('core.employee', login_url='login/')
def order_status_distribution(request):
    # Query the database for order statuses
    statuses = Order.objects.values_list('order_status', flat=True)

    # Count occurrences of each status
    status_counts = {
        'Pending': 0,
        'Accepted': 0,
        'Completed': 0,
    }

    for status in statuses:
        if status == Order.OrderStatus.Pending:
            status_counts['Pending'] += 1
        elif status == Order.OrderStatus.Accepted:
            status_counts['Accepted'] += 1
        elif status == Order.OrderStatus.Completed:
            status_counts['Completed'] += 1

    # Generate the pie chart
    labels = status_counts.keys()
    sizes = status_counts.values()
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.1, 0, 0)  # explode 1st slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    # Return the pie chart as an HTTP response
    return HttpResponse(buf, content_type='image/png')


def reviews_view(request):
    current_time = getattr(request, 'current_time', None)
    reviews = Review.objects.all()
    is_employee = request.user.has_perm('core.employee')
    is_customer = request.user.has_perm('core.customer')
    is_authenticated = is_employee or is_customer
    context = {
        'is_customer': is_customer,
        'is_employee': is_employee,
        'is_authenticated': is_authenticated,
        current_time: current_time,
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context)


@permission_required('core.customer', login_url='login/')
def add_review_view(request):
    current_time = getattr(request, 'current_time', None)
    context = {
        'is_customer': request.user.has_perm('core.customer'),
        'is_employee': request.user.has_perm('core.employee'),
        current_time: current_time
    }
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            review = form.save(commit=False)
            review.user = customer
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
        context['form'] = form
    return render(request, 'reviews/add_review.html', context)
