from django.contrib import admin
from .models import title,casts,actees,direct,comedian,music,sho,genre,MovieTitleGenres
# Register your models here.

admin.site.register(title)
admin.site.register(actees)
admin.site.register(direct)
admin.site.register(comedian)
admin.site.register(music)
admin.site.register(sho)
admin.site.register(genre)
admin.site.register(MovieTitleGenres)



@admin.register(casts)
class MovieTitleAdmin(admin.ModelAdmin):
    list_display = ('actor_id','actor', 'date_of_birth', 'debut_movie','debut_year','img')

