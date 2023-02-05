from django.shortcuts import render, redirect
from products.models import Product,Review,Category
from products.forms import ProductCreateForm,ReviewCreateForm
from django.views.generic import ListView,CreateView,DetailView
# Create your views here.

PAGINATION_LIMIT=3

class MainView(ListView):
    model=Product

class ProductView(ListView):
    model=Product
    def get(self,request,**kwargs):
        category_id = request.GET.get('category_id')
        if category_id:
            products = Product.objects.filter(category=Category.objects.get(id=category_id))
        else:
            products = self.get_queryset()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search is not None:
            products = Product.objects.filter(
                title__icontains=search
            )

        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'products': products,
            'user': request.user,
            'max_page': range(1, max_page + 1)
        }
        return render(request, self.template_name, context=context)


class ProductDetailView(DetailView,CreateView):
    queryset = Product.objects.all()
    model =Product
    form_class = ReviewCreateForm
    pk_url_kwarg = 'id'


    def get_context_data(self, **kwargs):

        return {
            'product': self.get_object(),
            'reviews': Review.objects.filter(product=self.get_object()),
            'form': kwargs.get('form',self.form_class),



        }

    def post(self,request,*args,**kwargs):
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author_id=request.user.id,
                product=self.get_object(),
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{self.get_object().id}')
        return render(request, self.template_name, context=self.get_context_data(form=form))


class CategoriesView(ListView):
    model = Category

    def get(self,request,**kwargs):
        context = {
            'categories': Category.objects.all()}
        return render(request, self.template_name, context=context)

class CreateProductView(CreateView):
    def get(self,request,**kwargs):
        if not request.user.is_anonymous:
            context = {
                'form': ProductCreateForm
            }
            return render(request, self.template_name, context=context)
        elif request.user.is_anonymous:
            return redirect('/products')

    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(request.POST, request.FILES)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                author_id=request.user.id,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                year_of_release=form.cleaned_data['year_of_release'] if form.cleaned_data[
                                                                            'year_of_release'] is not None else 2023
            )
            return redirect('/products/')
        return render(request, 'products/create.html', context={
            'form': form
        })



