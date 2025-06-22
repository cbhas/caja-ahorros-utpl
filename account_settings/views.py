from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        user.phone = request.POST.get('telefono')
        user.address = request.POST.get('direccion')

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()

    return render(request, 'account_settings/profile.html', {
        'client': user
    })

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            request.user.profile_picture = request.FILES['profile_picture']
            request.user.save()
            return JsonResponse({'success': True, 'message': 'Foto de perfil actualizada correctamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error al actualizar la foto de perfil'})
    return JsonResponse({'success': False, 'message': 'No se proporcionó ninguna imagen'})