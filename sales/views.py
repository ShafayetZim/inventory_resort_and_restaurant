from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View
from sales.forms import SalesCreateForm, SalesChildFormset
from sales.models import SalesParent, SalesChild
from sales.serializers import SalesItemSerializerPopUp

from ecommerce.models import Customers, Product
# from stock.models import StockPrime
from django.db import IntegrityError, transaction
# from fpdf import FPDF
# from accounts.models import GlHeader, AccountsPrime


class SalesListView(LoginRequiredMixin, ListView, ):
    model = SalesParent  # Model I want to Covert to List
    template_name = 'sales/sales.html'  # Template Name
    context_object_name = 'sales'  # Change default name of objectList
    ordering = ['-order_date', '-updated_at']  # Ordering post LIFO
    paginate_by = 20  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sales List"
        context["nav_bar"] = "sales"
        context['stocks_list'] = self.model.objects.all()
        return context


def new_sales(request):
    template_name = 'sales/new_sales.html'

    if request.method == 'GET':
        print("GET called")
        sales_form = SalesCreateForm(None)
        sales_form_child = SalesChildFormset(queryset=SalesChild.objects.none())

    elif request.method == 'POST':
        print("Post called")
        sales_form = SalesCreateForm(request.POST)
        sales_form_child = SalesChildFormset(request.POST)

        if sales_form.is_valid() and sales_form_child.is_valid():
            sales_parent = sales_form.save(commit=False)
            sales_parent.author = request.user
            sales_parent.is_active = True
            sales_parent.save()

            for form in sales_form_child:

                if form.is_valid():
                    try:
                        packing_qty = form.cleaned_data.get('packing_qty')
                        product_qty = form.cleaned_data.get('quantity')

                        if (packing_qty is not None and packing_qty > 0) and (
                                product_qty is not None and product_qty > 0):
                            total_packing = product_qty / packing_qty

                        else:
                            total_packing = 1.0

                        child = form.save(commit=False)
                        child.order_date = sales_parent.order_date
                        child.packing = total_packing
                        child.invoice_no = SalesParent.objects.get(invoice_no=sales_parent.invoice_no)
                        child.author = sales_parent.author
                        child.is_active = True
                        child.save()

                    except IntegrityError as e:
                        print(e.args)

                else:
                    print("Child Form Error")
                    print(form.errors)

            messages.add_message(request, messages.SUCCESS, 'New Sales Entry Successful')
            return redirect('sales-list')

        else:
            print("Not Valid Create Form")
            print(sales_form.errors)
            print(sales_form_child.errors)

    return render(request, template_name, {
        'sales_form': sales_form,
        'formset': sales_form_child,
        'title': 'New Sales',
        'nav_bar': 'new_sales',
    })


def get_current_stock_by_warehouse(warehouse, product):
    available_qty = StockPrime.objects.filter(warehouse=warehouse, product=product).aggregate(
        total_qty=Sum(F('quantity') * F('sign')))
    available_qty = available_qty.get('total_qty')

    if available_qty is None:
        available_qty = 0.0
    return available_qty


