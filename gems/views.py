from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from django.views.generic.base import TemplateView

from .forms import UploadFileForm
from .models import Deal, Customer


class HomePageView(TemplateView):
    template_name = 'home.html'


class DataView(ListView):
    template_name = 'data_view.html'
    model = Deal

    def get_context_data(self, *, object_list=None, **kwargs):
        customers_qset = Customer.objects.all().order_by('spent_money').reverse()[:5]
        clients_data = []

        for customer in customers_qset:
            clients_data.append(f'{customer.username}'
                                f' {customer.spent_money}'
                                f' {customer.gems}')

        context = {'context': clients_data}

        return context


class UploadDataView(TemplateView, FormView):
    template_name = 'upload_file.html'
    model = Deal
    form_class = UploadFileForm

    def post(self, request):

        if request.FILES['file'].name != 'deals.csv':
            response = 'Status: Error, Desc: Wrong file name. Should be: "deals.csv" Try again.'
            print(response)
            return HttpResponse('<h1>Wrong file name.</h1>', status=406)

        Customer.objects.all().delete()

        deals = tuple(tuple(str(deal, encoding='utf-8').split(',')) for deal in request.FILES['file'])[1:]

        for deal in deals:
            try:
                Customer.objects.get(username__exact=deal[0])
            except Customer.DoesNotExist:
                Customer.objects.create(username=deal[0], spent_money=0, gems='')
            name = deal[1].replace(' ', '_')
            time = deal[4].rstrip("\r\n")

            try:
                Deal.objects.create(username=Customer.objects.get(username__exact=deal[0]),
                                    gem_name=name,
                                    spent_money=int(deal[2]),
                                    gems=int(deal[3]),
                                    date=time
                                    )
            except ValueError:
                response = 'Status: Error, Desc: Wrong data format.' \
                           ' Should be: 1st column: str,' \
                           ' 2nd column: str,' \
                           ' 3rd column: int,' \
                           ' 4th column: int,' \
                           ' 5th column: str. Try again.'
                print(response)
                return HttpResponse('<h1>Wrong data format.</h1>', status=406)
            except ValidationError:
                response = 'Status: Error, Desc: Wrong data format.' \
                           ' Should be: 1st column: str,' \
                           ' 2nd column: str,' \
                           ' 3rd column: int,' \
                           ' 4th column: int,' \
                           ' 5th column: str. Try again.'
                print(response)
                return HttpResponse('<h1>Wrong data format.</h1>', status=406)

        for customer in Customer.objects.all():
            customers_deals = Deal.objects.filter(username=customer)
            spent_money = customers_deals.aggregate(Sum('spent_money'))['spent_money__sum']
            gems = str(set(deal.gem_name for deal in customers_deals)) \
                .rstrip('}').lstrip('{').replace(',', '').replace("'", '')
            Customer.objects.filter(username=customer.username).update(spent_money=spent_money)
            Customer.objects.filter(username=customer.username).update(gems=gems)

        customers = Customer.objects.all().order_by('spent_money').reverse()[:5]

        gems = str([customer.gems + " " for customer in customers]) \
            .lstrip('[').rstrip(']').replace(',', '').replace("'", '')

        gems_amounts = dict((gem, gems.count(gem)) for gem in gems.split())

        for customer in customers:
            gems = str([gem for gem in customer.gems.split() if gems_amounts[gem] >= 2]) \
                .lstrip('[').rstrip(']').replace("'", '').replace(',', '')
            Customer.objects.filter(username=customer.username).update(gems=gems)

        print('Status: OK')
        return HttpResponse('<h1>Upload Successful!</h1>')
