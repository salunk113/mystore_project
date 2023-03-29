from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from customer.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from api.models import Products,Carts
from django.db.models import Sum

class SignUpView(CreateView):
    template_name="signup.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"account created success fully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"account creation failed")

        return super().form_invalid(form)


class SigninView(FormView):
    template_name="cust-login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("user-home")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"cust-login.html",{"form":form})

class HomeView(ListView):
    template_name="cust-index.html"
    context_object_name="products"
    model=Products



class ProductDetailView(DetailView):
    template_name="cust-productdetail.html"
    context_object_name="product"
    pk_url_kwarg="id"
    model=Products


def addto_cart(request,*args,**kwargs):
    id=kwargs.get("id")
    product=Products.objects.get(id=id)
    user=request.user
    Carts.objects.create(user=user,product=product)
    messages.success(request,"item hasbeen added to cart")
    return redirect("user-home")


class CartListView(ListView):
    template_name="cart-list.html"
    model=Carts
    context_object_name="carts"

    def get(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user)
        total=Carts.objects.filter(user=request.user).aggregate(tot=Sum("products__price"))
        return render(request,"cart-list.html",{"carts":qs,"total":total})

    # def get_queryset(self):
    #     return Carts.objects.filter(user=self.request.user)



# form_valid(),get_query_set()