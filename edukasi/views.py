from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import KategoriEdukasi, MateriEdukasi

@login_required
def pusat_edukasi(request, slug=None):
    user_role = getattr(request.user, 'role', 'semua')
    user_role = user_role.lower() if user_role else 'semua'

    kategori_list = KategoriEdukasi.objects.all().prefetch_related('materi')

    materi_list = MateriEdukasi.objects.filter(
        target_role__in=['semua', user_role]
    ).order_by('urutan')
    if slug:
        materi_aktif = MateriEdukasi.objects.filter(
            slug=slug,
            target_role__in=['semua', user_role]
        ).first()
    else:
        materi_aktif = materi_list.first()
    if not materi_aktif:
        materi_aktif = MateriEdukasi.objects.first()

    context = {
        'kategori_list': kategori_list,
        'materi_list': materi_list,
        'materi_aktif': materi_aktif,
        'role': user_role
    }

    return render(request, 'edukasi/docs.html', context)