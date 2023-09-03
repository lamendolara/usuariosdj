from typing import Any, Dict
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse  #lazy sirve para poder acceder a urls desde el "name".
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.http import HttpResponseRedirect

from django.views.generic import (
    View,
    CreateView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserResgisterForm, 
    LoginForm,
    UpdatePasswordForm,
    VerificationForm,
)

from .models import User
#
from .functions import code_generator

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserResgisterForm
    success_url = '/' #le puse "/register/" y me devuelve a la pagina de registro y no da errores.

    #Para que haga el proceso de guardado los forms necesitan el metodo forms_valid
    def form_valid(self, form):
        # generamos el código
        codigo = code_generator()
        print("******************") 
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo
        )
        # enviar el codigo al email del usuario
        asunto = 'Confirmación de e-mail'
        mensaje = 'Código de verificación: ' + codigo
        email_remitente = 'lamendolara@gmail.com'
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],] )
        # Una vez confirmado reedirigir a pantalla de validacion, donde el nuevo usuario colocara el codigo para validarlo.
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        ) 



        return super(UserRegisterView, self).form_valid(form)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):

        print("******************") 
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )

        login(self.request,user)
        
        return super(LoginUser, self).form_valid(form)
    
class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        """Se comprueba que el usuario actual sea correcto y se cambia la contraseña por una nueva"""

        print("******************")
        usuario = self.request.user  #verifica el usuario actual 
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1'],
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        
        logout(self.request)
        
        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        #
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        
        return super(CodeVerificationView, self).form_valid(form)


