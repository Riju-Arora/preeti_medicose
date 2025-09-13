# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Product


# 🏠 Home Page
def home(request):
    return render(request, 'shop/index.html')


# 📦 Products Page with Search, Filter & Pagination
from django.core.paginator import Paginator

def products(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "all")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    products = Product.objects.all()

    # 🔍 Apply search
    if query:
        products = products.filter(name__icontains=query)

    # 🔍 Apply category
    if category != "all":
        products = products.filter(category__iexact=category)

    # 🔍 Apply price filter
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # 🔍 Apply sorting
    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-id")

    # ✅ Pagination (6 per page)
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)

    return render(request, "shop/products.html", {
        "page_obj": page_obj,
        "products": page_obj,   # keep for compatibility
    })



# 🛒 Add to Cart
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    return redirect("cart")


# ➕➖ Update Cart Quantity
def update_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart and request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            cart[product_id] += 1
        elif action == "decrease":
            if cart[product_id] > 1:
                cart[product_id] -= 1
            else:
                # remove item if quantity is 0
                del cart[product_id]

        request.session["cart"] = cart

    return redirect("cart")


# ❌ Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("cart")


# 🛍️ Cart Page
def cart(request):
    cart = request.session.get("cart", {})
    cart_items, total = [], 0

    for product_id, quantity in list(cart.items()):
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
        except Product.DoesNotExist:
            del cart[product_id]
            request.session["cart"] = cart

    return render(request, "shop/cart.html", {"cart_items": cart_items, "total": total})


# ✅ Checkout (WhatsApp Order)
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart")

    cart_items, total, total_savings = [], 0, 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        # 💰 Calculate savings if MRP > Price
        savings = 0
        if product.mrp and product.mrp > product.price:
            savings = (product.mrp - product.price) * quantity
            total_savings += savings

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
            "savings": savings
        })

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # 📲 WhatsApp Message
        order_text = f"🛒 New Order from Preeti Medicose%0A%0A"
        for i, item in enumerate(cart_items, start=1):
            order_text += f"{i}. {item['product'].name} - ₹{item['product'].price} x {item['quantity']} = ₹{item['subtotal']}%0A"
            if item["savings"] > 0:
                order_text += f"   ✅ You Saved: ₹{item['savings']}%0A"
        order_text += f"%0A💰 Total: ₹{total}%0A"
        if total_savings > 0:
            order_text += f"🎉 Total Savings: ₹{total_savings}%0A"
        order_text += f"%0A👤 Name: {name}%0A📞 Phone: {phone}%0A🏠 Address: {address}"

        whatsapp_number = "919350050904"
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={order_text}"

        # ✅ Clear cart after order
        request.session["cart"] = {}

        return render(request, "shop/thank_you.html", {
            "whatsapp_url": whatsapp_url,
            "total_savings": total_savings
        })

    return render(request, "shop/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "total_savings": total_savings
    })



# ✅ Thank You Page
def thank_you(request):
    return render(request, "shop/thank_you.html")
