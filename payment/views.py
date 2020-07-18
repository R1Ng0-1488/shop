from django.shortcuts import render, redirect, get_object_or_404
import braintree

from order.models import Order
from order.tasks import order_created
# Create your views here.

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # get token for creating the transaction
        nonce = request.POST.get('payment_method_nonce', None)
        # create and save the transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # start asinc task
            order_created.delay(order_id)
            # отмечает заказ как оплаченного
            order.paid = True
            # Сохраниение id транзакции в заказ
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # формирование одноразового токена для  JS SDK
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
