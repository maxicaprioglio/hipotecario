import requests
from django.http import JsonResponse
from django.shortcuts import render
from .forms import FormularioCredito
from .models import Consulta
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect   

def pagina_inicio(request):
    if request.method == 'POST':
        form = FormularioCredito(request.POST)
        if form.is_valid():
            # obtengo los datos del formulario
            nombre = form.cleaned_data['nombre']
            edad = form.cleaned_data['edad']
            email = form.cleaned_data['email']
            celular = form.cleaned_data['celular']
            tipo_empleo = form.cleaned_data['tipo_empleo']
            antiguedad_laboral = form.cleaned_data['antiguedad_laboral']
            bruto = form.cleaned_data['bruto']
            propiedad = form.cleaned_data['propiedad']
            ahorros = form.cleaned_data['ahorros']
            plazo = form.cleaned_data['plazo']
            prestamo = propiedad - ahorros
            
            # guardo los datos en la base de datos
            consulta = Consulta(
                nombre=nombre,
                edad=edad,
                email=email,
                celular=celular,
                tipo_empleo=tipo_empleo,
                antiguedad_laboral=antiguedad_laboral,
                bruto=bruto,
                propiedad=propiedad,
                ahorros=ahorros,
                plazo=plazo
            )
            try:
                consulta.save()
            except Exception as e:
                return JsonResponse({'mensaje_exito': False, 'error': True})

            # preparo los datos para mostrar al usuario
            cuotas =  int((prestamo*1.065) / (plazo*12)) # 6.5% de interes al prestamo
            
            informe = {
                'cliente': nombre,
                'importe': prestamo,
                'plazo': plazo*12,
                'cuotas': cuotas
            }

            # envio un correo al cliente con los datos del cliente
            asunto = 'Consulta de credito'
            mensaje = f"Estimado {nombre},\n    Tu solicitud para el crédito hipotecario ha sido recibida con éxito.\n\nDetalles de la solicitud:\n  Plazo del prestamo: {plazo*12} meses\n    Prestamo solicitado: ${prestamo}\n    Cuotas mensuales: ${cuotas}\n\n    Nos pondremos en contacto contigo a la brevedad para continuar con el proceso.\n\nSaludos cordiales,\n    El equipo de crédito Hipotecario"
            destinatario = 'maximiliano.caprioglio@lalupitacontenidos.site'

            try:
                send_mail(
                    asunto,
                    mensaje,
                    destinatario,
                    [email],
                    fail_silently=False)
                return JsonResponse({'mensaje_exito': True, 'informe': informe})
            except Exception as e:
                return JsonResponse({'mensaje_exito': True, 'informe': informe, 'error': 'No se pudo enviar el correo, Pero te dejamos la cotizacion visible en la web, inténtalo más tarde o revisa que tu mail este bien.'})
        else:
            return JsonResponse({'mensaje_exito': False, 'errors': form.errors})
    else:
        form = FormularioCredito()
        return render(request, 'creditos/index.html', {'form': form})

def obtener_cotizacion_dolar(request):
    try:
        response = requests.get("https://dolarapi.com/v1/dolares/oficial")
        data = response.json()
        return JsonResponse({
            'valor': data['venta'],
            'moneda': data['moneda'],
            'fecha': data['fechaActualizacion']
        })
    except Exception as e:
        return JsonResponse({'error': 'No se pudo obtener la cotización'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel')
        else:
            return render(request, 'creditos/login.html', {'error': 'Credenciales inválidas'})
    else:
        return  render(request, 'creditos/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required        
def panel_view(request):
    consultas = Consulta.objects.all()
    return render(request, 'creditos/panel.html', {'consultas': consultas})

@login_required
def eliminar_consulta(request, consulta_id):
    try:
        consulta = Consulta.objects.get(id=consulta_id)
        consulta.delete()
        return redirect('panel')
    except Consulta.DoesNotExist:
        return render(request, 'creditos/panel.html', {'error': 'Consulta no encontrada'})