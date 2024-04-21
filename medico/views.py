from django.shortcuts import render, redirect
from . models import Especialidades, DadosMedico, DatasAbertas, is_medico
from django.contrib.messages import add_message, constants
from datetime import datetime


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
        # if request.user is None:
        #     return redirect('/usuarios/login')

        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao= request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            cedula_identidade_medica=cim,
            rg=rg,
            foto=foto,
            especialidade_id=especialidade,
            descricao=descricao,
            valor_consulta=valor_consulta,
            user=request.user
        )

        dados_medico.save()
        add_message(request, constants.SUCCESS, 'Cadastro Médico realizado com sucesso')
        return redirect('/medico/abrir_horario')


def abrir_horario(request):
    if not is_medico(request.user):
        add_message(request, constants.WARNING, 'Somente médicos podem abrir horários')
        return redirect('/usuarios/sair')

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {
            "dados_medico": dados_medicos,
            "datas_abertas": datas_abertas  
        })
    
    if request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        if data_formatada <= datetime.now():
            add_message(request, constants.WARNING, "A data não pode ser anterior a data atual")
            return redirect('/medico/abrir_horario')
        
    horario_abrir = DatasAbertas(
        data=data,
        user=request.user,
    )

    horario_abrir.save()

    add_message(request, constants.SUCCESS, "Horario cadastrado com sucesso")
    return redirect('/medico/abrir_horario')
