from django.urls import path
from .import views
urlpatterns=[
    path('',views.product_View.as_view(),name='index'),
    path('mybidding:<int:pk>',views.mybiddingView.as_view(),name='mybidding'),
    path('profile',views.myprofile.as_view(),name='profile'),
    path('update-profile',views.get_updated,name='get_update'),
    path('my-bidding',views.get_details.as_view(),name='get_details'),
    path('listing',views.listing_page.as_view(),name='listing_page')
]