from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Item(models.Model):
	item_name = models.CharField(max_length=200,help_text='Enter the name of the item')
	item_image = models.ImageField()
	base_price = models.IntegerField(help_text='Enter the base price of the item')
	item_description = models.CharField(max_length=200,help_text='Describe the item')
	item_created = models.DateTimeField(editable=False)
	item_owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
	item_close = models.DateTimeField(default=timezone.now)

	option = (
		('g', 'General'),
		('h', 'Household'),
		('e', 'Electronics'),
		('f', 'Food'),
		('c', 'Clothing'),
	)

	item_category = models.CharField(max_length=1, choices=option,blank=True)

	def __str__(self):
		return self.item_name

	def get_absolute_url(self):
		return reverse('item-detail', args=[str(self.id)])

	def get_winner(self):
		bids_list = Bid.objects.filter(item=self).order_by('-bid_amount','bid_created')
		if bids_list:
			item_owner = bids_list[0].bidder
			return bids_list[0].bidder
		else:
			return None

	def test_view(self):
		now = timezone.now()
		naive = self.item_close
		delta = naive-now
		ts = int(delta.total_seconds())
		if (ts<=0):
			return ""
		else:
			return ts;

	def get_time_left(self):
		now = timezone.now()
		naive = self.item_close
		delta = naive-now
		ts = int(delta.total_seconds())
		if (ts<=0):
			return ""
		else:
			days = int(ts/86400)
			hours = int((ts%86400)/3600)
			minutes = int((ts%3600)/60)
			seconds = int((ts%60)/1)
			arr = [days,hours,minutes,seconds]
			letters = "dhms"
			anything = False
			output = ""
			for i in range(4):
				if arr[i]: 
					anything = True
				if anything:
					output += (str(arr[i])+letters[i]+" ")
			return output[:-1]

	def get_current_bid(self):
		bids_list = Bid.objects.filter(item=self).order_by('-bid_amount','bid_created')
		if len(bids_list) == 0:
			return self.base_price
		else:
			return bids_list[0]

	def save(self, *args, **kwargs):
		if not self.id:
			self.item_created = timezone.now()
		return super(Item, self).save(*args, **kwargs)

class Bid(models.Model):
	bid_amount = models.IntegerField(help_text='how much you want to bid')
	item = models.ForeignKey(Item,on_delete=models.CASCADE,null=True,blank=True)
	bidder = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	bid_created = models.DateTimeField(editable=False,default=timezone.now)

	def __str__(self):
		return str(self.bid_amount)

	def get_absolute_url(self):
		return reverse('bid-detail', args=[str(self.id)])

	def save(self, *args, **kwargs):
		if not self.id:
			self.bid_created = timezone.now()
		return super(Bid, self).save(*args, **kwargs)