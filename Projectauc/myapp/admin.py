from django.contrib import admin
from .models import product,Buyer,bidding
# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display=['pro_id','title','base_price','category','status','verified','auction_start','auction_expiration']
admin.site.register(product,productAdmin)

class biddingAdmin(admin.ModelAdmin):
    list_display=['current_price','bid_date','updated_price']
admin.site.register(bidding,biddingAdmin)


class BuyerAdmin(admin.ModelAdmin):
    list_display=['user','doc_type','valid_doc','contact','address','gender','verified']
admin.site.register(Buyer,BuyerAdmin)