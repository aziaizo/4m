from django.shortcuts import render
from products.models import Product,Review,Category


# Create your views here.

def main(request):
    if request.method =='GET':
        return render(request, ' layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        category_id=request.GET.get('category_id')
        if category_id:
            products=Product.objects.filter(category=Category.objects.get(id=category_id))
        else:
            products=Product.objects.all()

        context= {
            'products': products,


        }
        return render(request, 'products/products.html', context=context)



def product_detail_view(request,id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        reviews=Review.objects.filter(product=product)
        context = {
            'product':product,
            'reviews':reviews
        }

        return render(request, 'products/detail.html',context=context)

def categories_view(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all()}
        return render(request, 'categories/category.html', context=context)