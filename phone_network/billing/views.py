from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Client, Device, Tariff, Call
from .services.billing_service import BillingService

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            client = Client.objects.get(username=username)
            if client.password == password:
                request.session['client_id'] = client.id
                request.session['is_admin'] = client.is_admin
                request.session['client_name'] = client.name
                if client.is_admin:
                    return redirect('admin_dashboard')
                else:
                    return redirect('dashboard')
            else:
                return render(request, 'billing/login.html', {'error': 'Неверный пароль'})
        except Client.DoesNotExist:
            return render(request, 'billing/login.html', {'error': 'Пользователь не найден'})
    
    return render(request, 'billing/login.html')

def dashboard(request):
    if 'client_id' not in request.session:
        return redirect('login')
    
    client = Client.objects.get(id=request.session['client_id'])
    devices = Device.objects.filter(client=client)
    recent_calls = Call.objects.filter(from_device__client=client).order_by('-start_time')[:5]
    
    context = {
        'client': client,
        'devices': devices,
        'recent_calls': recent_calls,
        'client_name': client.name,
        'total_spent': sum([float(call.cost) for call in Call.objects.filter(from_device__client=client)]),
        'total_calls': Call.objects.filter(from_device__client=client).count(),
    }
    return render(request, 'billing/dashboard.html', context)

def make_call(request):
    if 'client_id' not in request.session:
        return redirect('login')
    
    client = Client.objects.get(id=request.session['client_id'])
    devices = Device.objects.filter(client=client)
    
    if request.method == 'POST':
        from_device_id = request.POST.get('from_device')
        to_number = request.POST.get('to_number')
        duration = int(request.POST.get('duration'))
        
        result = BillingService.process_call(int(from_device_id), to_number, duration)
        
        if result['success']:
            return render(request, 'billing/make_call.html', {
                'devices': devices,
                'success': result['message'],
                'new_balance': result['new_balance'],
                'client_name': client.name,
            })
        else:
            return render(request, 'billing/make_call.html', {
                'devices': devices,
                'error': result['error'],
                'client_name': client.name,
            })
    
    return render(request, 'billing/make_call.html', {'devices': devices, 'client_name': client.name})

def topup_balance(request):
    if 'client_id' not in request.session:
        return redirect('login')
    
    client = Client.objects.get(id=request.session['client_id'])
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        client.add_balance(amount)
        return render(request, 'billing/topup.html', {
            'success': f'Баланс успешно пополнен на {amount} руб',
            'new_balance': client.balance,
            'balance': client.balance,
            'client_name': client.name,
        })
    
    return render(request, 'billing/topup.html', {'balance': client.balance, 'client_name': client.name})

def call_history(request):
    if 'client_id' not in request.session:
        return redirect('login')
    
    client = Client.objects.get(id=request.session['client_id'])
    device_ids = client.devices.values_list('id', flat=True)
    calls = Call.objects.filter(from_device_id__in=device_ids).order_by('-start_time')
    
    return render(request, 'billing/call_history.html', {
        'calls': calls,
        'client_name': client.name,
    })

def change_tariff(request):
    if 'client_id' not in request.session:
        return redirect('login')
    
    client = Client.objects.get(id=request.session['client_id'])
    tariffs = Tariff.objects.all()
    
    if request.method == 'POST':
        tariff_id = request.POST.get('tariff_id')
        new_tariff = Tariff.objects.get(id=tariff_id)
        client.tariff = new_tariff
        client.save()
        return render(request, 'billing/change_tariff.html', {
            'tariffs': tariffs,
            'current_tariff': new_tariff,
            'success': f'Тариф успешно изменен на {new_tariff.name}',
            'client_name': client.name,
        })
    
    return render(request, 'billing/change_tariff.html', {
        'tariffs': tariffs,
        'current_tariff': client.tariff,
        'client_name': client.name,
    })

def admin_dashboard(request):
    if 'client_id' not in request.session or not request.session.get('is_admin'):
        return redirect('login')
    
    admin_user = Client.objects.get(id=request.session['client_id'])
    clients = Client.objects.all()
    tariffs = Tariff.objects.all()
    calls = Call.objects.all().order_by('-start_time')[:50]
    devices = Device.objects.all()
    
    # Статистика
    total_balance = sum([float(c.balance) for c in clients])
    total_calls = calls.count()
    total_revenue = sum([float(c.cost) for c in calls])
    
    context = {
        'clients': clients,
        'tariffs': tariffs,
        'calls': calls,
        'devices': devices,
        'client_name': admin_user.name,
        'total_balance': total_balance,
        'total_calls': total_calls,
        'total_revenue': total_revenue,
        'total_clients': clients.count(),
        'total_devices': devices.count(),
    }
    return render(request, 'billing/admin_dashboard.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('login')

def api_process_call(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        result = BillingService.process_call(
            data['from_device_id'],
            data['to_number'],
            data['duration_minutes']
        )
        return JsonResponse(result)