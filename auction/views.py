from django.shortcuts import render,get_object_or_404
from django.contrib.auth import login,authenticate
from .forms import SignUpForm,BidForm,ItemForm
from . models import Item,Bid
from django.contrib.auth.decorators import login_required

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username,password=raw_password)
			login(request,user)
			item_count = Item.objects.all().count()
			bid_count = Bid.objects.all().count()
			return render(request,'auction/index.html',{'item_count':item_count,'bid_count':bid_count})
	else:
		form = SignUpForm()
	return render(request,'auction/signup.html',{'form':form})


def index(request):
	item_count = Item.objects.all().count()
	bid_count = Bid.objects.all().count()

	return render(request,'auction/index.html',{'item_count':item_count,'bid_count':bid_count})

@login_required
def add_item(request):
	form = ItemForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		item = Item()
		item.item_name = form.cleaned_data.get('item_name')
		item.base_price = form.cleaned_data.get('base_price')
		item.item_description = form.cleaned_data.get('item_description')
		item.item_image = request.FILES['item_image']
		item.item_category = form.cleaned_data.get('item_category')
		item.item_close = form.cleaned_data.get('item_close')
		item.save()
		item_list = Item.objects.all()
		return render(request,'auction/item_list.html',{'item_list':item_list})
	return render(request,'auction/create_item.html',{'form':form})

@login_required
def add_bid(request,pk):
	item = get_object_or_404(Item,pk=pk)
	form = BidForm(request.POST or None)
	if item.get_time_left():
		if form.is_valid():
			data = form.cleaned_data.get('bid_amount')
			if data < item.base_price:
				context = {
					'form':form,
					'error_message': 'Bid amount should be greater than base price',
				}
				return render(request,'auction/create_bid.html',context)
			bid = form.save()
			bid.item = item
			bid.bidder = request.user
			bid.save()
			bid_count = Bid.objects.all().count()
			item_count = Item.objects.all().count()
			return render(request,'auction/item_detail.html',{'item':bid.item})
		return render(request,'auction/create_bid.html',{'form':form})
	context = {
		'form':form,
		'error_message': 'Bid is over',
	}
	return render(request,'auction/create_bid.html',context)

@login_required
def update_bid(request,pk):
	bid = get_object_or_404(Bid,pk=pk)
	form = BidForm(request.POST or None)
	if bid.item.get_time_left():
		if form.is_valid():
			data = form.cleaned_data.get('bid_amount')
			if data < bid.item.base_price:
				context = {
					'form':form,
					'error_message': 'Bid amount should be greater than base price',
				}
				return render(request,'auction/create_bid.html',context)
			bid.bid_amount=form.cleaned_data.get('bid_amount')
			bid.save()
			return render(request,'auction/bid_detail.html',{'bid':bid})
		return render(request,'auction/create_bid.html',{'form':form})
	context = {
		'form':form,
		'error_message': 'Bid amount should be greater than base price',
	}
	return render(request,'auction/create_bid.html',context)

from django.views import generic
from django.db.models import Q

def item_list(request):
	query = request.GET.get("q")
	if query:
		item_list = Item.objects.filter(
			Q(item_name__icontains=query)
		).distinct()
		return render(request,'auction/item_list.html',{'item_list':item_list})
	category = request.POST.get('category')
	if not category:
		category = 'all'
	if category == 'all':
		item_list = Item.objects.all()
	else:
		item_list = Item.objects.filter(item_category=category)
	item_list = [item for item in item_list]
	sort = request.POST.get('sort')
	if sort:
		if sort == 'cheap':
			item_list.sort(key=lambda item: item.base_price)
		elif sort == 'exp':
			item_list.sort(key=lambda item: item.base_price, reverse=True)
		else:
			item_list.sort(key=lambda item: item.item_created, reverse=True)
	return render(request,'auction/item_list.html',{'item_list':item_list})

class item_detail(generic.DetailView):
	model = Item

@login_required
def bid_list(request):
	bid_list = Bid.objects.filter(bidder=request.user)
	return render(request,'auction/bid_list.html',{'bid_list':bid_list})

@login_required
def bid_detail(request,pk):
	bid = get_object_or_404(Bid,pk=pk)
	return render(request,'auction/bid_detail.html',{'bid':bid})

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

class delete_bid(DeleteView):
	model = Bid
	success_url = reverse_lazy('bid-list')

import datetime

def result(request):
	item_list = Item.objects.all()
	for item in item_list:
		if datetime.date.today() > item.item_created:
			win = 0
			bid_list = item.bid_set.all()
			for bid in bid_list:
				if bid.bid_amount > win:
					item.item_owner = bid.bidder
					win = bid.bid_amount
			item.save()
	return render(request,'auction/item_list.html',{'item_list':item_list})

@login_required
def profile(request):
	item_list = Item.objects.all()
	winning_items = []
	beaten_items = []
	for item in item_list:
		bid = Bid.objects.filter(bidder=request.user, item=item)
		if bid:
			if item.get_winner() == request.user:
				winning_items.append(item)
			else:
				beaten_items.append(item)
	return render(request,'auction/profile.html',{'winning_items':winning_items,'beaten_items':beaten_items})

def item_test(request,pk):
	item = get_object_or_404(Item,pk=pk)
	return render(request,'auction/test.html',{'item':item})