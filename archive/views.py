from django.shortcuts import render, get_object_or_404, redirect
from .models import BusinessLine, tableBusiness, pointGroup, ArchivedItem,Country,tx_ID
from django.db.models import Count
from .forms import *
from kompanies.views import *
from django.contrib import messages
import requests
import base58
from django.core.mail import send_mail
import secrets
import string


def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

def get_transaction(txid):
    url = "https://api.trongrid.io/wallet/gettransactionbyid"
    payload = {"value": txid}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json() if response.status_code == 200 else None

def parse_transaction_data(data):
    usdt_trc20_address = "41a614f803b6fd780986a42c78ec9c7f77e6ded13c"
    if 'raw_data' in data:
        for contract in data['raw_data'].get('contract', []):
            if contract['parameter']['type_url'] == "type.googleapis.com/protocol.TriggerSmartContract":
                contract_address = contract['parameter']['value']['contract_address']
                transfer_data = contract['parameter']['value']['data']
                function_selector = transfer_data[:8]
                if function_selector == 'a9059cbb':
                    to_address_hex = transfer_data[32:72]
                    to_address = base58.b58encode_check(bytes.fromhex('41' + to_address_hex)).decode('utf-8')
                    amount_hex = transfer_data[72:136]
                    amount_dec = int(amount_hex, 16)
                    amount_real = amount_dec / 10**6
                    token_type = "USDT" if contract_address.lower() == usdt_trc20_address.lower() else "Unknown Token"
                    return {
                        'to_address': to_address,
                        'amount': amount_real,
                        'token_type': token_type,
                        'network': 'TRC-20'
                    }
    return None

def is_transaction_to_address_and_amount(txid, target_address, required_amount):
    data = get_transaction(txid)
    if not data:
        print("Transaction data could not be retrieved or is invalid.")
        return False
    
    parsed_data = parse_transaction_data(data)
    if parsed_data and parsed_data['to_address'] == target_address and parsed_data['amount'] >= required_amount:

        print(f"Transaction confirmed to {target_address} with sufficient amount: Yes")
        if parsed_data:
            print(f"Attempted transaction to {parsed_data['to_address']} for {parsed_data['amount']} {parsed_data['token_type']} on {parsed_data['network']}")
        return True
    else:
        print(f"Transaction confirmed to {target_address} with sufficient amount: No")
        if parsed_data:
            print(f"Attempted transaction to {parsed_data['to_address']} for {parsed_data['amount']} {parsed_data['token_type']} on {parsed_data['network']}")
        return False

def dashboard(request, name):

    businessline = get_object_or_404(BusinessLine, name=name)
    table_businesses = tableBusiness.objects.filter(businessLine=businessline)
    countries = Country.objects.all()

    for tb in table_businesses:
        current_count = tb.blocks.count()
        
        if current_count < 180:
            additional_needed = 180 - current_count
            for _ in range(additional_needed):
                new_point_group = pointGroup(table_business=tb)

                # ArchivedItem nesneleri oluşturuluyor ama henüz kaydedilmiyor
                archived_items = {
                    'one': ArchivedItem(name="New Item for One", pointGroup=new_point_group),
                    'two': ArchivedItem(name="New Item for Two", pointGroup=new_point_group),
                    'three': ArchivedItem(name="New Item for Three", pointGroup=new_point_group),
                    'four': ArchivedItem(name="New Item for Four", pointGroup=new_point_group),
                    'five': ArchivedItem(name="New Item for Five", pointGroup=new_point_group),
                    'six': ArchivedItem(name="New Item for Six", pointGroup=new_point_group),
                    'seven': ArchivedItem(name="New Item for Seven", pointGroup=new_point_group),
                    'eight': ArchivedItem(name="New Item for Eight", pointGroup=new_point_group),
                    'nine': ArchivedItem(name="New Item for Nine", pointGroup=new_point_group),
                }

                # İlk olarak pointGroup kaydediliyor
                new_point_group.save()

                # ArchivedItem nesneleri kaydediliyor
                for item in archived_items.values():
                    item.save()

                # İlişkiler pointGroup'a atanıyor
                for attr, item in archived_items.items():
                    setattr(new_point_group, attr, item)

                # İlişkilerin kaydedilmesi için pointGroup tekrar kaydediliyor
                new_point_group.save()

    blocks = pointGroup.objects.filter(table_business__in=table_businesses)
    total_blocks_count = blocks.count()

    return render(request, 'dashboard.html', {
        'businessline': businessline,
        'blocks': list(blocks),
        'total_blocks': total_blocks_count,
        'countries':countries,
    })

