from django.contrib import admin
from .models import KategoriEdukasi, MateriEdukasi

class MateriEdukasiAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'target_role', 'updated_at')
    list_filter = ('kategori', 'target_role')
    search_fields = ('judul',)
    prepopulated_fields = {'slug': ('judul',)} 
    
admin.site.register(KategoriEdukasi)
admin.site.register(MateriEdukasi, MateriEdukasiAdmin)