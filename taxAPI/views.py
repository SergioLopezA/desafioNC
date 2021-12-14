from django.views import View
from django.http import JsonResponse
import json
from .models import Payable, Transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class PayableView(View):
    def get(self, request):
        obj_list = []
        if ('service' in request.GET):
            unpaid_list = Payable.objects.filter(
             status=0, service=request.GET['service']).order_by('expire_date')
            for unpaid in unpaid_list:
                obj_list.append({
                    'expire_date': unpaid.expire_date,
                    'amount': unpaid.amount,
                    'id': unpaid.id,
                })

        else:
            unpaid_list = Payable.objects.filter(
                status=0).order_by('expire_date')
            for unpaid in unpaid_list:
                obj_list.append({
                    'service': unpaid.service,
                    'expire_date': unpaid.expire_date,
                    'amount': unpaid.amount,
                    'id': unpaid.id,
                })

        return JsonResponse(obj_list, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        service = data.get('service')
        description = data.get('description')
        amount = data.get('amount')
        expire_date = data.get('expire_date')
        status = data.get('status')

        payable_data = {
            'service': service,
            'description': description,
            'expire_date': expire_date,
            'amount': amount,
            'status': status,
            'id': id,
        }

        try:
            payable = Payable.objects.create(**payable_data)
            payable.save()

        except:
            return JsonResponse({'message': 'Error creating Payable'}, status=402)

        return JsonResponse({"message": "New Payable Created"}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TransactionView(View):
    def get(self, request):
        obj_list = []
        if ('f_date' in request.GET) and ('e_date' in request.GET):
            f_date = request.GET['f_date']
            e_date = request.GET['e_date']
            transaction_list = Transaction.objects.filter(
                paid_date__range=(f_date, e_date)).order_by('paid_date')
            date_day = ''
            amount_total = 0.0
            num_transaction = 0

            for transaction in transaction_list:
                if date_day == '':
                    date_day = transaction.paid_date

                if transaction.paid_date == date_day:
                    amount_total += transaction.amount_total
                    num_transaction += 1
                else:
                    obj_list.append({
                        'paid_date': date_day,
                        'amount_total': amount_total,
                        'num_transaction': num_transaction,
                    })

                    date_day = ''
                    amount_total = 0.0
                    num_transaction = 0

            obj_list.append({
                'paid_date': date_day,
                'amount_total': amount_total,
                'num_transaction': num_transaction,
            })

        else:
            transaction_list = Transaction.objects.all().order_by('paid_date')
            for transaction in transaction_list:
                obj_list.append({
                    'paid_date': transaction.paid_date,
                    'amount': transaction.amount,
                    'code_bar': transaction.code_bar,
                })

        return JsonResponse(obj_list, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        code_bar = data.get('code_bar')
        try:
            payable = Payable.objects.get(id=code_bar)
        except:
            return JsonResponse({'message': 'Err code Payable'}, status=402)

        amount = data.get('amount')
        payment_method = data.get('payment_method')
        card_number = data.get('card_number')
        paid_date = data.get('paid_date')

        if payable.status != 0:
            return JsonResponse({'message': 'Err cant pay this Payable'}, status=402)
        elif float(amount) != float(payable.amount):
            print(type(amount))
            print(type(payable.amount))
            return JsonResponse({'message': 'Err amount do not match'}, status=402)

        if payment_method == 'CA':
            card_number = ""
        elif card_number < 1000000000000000 or card_number > 999999999999999999:
            return JsonResponse({'message': 'wrong card number'}, status=402)

        transaction_data = {
            'amount': amount,
            'payment_method': payment_method,
            'card_number': card_number,
            'paid_date': paid_date,
            'code_bar': payable.id,
        }

        payable.status = 1

        try:
            transaction = Transaction.objects.create(
                amount=amount, payment_method="CA",
                card_number=card_number, paid_date=paid_date, code_bar=payable.id)
            transaction.save()
        except:
            return JsonResponse({'message': 'Error creating Transaction'}, status=402)

        payable.save()

        return JsonResponse({"message": "New Transaction Created"}, status=201)