def create(request, name):
    businessline = get_object_or_404(BusinessLine, name=name)
    table_businesses = tableBusiness.objects.filter(businessLine=businessline)
    countries = Country.objects.all()

    for tb in table_businesses:
        current_count = tb.blocks.count()
        
        if current_count < 180:
            additional_needed = 180 - current_count
            for _ in range(additional_needed):
                new_point_group = pointGroup(table_business=tb)

                # ArchivedItem nesneleri oluşturuluyor ama henüz kaydedilmiyor
                archived_items = {
                    'one': ArchivedItem(name="New Item for One", pointGroup=new_point_group),
                    'two': ArchivedItem(name="New Item for Two", pointGroup=new_point_group),
                    'three': ArchivedItem(name="New Item for Three", pointGroup=new_point_group),
                    'four': ArchivedItem(name="New Item for Four", pointGroup=new_point_group),
                    'five': ArchivedItem(name="New Item for Five", pointGroup=new_point_group),
                    'six': ArchivedItem(name="New Item for Six", pointGroup=new_point_group),
                    'seven': ArchivedItem(name="New Item for Seven", pointGroup=new_point_group),
                    'eight': ArchivedItem(name="New Item for Eight", pointGroup=new_point_group),
                    'nine': ArchivedItem(name="New Item for Nine", pointGroup=new_point_group),
                }

                # İlk olarak pointGroup kaydediliyor
                new_point_group.save()

                # ArchivedItem nesneleri kaydediliyor
                for item in archived_items.values():
                    item.save()

                # İlişkiler pointGroup'a atanıyor
                for attr, item in archived_items.items():
                    setattr(new_point_group, attr, item)

                # İlişkilerin kaydedilmesi için pointGroup tekrar kaydediliyor
                new_point_group.save()

    blocks = pointGroup.objects.filter(table_business__in=table_businesses)
    total_blocks_count = blocks.count()

    return render(request, 'create.html', {
        'businessline': businessline,
        'blocks': list(blocks),
        'total_blocks': total_blocks_count,
        'countries':countries,
    })

