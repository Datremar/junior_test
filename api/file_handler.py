def handle_uploaded_file(file):
    with open('api/data/deals.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
