from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmarSenha = request.POST.get('confirmar_senha')

        if senha != confirmarSenha:
            messages.add_message(request, constants.ERROR, "A senha e confirmar Senha devem ser iguais.")
            return redirect('/usuarios/cadastro/')
        
        if len(senha) < 6:
            messages.add_message(request, messages.ERROR, "Asenha deve ter mais de seis digitos")
            return redirect('/usuarios/cadastro/')

        users = User.objects.filter(username = username)    
        if users.exists():
            messages.add_message(request, messages.ERROR, "Já exite um usuário cadastrado com esse username.")
            return redirect('/usuarios/cadastro/')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = senha
        )
        
        return redirect('/usuarios/login/')
        #return HttpResponse('Usuário criado com sucesso!!')
        #return HttpResponse(f'{username} - {email} - {senha} - {confirmarSenha}')

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username = username, password = senha)
        if user:
            auth.login(request, user)
            return redirect('/pacientes/home/')
        
        messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos!")
        return redirect('/usuarios/login/')
    
def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login/')