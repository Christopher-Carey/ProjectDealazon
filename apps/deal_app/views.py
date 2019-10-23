from django.shortcuts import render, HttpResponse,redirect
from apps.login_app.models import User
from .models import *
import requests
from bs4 import BeautifulSoup
import base64
from selenium import webdriver
import time


def index(request):
    user=User.objects.get(email=request.session['email'])

    if not 'deal' in request.session:
        request.session["deal"] = 0
    if not 'sort' in request.session:
        request.session["sort"] = 0


    if request.session["deal"] == 0:
        url='https://www.amazon.com/gp/goldbox/?pf_rd_p=dfe13b09-3b88-422f-bc64-07ef802d4688&pf_rd_r=FGXM91S8527CSY369PG9'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        find_img = soup.find_all("div",class_="a-row layer")
        find_img = find_img[0:6]

        all_deals=Deal.objects.all()
        for i,deal in zip(find_img,all_deals):
            deal.title=i.contents[1].attrs['alt']
            deal.img=i.contents[1].attrs['src']
            deal.save()
        request.session["deal"]=1

    context={
        'all_products':user.who_posted.all(),
        'sorted_price':user.who_posted.all().order_by('price'),
        'all_deals':Deal.objects.all()
    }
    
    return render(request,"deal_app/index.html",context)

def sort_price(request):
    request.session['sort']=1
    return redirect("/deals")

def add_deal(request):
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    user=User.objects.get(email=request.session['email'])
    url=request.POST['url']
    # BS SETUP
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'lxml')

    title = soup.find(id="productTitle").get_text()
    # GET PRICE
    str_price = soup.find(id="priceblock_ourprice")
    if str_price == None:
        str_price = soup.find(id="priceblock_saleprice").get_text()
    else:
        str_price = soup.find(id="priceblock_ourprice").get_text()
    price=str_price[1:8]

    # GET IMAGE
    find_img = soup.find(id="landingImage").attrs
    img=find_img['data-old-hires']

    # ADD PRODUCT TO DATABASE
    Product.objects.create(url=url,title=title,price=price,users=user,img=img,updated_price=price)
  
    return redirect("/deals")

def update_price(request):

    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    user=User.objects.get(email=request.session['email'])
    users_products=user.who_posted.all()
    for product in users_products:
        url=product.url
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,'lxml')

        str_price = soup.find(id="priceblock_ourprice")
        if str_price == None:
            str_price = soup.find(id="priceblock_saleprice").get_text()
        else:
            str_price = soup.find(id="priceblock_ourprice").get_text()
        price=str_price[1:8]
        
        product.updated_price=price
        product.save()
    print("done")
    return redirect("/deals")

def deals(request):
    url='https://www.amazon.com/gp/goldbox/?pf_rd_p=dfe13b09-3b88-422f-bc64-07ef802d4688&pf_rd_r=FGXM91S8527CSY369PG9'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    find_img = soup.find_all("div",class_="a-row layer")
    find_img = find_img[0:6]

    output_list = []
    for i in find_img:
        output_list.append([i.contents[1].attrs['alt'], i.contents[1].attrs['src']])
 
    return redirect("/deals")


def user_page(request):
    user=User.objects.get(email=request.session['email'])
    all_products=user.who_posted.all()
    uploaded_time=[]

    for product in all_products:
        dif=product.updated_at - product.created_at
        product.days_logged=dif
        product.save()

        print(dif)
    print(uploaded_time)




    context={
        'all_products':user.who_posted.all(),
        'uploaded_days':uploaded_time
    }

    return render(request,"deal_app/user_page.html",context)