@login_required
def new_sales_edit(request, invoice_no):
    template_name = 'sales/new_sales_edit.html'

    if request.method == 'GET':
        print("GET called")
        parent = get_object_or_404(SalesParent, invoice_no=invoice_no)
        sales_form = SalesCreateForm(instance=parent)
        queryset = SalesChild.objects.filter(invoice_no=invoice_no)

        # Set Current Stock of Item
        for query in queryset:
            query.extra_field = get_current_stock_by_warehouse(parent.warehouse, query.product)
            query.save()

        sales_form_child = SalesChildFormset(queryset=SalesChild.objects.filter(invoice_no=invoice_no))

    elif request.method == 'POST':
        print("Post called")
        parent = get_object_or_404(SalesParent, invoice_no=invoice_no)
        sales_form = SalesCreateForm(request.POST, instance=parent)
        queryset = SalesChild.objects.filter(invoice_no=invoice_no)
        sales_form_child = SalesChildFormset(request.POST, queryset=queryset)

        if sales_form.is_valid() and sales_form_child.is_valid():
            sales_parent = sales_form.save(commit=False)
            sales_parent.author = request.user
            sales_parent.is_active = True
            sales_parent.save()

            for form in sales_form_child:

                if form.is_valid():
                    try:
                        packing_qty = form.cleaned_data.get('packing_qty')
                        product_qty = form.cleaned_data.get('quantity')

                        if (packing_qty is not None and packing_qty > 0) and (
                                product_qty is not None and product_qty > 0):
                            total_packing = product_qty / packing_qty

                        else:
                            total_packing = 1.0

                        child = form.save(commit=False)
                        child.order_date = sales_parent.order_date
                        child.invoice_no = SalesParent.objects.get(invoice_no=sales_parent.invoice_no)
                        child.packing = total_packing
                        child.author = sales_parent.author
                        child.is_active = True
                        child.save()
                    except IntegrityError as e:
                        print(e.args)
                        messages.add_message(request, messages.WARNING, 'Sales Product must be Unique!')
                        return redirect(request.path)

                else:
                    print("Child Form Error")
                    messages.add_message(request, messages.ERROR, form.errors)
                    print(form.errors)

            messages.add_message(request, messages.SUCCESS, 'Sales Update Successful')
            return redirect('sales-list')

        else:
            print("Not Valid Create Form")
            print(sales_form_child.errors)

    return render(request, template_name, {
        'sales_form': sales_form,
        'formset': sales_form_child,
        'title': 'New Sales',
        'nav_bar': 'new_sales',
    })


@login_required
def sales_post(request, invoice_no):
    print("invoice_no: " + invoice_no)
    sales_request_parent = SalesParent.objects.get(invoice_no=invoice_no)
    sales_request_child = SalesChild.objects.filter(invoice_no=sales_request_parent.invoice_no)

    for child in sales_request_child:
        available_stock_qty = get_current_stock_by_warehouse(sales_request_parent.warehouse, child.product)

        if available_stock_qty < child.quantity:
            messages.add_message(request, messages.WARNING, 'Not Enough Stock for '
                                 + child.product.product_name + ' in ' + sales_request_parent.warehouse.warehouse_name + ' Warehouse.'
                                 + ' Available Stock Qty ' + str(available_stock_qty))
            return redirect('sales-list')

    for child in sales_request_child:
        stock_obj = StockPrime()
        stock_obj.ref_number = child.invoice_no
        stock_obj.stock_in_date = datetime.today().strftime('%Y-%m-%d')
        stock_obj.product = child.product
        stock_obj.warehouse = sales_request_parent.warehouse
        stock_obj.quantity = child.quantity
        stock_obj.total_amount_tk = 0.0
        stock_obj.type = "Issue"
        stock_obj.stock_transaction_type = "SALE"
        stock_obj.sign = -1
        stock_obj.author = request.user
        stock_obj.is_active = True
        stock_obj.save()

    # System Generate Voucher Entry Receivable
    accounts_prime_obj = AccountsPrime()
    accounts_prime_obj.ref_number = invoice_no
    accounts_prime_obj.account_name = "Sales Income"
    accounts_prime_obj.sub_account = sales_request_parent.customer.customer_code
    accounts_prime_obj.transaction_type = "Receivable"
    accounts_prime_obj.prefix = "SAL"
    accounts_prime_obj.remarks = "System Generated Voucher Of Sales"
    accounts_prime_obj.amount = sales_request_parent.total_amount * -1  # Receivable Amount is Negative
    accounts_prime_obj.year = datetime.today().strftime('%Y')
    accounts_prime_obj.period = datetime.today().strftime('%m')
    accounts_prime_obj.status = "Post"
    accounts_prime_obj.created_date = datetime.today().strftime('%Y-%m-%d')
    accounts_prime_obj.author = request.user
    accounts_prime_obj.is_active = True

    # System Generate Voucher Entry Receipt
    if sales_request_parent.paid_amount > 0:
        accounts_prime_obj.save()
        accounts_prime_obj2 = AccountsPrime()
        accounts_prime_obj2.ref_number = invoice_no
        accounts_prime_obj2.account_name = "Sales Income"
        accounts_prime_obj2.sub_account = sales_request_parent.customer.customer_code
        accounts_prime_obj2.payment_method = "Cash"
        accounts_prime_obj2.transaction_type = "Receipt"
        accounts_prime_obj2.prefix = "SAL"
        accounts_prime_obj2.remarks = "System Generated Voucher Of Sales"
        accounts_prime_obj2.amount = sales_request_parent.paid_amount
        accounts_prime_obj2.year = datetime.today().strftime('%Y')
        accounts_prime_obj2.period = datetime.today().strftime('%m')
        accounts_prime_obj2.status = "Post"
        accounts_prime_obj2.created_date = datetime.today().strftime('%Y-%m-%d')
        accounts_prime_obj2.author = request.user
        accounts_prime_obj2.is_active = True
        accounts_prime_obj.save()
        accounts_prime_obj2.save()

    else:
        accounts_prime_obj.save()

    # System Generate Voucher Entry Child
    sales_request_parent.status = "Post"
    sales_request_parent.save()

    messages.add_message(request, messages.SUCCESS, 'Sales Posted Successfully !')

    return redirect('sales-list')