def create_2(request, name, id):
    
    businessline = get_object_or_404(BusinessLine, name=name)
    pointGroup_real = get_object_or_404(pointGroup, id=id)
    countries = Country.objects.all()
    table = tableBusiness.objects.get(businessLine=businessline)
    if request.method == 'POST':
        form = Form1(request.POST, request.FILES)
        
        if form.is_valid():
            max_file_size = 2 * 1024 * 1024  # 2MB limit
            for field, value in form.cleaned_data.items():
                print(f"{field}: {value}")

            pointGroup_changing = pointGroup_real
            pointGroup_changing.table_business = table
            selected_countries = form.cleaned_data.get('country', []) 
            image_files = [form.cleaned_data.get(f'image{i}') for i in range(1, 10) if form.cleaned_data.get(f'image{i}')]
            
            if not image_files:
                messages.error(request, "At least one image must be uploaded.")
                return redirect('create_2', name=name, id=id)
            else:
                if any(img.size > max_file_size for img in image_files if img):
                    messages.error(request, "All images must be less than 2MB.")
                    return redirect('create_2', name=name, id=id)
                
                else:
                    image_count = len(image_files)
                    price = image_count * 10
                    txid = form.cleaned_data['txID']
                    target_address = "TYKDPwCAGxt6Xob4WdpUNTuKrBAAHbZU5w" 

                    print(image_count)
                    print(price)
                    print(txid)

                    if tx_ID.objects.filter(name=txid).exists():
                        messages.error(request, "This transaction ID has already been used.")
                        return redirect('create_2', name=name, id=id)
                    
                    if not is_transaction_to_address_and_amount(txid, target_address, price):
                        print()
                        messages.error(request, "transaction amount is insufficient or to the wrong txID.")
                        return redirect('create_2', name=name, id=id)

            random_password = generate_random_password()

            if form.cleaned_data['image1']:
                if pointGroup_changing.one:
                    if pointGroup_changing.one.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.one.country.add(country) 

                        pointGroup_changing.one.image = form.cleaned_data['image1'] 
                        pointGroup_changing.one.name = form.cleaned_data['name']
                        pointGroup_changing.one.url = form.cleaned_data['url']
                        pointGroup_changing.one.txID = form.cleaned_data['txID']
                        pointGroup_changing.one.save()
                        pointGroup_changing.one.password = random_password
                        pointGroup_changing.one.save()


            if form.cleaned_data['image2']:
                if pointGroup_changing.two:
                    if pointGroup_changing.two.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.two.country.add(country) 

                        pointGroup_changing.two.image = form.cleaned_data['image2'] 
                        pointGroup_changing.two.name = form.cleaned_data['name']
                        pointGroup_changing.two.url = form.cleaned_data['url']
                        
                        pointGroup_changing.two.txID = form.cleaned_data['txID']
                        pointGroup_changing.two.save()
                        pointGroup_changing.two.password = random_password                   
                        pointGroup_changing.two.save()
 
            if form.cleaned_data['image3']:
                if pointGroup_changing.three:
                    if pointGroup_changing.three.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.three.country.add(country) 

                        pointGroup_changing.three.image = form.cleaned_data['image3'] 
                        pointGroup_changing.three.name = form.cleaned_data['name']
                        pointGroup_changing.three.url = form.cleaned_data['url']
                 
                        pointGroup_changing.three.txID = form.cleaned_data['txID']
                        pointGroup_changing.three.save()
                        pointGroup_changing.three.password = random_password  
                        pointGroup_changing.three.save()

            if form.cleaned_data['image4']:
                if pointGroup_changing.four:
                    if pointGroup_changing.four.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.four.country.add(country) 

                        pointGroup_changing.four.image = form.cleaned_data['image4'] 
                        pointGroup_changing.four.name = form.cleaned_data['name']
                        pointGroup_changing.four.url = form.cleaned_data['url']
                
                        pointGroup_changing.four.txID = form.cleaned_data['txID']
                        pointGroup_changing.four.save()
                        pointGroup_changing.four.password = random_password  
                        pointGroup_changing.four.save()

            if form.cleaned_data['image5']:
                if pointGroup_changing.five:
                    if pointGroup_changing.five.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.five.country.add(country) 

                        pointGroup_changing.five.image = form.cleaned_data['image5'] 
                        pointGroup_changing.five.name = form.cleaned_data['name']
                        pointGroup_changing.five.url = form.cleaned_data['url']
                        pointGroup_changing.five.txID = form.cleaned_data['txID']
                        pointGroup_changing.five.save()
                        pointGroup_changing.five.password = random_password  
                        pointGroup_changing.five.save()

            if form.cleaned_data['image6']:
                if pointGroup_changing.six:
                    if pointGroup_changing.six.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.six.country.add(country) 

                        pointGroup_changing.six.image = form.cleaned_data['image6'] 
                        pointGroup_changing.six.name = form.cleaned_data['name']
                        pointGroup_changing.six.url = form.cleaned_data['url']
                        pointGroup_changing.six.txID = form.cleaned_data['txID']
                        pointGroup_changing.six.save()
                        pointGroup_changing.six.password = random_password  

                        pointGroup_changing.six.save()

            if form.cleaned_data['image7']:
                if pointGroup_changing.seven:
                    if pointGroup_changing.seven.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.seven.country.add(country) 

                        pointGroup_changing.seven.image = form.cleaned_data['image7'] 
                        pointGroup_changing.seven.name = form.cleaned_data['name']
                        pointGroup_changing.seven.url = form.cleaned_data['url']
                        pointGroup_changing.seven.txID = form.cleaned_data['txID']
                        pointGroup_changing.seven.save()

                        pointGroup_changing.seven.password = random_password  
                        pointGroup_changing.seven.save()
                        

                        

            if form.cleaned_data['image8']:
                if pointGroup_changing.eight:
                    if pointGroup_changing.eight.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.eight.country.add(country) 

                        pointGroup_changing.eight.image = form.cleaned_data['image8'] 
                        pointGroup_changing.eight.name = form.cleaned_data['name']
                        pointGroup_changing.eight.url = form.cleaned_data['url']
             
                        pointGroup_changing.eight.txID = form.cleaned_data['txID']
                        pointGroup_changing.eight.save()
                        pointGroup_changing.eight.password = random_password  
                        pointGroup_changing.eight.save()

            if form.cleaned_data['image9']:
                if pointGroup_changing.nine:
                    if pointGroup_changing.nine.image:
                        return redirect("home")
                    else:
                        
                        for country in selected_countries:
                            pointGroup_changing.nine.country.add(country) 

                        pointGroup_changing.nine.image = form.cleaned_data['image9'] 
                        pointGroup_changing.nine.name = form.cleaned_data['name']
                        pointGroup_changing.nine.url = form.cleaned_data['url']
                        pointGroup_changing.eight.save()
                        
                        pointGroup_changing.nine.txID = form.cleaned_data['txID']
                        pointGroup_changing.nine.password = random_password  
                        pointGroup_changing.nine.save()

            pointGroup_changing.save()

            new_tx_id = tx_ID(name=txid)
            new_tx_id.save()

            send_mail(
                'Welcome to komPaines!',
                f"Here some information for you.\n\nYou can delete your items anytime with this password:  {random_password}  \n\nIf you need any help or information about komPaines, you can directly message to this mail. \n\nLink here: http://192.168.1.37:8000/board/{name}/delete/{id}\n\nkomPaines team",  # f-string ile formatlama
                'kompaines@gmail.com',  # Gönderici e-posta adresi
                [form.cleaned_data['name']],  # Alıcı e-posta adresleri listesi
                fail_silently=False,
            )

            messages.success(request,"Your transaction and upload have been successful.")

            return redirect('dashboard', name=name)

        elif not form.is_valid():
            for field, errors in form.errors.items():
                print(f"{field} is invalid: {', '.join(errors)}")
            print(form.errors.as_text())
            # Corrected render call
            return redirect('create_2', name=name, id=id)
        else:
            # Corrected render call
            return redirect('create_2', name=name, id=id) 
    
    else:
        form = Form1()  # GET isteği için boş form

    return render(request, 'create_2.html', {
        'businessline': businessline,
        'block': pointGroup_real,
        'countries': countries,
        'form': form  # Formu template'e gönder
    })


