from django.shortcuts import render, HttpResponse,redirect
from apps.login_app.models import User
from .models import *
import requests
from bs4 import BeautifulSoup
import base64
from selenium import webdriver




def index(request):
    # user=User.objects.get(email=request.session['email'])
    # products=user.who_posted.all()
    # for product in products:
    #     url=product.url
    #     # BS SETUP
    #     headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    #     page = requests.get(url,headers=headers)
    #     soup = BeautifulSoup(page.content,'lxml')

    #     # GET PRICE
    #     str_price = soup.find(id="priceblock_ourprice")
    #     if str_price == None:
    #         str_price = soup.find(id="priceblock_saleprice").get_text()
    #     else:
    #         str_price = soup.find(id="priceblock_ourprice").get_text()
    #     updated_price=str_price[1:8]
    #     print(updated_price)

    #     product.updated_price=updated_price
    #     product.save()

    context={
        'all_products':Product.objects.all()
    }
    return render(request,"deal_app/index.html",context)
def sort(request):
    Product.objects.order_by('-created_at')
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

def deals(request):
    # headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    url='https://www.amazon.com/gp/goldbox/?pf_rd_p=dfe13b09-3b88-422f-bc64-07ef802d4688&pf_rd_r=FGXM91S8527CSY369PG9'
    # browser = webdriver.PhantomJS(executable_path = "C:\\Program Files\\phantomjs-2.1.1-windows\\bin")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    # find_img = soup.find(id="101_dealView_0")
    find_img = soup.find_all("div",class_="a-row layer").attrs
    for i in find_img:
        print(i.attrs)
        # print(find_img[i])
 

    return redirect("/deals")


# def get_info(url):
#     headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
#     # BS SETUP
#     page = requests.get(url,headers=headers)
#     soup = BeautifulSoup(page.content,'lxml')

#     title = soup.find(id="productTitle").get_text()

#     # GET PRICE
#     str_price = soup.find(id="priceblock_ourprice")
#     if str_price == None:
#         str_price = soup.find(id="priceblock_saleprice").get_text()
#     else:
#         str_price = soup.find(id="priceblock_ourprice").get_text()
#     price=str_price[1:8]

#     # GET IMAGE
#     find_img = soup.find(id="landingImage").attrs
#     img=find_img['data-old-hires']

#     product_info={
#         'url':url,
#         'title':title,
#         'price':price,
#         'img':img
#     }

#     return product_info


