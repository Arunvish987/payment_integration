from django.shortcuts import render
import razorpay
from .models import Coffee
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        email = request.POST.get('email')
        client = razorpay.Client(auth=("rzp_test_I2uBUvvKv9tk7F", "X1OlNxXNnhu12eUOVaUVunAs"))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture': '1'})

        coffee = Coffee(name=name, amount=amount, email=email, payment_id=payment['id'])
        coffee.save()

        return render(request, 'src/index.html', {'payment':payment})

    return render(request, 'src/index.html')

@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ''
        data = {}
        for key, val in a.items():
            if key == 'razorpay_order_id':
                data['razorpay_order_id'] = val
                order_id = val
            elif key == 'razorpay_payment_id':
                data['razorpay_payment_id'] = val
            elif key == 'razorpay_signature':
                data['razorpay_signature'] = val
                
        user = Coffee.objects.filter(payment_id=order_id).first()

        client = razorpay.Client(auth=("rzp_test_I2uBUvvKv9tk7F", "X1OlNxXNnhu12eUOVaUVunAs"))
        check = client.utility.verify_payment_signature(data)

        if check:
            return render(request, 'error.html')
        user.is_paid = True
        user.save()

        msg_plain = render_to_string('src/email.txt')
        msg_html = render_to_string('src/email.html')

        send_mail("Your payment has been recieved.", msg_plain, settings.EMAIL_HOST_USER, [user.email
        ], html_message=msg_html)
    
    return render(request, 'src/success.html')