@login_required
def sales_delete(request, invoice_no):
    if request.method == 'GET':
        instance = SalesParent.objects.get(invoice_no=invoice_no)
        SalesChild.objects.filter(invoice_no=instance.invoice_no).delete()
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Delete Success')
        return redirect('sales-list')


@login_required
def print_challan(request, invoice_no):
    print(invoice_no)
    sales_parent = SalesParent.objects.get(invoice_no=invoice_no)
    sales_child = SalesChild.objects.filter(invoice_no=invoice_no)
    total_qty = sales_child.aggregate(Sum('quantity'))
    total_qty = total_qty.get('quantity__sum')
    print(total_qty)

    # print('%d in words is: %s' % (total_amount, getWords(total_amount)))

    context = {
        'title': "Daily Attendants Sheet",
        'nav_bar': "report_nav",
        'sales_item': sales_child,
        'total_qty': total_qty,
        'challan_info': sales_parent,
        'bill_info': GlHeader.objects.filter(ref_number=sales_parent.invoice_no).last,
    }
    pdf = render('sales/challan_print.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, template_name, context)


@login_required
def print_bill(request, invoice_no):
    print(invoice_no)
    sales_parent = SalesParent.objects.get(invoice_no=invoice_no)
    sales_child = SalesChild.objects.filter(invoice_no=invoice_no)
    total_amount = sales_child.aggregate(Sum('amount'))
    total_amount = total_amount.get('amount__sum')
    print(total_amount)

    # print('%d in words is: %s' % (total_amount, getWords(total_amount)))

    context = {
        'title': "Daily Attendants Sheet",
        'nav_bar': "report_nav",
        'sales_item': sales_child,
        'total_tk': total_amount,
        'challan_info': sales_parent,
        'bill_info': GlHeader.objects.filter(ref_number=sales_parent.invoice_no).last,

    }
    pdf = render('sales/bill_print.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, template_name, context)


# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf = render_to_pdf('sales/bill_print.html')

#         # rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')


@login_required
def customer_info(request):
    print("customer_info called")
    customer_code = request.GET.get('customer_code', None)
    customer = Customers.objects.get(customer_code=customer_code)
    data = {
        'address': customer.customer_address,
        'phone': customer.phone,
    }
    # print(data)
    return JsonResponse(data, status=200)


def product_info(request):
    print("product_info called")
    product_id = request.GET.get('product_id', None)
    product = Product.objects.get(product_id=product_id)
    data = {
        'price': product.price,

    }
    # print(data)
    return JsonResponse(data, status=200)


@login_required
def stock_by_warehouse(request):
    print("warehouse stock  called")
    warehouse_id = request.GET.get('warehouse_id', None)
    item = request.GET.get('item', None)

    available_qty = Product.objects.get(id=item)

    data = {
        'stock': available_qty,
        'price': available_qty.price,

    }
    print(data)
    return JsonResponse(data, status=200)


def sales_item_popup(request):
    invoice_no = request.GET['invoice_no']
    dataset = SalesChild.objects.filter(invoice_no=invoice_no)
    list_1 = list()
    for item in dataset:
        ser = SalesItemSerializerPopUp(item)
        list_1.append(ser.data)
    return JsonResponse(list_1, safe=False)


def test(request, invoice_no):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(40, 10, "We are working on your challan print.... please allow us some time")
    pdf.output("tuto1.pdf")

    with open('tuto1.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed


