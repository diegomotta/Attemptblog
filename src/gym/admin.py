from django.contrib import admin
from  .models import Post



class AdminPost(admin.ModelAdmin):
	list_display = ["__str__","title","content"]
	search_fields=["title","content"]
	list_editable=["title"]
	class Meta:
		model = Post
admin.site.register(Post,AdminPost)


