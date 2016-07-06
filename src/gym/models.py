from __future__ import unicode_literals
from django.core.urlresolvers import reverse 
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

class PostManagerTitle(models.Manager):
	def get_query_set(self): 
		return super(PostManagerTitle, self).get_query_set().filter(title='Tester') 

def upload_location(instance,filaname):
	return "%s/%s" %(instance.slug, filaname)
	
class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location,blank=True,null=True, width_field="width_field", height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	publish = models.DateField(blank=True,null=True,auto_now=False, auto_now_add=False)

	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
	created_at = models.DateTimeField(auto_now=False,auto_now_add=True)
	objects = models.Manager() #MANAEJADOR PREDETERMINADO
	contentss = PostManagerTitle();
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:post-detail", kwargs={'slug': self.slug})
		
	class Meta:
		ordering = ["-id","-created_at","-updated_at"]
		
def create_slug(instance,new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().pk)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)