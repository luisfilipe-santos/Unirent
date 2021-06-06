from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Propriedade)
admin.site.register(Inquilino)
admin.site.register(Senhorio)
admin.site.register(Oferta)
admin.site.register(Message)
admin.site.register(Contrato)
admin.site.register(Review)
admin.site.register(ReviewUser)