def delete(request, name, id):
    
    businessline = get_object_or_404(BusinessLine, name=name)
    pointGroup_real = get_object_or_404(pointGroup, id=id)
    countries = Country.objects.all()
    table = tableBusiness.objects.get(businessLine=businessline)
    
    if request.method == 'POST':
        form = Form2(request.POST, request.FILES)


        if form.is_valid():
            block_id = form.cleaned_data['block']
            password = form.cleaned_data["password"]
            block_name = form.cleaned_data["name"]

            if ArchivedItem.objects.get(id=block_id):
                theBlock = ArchivedItem.objects.get(id=block_id)
                
                if block_name != theBlock.name:
                    messages.error(request,"E-mail is not true. Please try again.")
                    return redirect('delete', name=name, id=id)          

                if password == theBlock.password:
                    theBlock.reset_item()
                else:
                    messages.error(request,"Incorrect password. Please try again.")
                    return redirect('delete', name=name, id=id)           
            else:
                messages.error(request,"Please select valid item")
                return redirect('delete', name=name, id=id)      
         

            print(block_id)
            send_mail(
                "Goodbye!",
                f"You successfuly deleted your data, have a nice day!\n\nkomPaines team",  # f-string ile formatlama
                'kompaines@gmail.com',  # Gönderici e-posta adresi
                [form.cleaned_data['name']],  # Alıcı e-posta adresleri listesi
                fail_silently=False,
            )

            messages.success(request,"You deleted your item successfuly")

            return redirect('delete', name=name, id=id)

        elif not form.is_valid():
            for field, errors in form.errors.items():
                print(f"{field} is invalid: {', '.join(errors)}")
            print(form.errors.as_text())
            # Corrected render call
            return redirect('delete', name=name, id=id)
        else:
            for field, errors in form.errors.items():
                print(f"{field} is invalid: {', '.join(errors)}")
            print(form.errors.as_text())
            return redirect('delete', name=name, id=id) 
    
    else:
        form = Form2()  # GET isteği için boş form

    return render(request, 'delete.html', {
        'businessline': businessline,
        'block': pointGroup_real,
        'countries': countries,
        'form': form  # Formu template'e gönder
    })

