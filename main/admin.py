from django.contrib import admin
from .models import Author , Article , Category , Comments , Tags, Likes, PageHit

admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Tags)
admin.site.register(Likes)
admin.site.register(PageHit)

# Register your models here.
