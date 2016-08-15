from django.conf.urls import url

# Basic
from api.views import HomeView, TimestampView
urlpatterns = [
    url(r'^/?$',    HomeView.as_view()),
    url(r'^ts/?$',  TimestampView.as_view()),
]


# Test
from api.views import TestView
urlpatterns += [
    url(r'^test/?$',            TestView.as_view()),
]


# User
from user.views import UserRegisterView, UserLoginView, \
                       UserLogoutView, UserChangePWView, UserInfoView,\
                       UserBankAccountView, UserTreeView
urlpatterns += [
    url(r'^user/register/?$',       UserRegisterView.as_view()),  # POST
    url(r'^user/login/?$',          UserLoginView.as_view()),     # POST
    url(r'^user/logout/?$',         UserLogoutView.as_view()),    # POST
    url(r'^user/password/?$',       UserChangePWView.as_view()),  # PUT

    # GET  : Get user's info.
    # POST : Create or update user info.
    url(r'^user/info/?$',           UserInfoView.as_view()),

    # POST : Create or update bank account
    # PUT  : Enable bank account
    url(r'^user/bank_account/?$',   UserBankAccountView.as_view()),

    url(r'^user/tree/?$',           UserTreeView.as_view()), # GET
]

# Order
from order.views import UserOrderView
urlpatterns += [
    url(r'^user/order/?$',             UserOrderView.as_view()),
]

# Product
from product.views import ProductView, ProductCategoryView, ProductDateView,\
                          ProductPriceView
urlpatterns += [
    url(r'^product/?$',             ProductView.as_view()),
    url(r'^product/category/?$',    ProductCategoryView.as_view()),
    url(r'^product/date/?$',        ProductDateView.as_view()),
    url(r'^product/price/?$',       ProductPriceView.as_view()),
]




