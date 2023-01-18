from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:  # checks if a product with sizes is added to bag
        if item_id in list(bag.keys()):  # checks if an item with the item id is already in bag
            if size in bag[item_id]['items_by_size'].keys():  # checks if an item with the same id and size is in bag
                bag[item_id]['items_by_size'][size] += quantity  # increments the quantity for the item with same size
            else:
                bag[item_id]['items_by_size'][size] = quantity  # sets the item quantity to quantity for item with different size
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}  # adds item to bag if not already in bag
    else:  # runs if a product without a size is added to bag
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
