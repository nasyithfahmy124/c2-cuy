from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormDonasi
from petani.models import Project

# Create your views here.
@login_required
def home_page(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'donatur/home_d.html', {
        'projects': projects
    })


@login_required
def danai_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = FormDonasi(request.POST)
        if form.is_valid():
            jumlah = form.cleaned_data['jumlah']
            sisa = project.target_dana - project.dana_terkumpul
            if jumlah > sisa:
                form.add_error('jumlah', f'Maksimal donasi: {sisa}')
            else:
                funding = form.save(commit=False)
                funding.donatur = request.user
                funding.project = project
                funding.save()
                project.dana_terkumpul += jumlah
                if project.dana_terkumpul >= project.target_dana:
                    project.status = 'selesai'
                else:
                    project.status = 'aktif'

                project.save()

                return redirect('home_d')
    else:
        form = FormDonasi()

    return render(request, 'donatur/donasi.html', {
        'form': form,
        'project': project
    })