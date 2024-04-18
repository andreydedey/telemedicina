from django.shortcuts import render, redirect
from . models import Especialidades, DadosMedico, is_medico
from django.contrib.messages import add_message, constants


# Create your views here.
def cadastro_medico(request):
    if request.method == "GET":
        if is_medico(request.user):
            add_message(request, constants.WARNING, "Você já é médico")
            return redirect('/medicos/abrir_horario')

        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {
            "especialidades": especialidades
        })
    
    if request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('cim')
        descricao= request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            cim=cim,
            rg=rg,
            foto=foto,
            especialidade=especialidade.id,
            descricao=descricao,
            valor_consulta=valor_consulta,
            user=request.user
        )

        dados_medico.save()
        add_message(request, constants.SUCCESS, 'Cadastro Médico realizado com sucesso')
        return redirect('/medicos/abrir_horario')
