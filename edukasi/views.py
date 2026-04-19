from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import KategoriEdukasi, MateriEdukasi

@login_required
def pusat_edukasi(request, slug=None):
    user_role = request.user.role 
    kategori_list = KategoriEdukasi.objects.all()
    materi_tersedia = MateriEdukasi.objects.filter(target_role__in=['semua', user_role])
    materi_aktif = None
    if slug:
        materi_aktif = get_object_or_404(MateriEdukasi, slug=slug, target_role__in=['semua', user_role])
    else:
        materi_aktif = materi_tersedia.first()

    context = {
        'kategori_list': kategori_list,
        'materi_list': materi_tersedia,
        'materi_aktif': materi_aktif,
    }
    
    return render(request, 'edukasi/docs.html', context)