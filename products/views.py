from django.shortcuts import render, redirect
from products.models import Product,Review,Category
from products.forms import ProductCreateForm,ReviewCreateForm

# Create your views here.

PAGINATION_LIMIT=3

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
        search=request.GET.get('search')
        page=int(request.GET.get('page', 1))

        if search is not None:
            products=Product.objects.filter(
                title__icontains=search
            )

        max_page=products.__len__()/PAGINATION_LIMIT

        if round(max_page)<max_page:
            max_page=round(max_page)+1
        else:
            max_page=round(max_page)

        products=products[PAGINATION_LIMIT*(page-1):PAGINATION_LIMIT*page]

        context= {
            'products': products,
            'user':request.user,
            'max_page':range(1,max_page+1)
        }
        return render(request, 'products/products.html', context=context)



def product_detail_view(request,id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        reviews=Review.objects.filter(product=product)
        context = {
            'product':product,
            'reviews':reviews,
            'form': ReviewCreateForm
        }

        return render(request, 'products/detail.html',context=context)
    if request.method == "POST":
        product = Product.objects.get(id=id)
        reviews = Review.objects.filter(product=product)
        form=ReviewCreateForm(data=request.POST)

    if form.is_valid():
        Review.objects.create(
            author_id=request.user.id,
            product=product,
            text=form.cleaned_data.get('text')
        )
        return redirect(f'/products/{product.id}')
    return render(request,'products/detail.html',context={
        'product':product,
        'reviews':reviews,
        'form':form

    })

def categories_view(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all()}
        return render(request, 'categories/category.html', context=context)

def create_post_view(request):
    if request.method == 'GET' and not request.user.is_anonymous:
        context = {
            'form':ProductCreateForm
        }
        return render(request,'products/create.html',context=context)
    elif request.user.is_anonymous:
        return redirect('/products')


    if request.method =='POST':
        form=ProductCreateForm(data=request.POST)


        if form.is_valid():
            Product.objects.create(
                author_id=request.user.id,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                year_of_release=form.cleaned_data['year_of_release'] if form.cleaned_data['year_of_release'] is not None else 2023
            )
            return redirect('/products/')
        return render(request,'products/create.html', context={
            'form':form
        })