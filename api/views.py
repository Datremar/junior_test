from _csv import reader

from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .file_handler import handle_uploaded_file
from .forms import UploadFileForm
from .models import Deal


# support class for DealsView
class Customer:
    def __init__(self, username: str, spent_money: int, gem_names: str):
        self.username = username
        self.spent_money = spent_money
        self.gem_names = [gem_names]

    def get_username(self):
        return self.username

    def add_spent_money(self, spent_money: int):
        self.spent_money += spent_money

    def add_gem_name(self, gem_name: str):
        if not any(gem_n == gem_name for gem_n in self.gem_names):
            self.gem_names.append(gem_name)

    def remove_gem_name(self, gem_name: str):
        self.gem_names.remove(gem_name)


# Create your views here.

class DealsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Hello.html'

    def get(self, request):
        customers = []

        for obj in Deal.objects.all():
            username = Deal._meta.get_field('username').value_from_object(obj)
            spent_money = int(Deal._meta.get_field('spent_money').value_from_object(obj))
            gem_name = Deal._meta.get_field('gem_name').value_from_object(obj)

            if not any(customer.get_username() == username for customer in customers):
                customers.append(Customer(username=username, spent_money=spent_money, gem_names=gem_name))

            for customer in customers:
                if customer.get_username() == username:
                    customer.add_spent_money(spent_money)
                    customer.add_gem_name(gem_name)

            customers = list(reversed(sorted(customers, key=lambda customer: customer.spent_money)))[:5]

        gem_dict = {}
        gems_to_delete = []

        for customer in customers:
            for name in customer.gem_names:
                if name not in gem_dict:
                    gem_dict[name] = 1
                else:
                    gem_dict[name] += 1

        for gem_key in gem_dict:
            if gem_dict[gem_key] < 2:
                gems_to_delete.append(gem_key)

        for gem_key in gems_to_delete:
            gem_dict.pop(gem_key)

        for customer in customers:
            gems = [gem for gem in customer.gem_names]
            for gem in gems:
                if gem not in gem_dict:
                    customer.remove_gem_name(gem)

        return Response({'customers': customers})


class UploadDealsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'submit_data.html'

    def get(self, request, *args, **kwargs):
        return Response({'form': UploadFileForm()})

    def post(self, request, *args, **kwargs):
        Deal.objects.all().delete()
        response = ''
        file = request.FILES['file']

        if file.name != 'deals.csv':
            response = 'Status: Error, Desc: Wrong file name. Should be: "deals.csv" Try again.'
            print(response)
            return Response({'response': response}, status=406)

        handle_uploaded_file(file)

        flag = True
        with open('api/data/deals.csv', encoding='utf-8') as data:
            deals = reader(data, delimiter=',')

            for deal in deals:
                if flag:
                    flag = not flag
                    continue

                try:
                    Deal.objects.create(username=deal[0],
                                        gem_name=deal[1],
                                        spent_money=int(deal[2]),
                                        gems=int(deal[3]),
                                        date=deal[4])
                except ValueError:
                    response = 'Status: Error, Desc: Wrong data format.' \
                               ' Should be: 1st column: str,' \
                               ' 2nd column: str,' \
                               ' 3rd column: int,' \
                               ' 4th column: int,' \
                               ' 5th column: datetime. Try again.'
                    print(response)
                    return Response({'response': response}, status=406)
                except ValidationError:
                    response = 'Status: Error, Desc: Wrong data format.' \
                               ' Should be: 1st column: str,' \
                               ' 2nd column: str,' \
                               ' 3rd column: int,' \
                               ' 4th column: int,' \
                               ' 5th column: datetime. Try again.'
                    print(response)
                    return Response({'response': response}, status=406)

        print('Status: OK')
        return Response({'response': 'File uploaded, go to /deal-view/'}, status=200)
