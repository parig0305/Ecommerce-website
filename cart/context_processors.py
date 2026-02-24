from .models import Cart


def cart_count(request):
    """Add cart count to all templates"""
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()
        
        if cart:
            return {'cart_count': cart.get_item_count()}
    except:
        pass
    
    return {'cart_count': 0}
