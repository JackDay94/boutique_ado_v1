from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity  # Find item id and item size and set its quantity
        else:
            del bag[item_id]['items_by_size'][size]  # Remove item if quantity less than 1
            if not bag[item_id]['items_by_size']: 
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity  # Add item with item id
        else:
            bag.pop(item_id)  # Remove item with item id

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]  # Delete item with a specific size
            if not bag[item_id]['items_by_size']: 
                bag.pop(item_id)  # Remove entire item_id if only size in bag
        else:
            bag.pop(item_id)  # Remove item with item id

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)


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
