from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('signup/',views.signup,name='signup'),
	path('items/',views.item_list,name='item-list'),
	path('items/<int:pk>/',views.item_detail.as_view(),name='item-detail'),
	path('bids/',views.bid_list,name='bid-list'),
	path('bids/<int:pk>',views.bid_detail,name='bid-detail'),
	path('items/<int:pk>/add-bid',views.add_bid,name='add-bid'),
	path('bids/<int:pk>/update-bid',views.update_bid,name='update-bid'),
	path('bids/<int:pk>/delete-bid',views.delete_bid.as_view(),name='delete-bid'),
	path('items/add-item',views.add_item,name='add-item'),
	path('result/',views.result,name='result'),
	path('profile/',views.profile,name='profile'),
	path('items/<int:pk>/test',views.item_test,name='item-test'),
]