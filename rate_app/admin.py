from django.contrib import admin
from .models import Tbl_User, Tbl_Movie, Tbl_Rating

# Register your models here.
admin.register(Tbl_User)
admin.site.register(Tbl_Movie)
admin.site.register(Tbl_Rating)
