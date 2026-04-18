from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormDonasi
from petani.models import Project
from django.db.models import Sum
from .models import Donasi
from django.contrib import messages
# Create your views here.
@login_required
def home_page(request):
    projects = Project.objects.filter(status='aktif').annotate(
        total_donasi=Sum('donasi__jumlah')
    ).order_by('-total_donasi')

    # fallback kalau None → jadi 0
    for p in projects:
        if p.total_donasi is None:
            p.total_donasi = 0

    total_dana = Donasi.objects.aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    total_project = projects.count()
    total_petani = Project.objects.values('petani').distinct().count()

    return render(request, 'donatur/home_d.html', {
        'projects': projects,
        'total_dana': total_dana,
        'total_project': total_project,
        'total_petani': total_petani
    })

# @login_required
# def danai_project(request, id):
#     project = get_object_or_404(Project, id=id)

#     if project.status != 'aktif':
#         return redirect('home_d')  # atau tampilkan error

#     if request.method == 'POST':
#         form = FormDonasi(request.POST)
#         if form.is_valid():
#             jumlah = form.cleaned_data['jumlah']
#             sisa = project.target_dana - project.dana_terkumpul

#             if jumlah > sisa:
#                 form.add_error('jumlah', f'Maksimal donasi: {sisa}')
#             else:
#                 funding = form.save(commit=False)
#                 funding.donatur = request.user
#                 funding.project = project
#                 funding.save()

#                 project.dana_terkumpul += jumlah

#                 if project.dana_terkumpul >= project.target_dana:
#                     project.status = 'selesai'
#                 else:
#                     project.status = 'aktif'

#                 project.save()

#                 return redirect('home_d')
#     else:
#         form = FormDonasi()

#     return render(request, 'donatur/donasi.html', {
#         'form': form,
#         'project': project
#     })

@login_required
def danai_project(request, id):
    project = get_object_or_404(Project, id=id)

    if project.status != 'aktif':
        return redirect('home_d')

    if request.method == 'POST':
        form = FormDonasi(request.POST)
        if form.is_valid():
            jumlah = form.cleaned_data['jumlah']

            # hitung total REAL dari database
            total = Donasi.objects.filter(project=project).aggregate(
                Sum('jumlah')
            )['jumlah__sum'] or 0

            sisa = project.target_dana - total

            if jumlah > sisa:
                form.add_error('jumlah', f'Maksimal donasi: {sisa}')
            else:
                funding = form.save(commit=False)
                funding.donatur = request.user
                funding.project = project
                funding.save()

                # cek status
                total_baru = total + jumlah
                if total_baru >= project.target_dana:
                    project.status = 'selesai'
                else:
                    project.status = 'aktif'

                project.save()
                messages.success(request,'Bantuan berhasil dikirim, terima kasih atas partisipasi anda!')
                return redirect('home_d')
    else:
        form = FormDonasi()

    return render(request, 'donatur/donasi.html', {
        'form': form,
        'project': project
    })

@login_required
def lihat_laporan(request, id):
    project = get_object_or_404(Project, id=id)
    laporan = project.laporan.all().order_by('-tanggal')

    return render(request, 'donatur/laporan_fp.html', {
        'project': project,
        'laporan': laporan
    })
    
@login_required
def detail(request, id):
    det = get_object_or_404(Project, id=id)

    total = Donasi.objects.filter(project=det).aggregate(
        Sum('jumlah')
    )['jumlah__sum'] or 0

    return render(request, 'donatur/detail.html', {
        'detail': det,
        'total_donasi': total
    })

