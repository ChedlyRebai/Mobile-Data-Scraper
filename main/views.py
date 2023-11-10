from itertools import zip_longest

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

listMarques=[]
ListProducts=[]
listTitles=[]
listPrice=[]
listImages=[]
listDiscount=[]
listStars=[]
listLinks=[]
listReviews=[]
listSellerRating=[]
listSellerRatingValue=[]
currentPage=0
numberPages=""

while True:
    
    url= f"https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page={currentPage}#catalog-listing"
    page=requests.get(url)
    src=page.content
    soup=BeautifulSoup(src,"lxml")
    sellerRating=soup.find_all('a',{'class':'fk-rad -me-start','data-eventaction':"seller_score"})

    #scraping number of pages
    if currentPage ==1 :
        numberPages=soup.find('div',{'class':'pg-w -ptm -pbxl'})
        numberPages= numberPages.find_all('a')[-1]
        numberPages= numberPages['href']
        numberPages = int(numberPages.split('=')[1].split('#')[0])

    #scraping marques
    marques = soup.find_all('a', {'data-eventaction': 'brand'})
    products=soup.find_all('article',{'class':'c-prd'})
    
    #scraping products
    for product in products:
        #scraping name of products
        productTitle=product.find('h3',{'class':'name'})
        listTitles.append(productTitle.text)

        #scraping price
        productPrice=product.find('div',{'class':'prc'})
        listPrice.append(productPrice.text)

        #scraping stars
        if product.find('div',{'class':'stars _s'}) != None:
           listReviews.append(int((product.find('div',{'class':'rev'}).text.strip())[-2]))
        else:
            listReviews.append(0)

        #scraping links
        listLinks.append(f"https://www.jumia.com.tn{product.find('a').attrs['href']}")

        #scraping images
        listImages.append(product.find('img',{'class':'img'}).attrs['data-src'])

        #scraping discount
        productDiscount=product.find('div',{'class':'_dsct'})
        if (productDiscount!=None):
            listDiscount.append(int(float(productDiscount.text.rstrip('%'))) )
        else:
            listDiscount.append(0)
        
        #scraping stars
        productStart=product.find('div',{'class':'stars'})
        if productStart != None:
            listStars.append(round(float((productStart.text).split()[0])))    
        else:
            listStars.append(0)
    currentPage+=1
    
    if currentPage==numberPages:
        break

#scraping rating 
for rating in sellerRating:
    listSellerRating.append( rating.text)   
    listSellerRatingValue.append( int(rating.text.split('%')[0]))

for marque in marques:
    listMarques.append(marque.text)

dfsellerRating=pd.DataFrame()
dfsellerRating['title']=listSellerRating
dfsellerRating['value']=listSellerRatingValue


sellerRatingDict=dfsellerRating.to_dict('records')


#put marques information in a dataframe
dfmarques=pd.DataFrame()
dfmarques['marque']=listMarques
marqueDict=dfmarques.to_dict('records')


#put product information in a dataframe
dfproduct= pd.DataFrame()
dfproduct['name']=listTitles
dfproduct['Discount']=listDiscount                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
dfproduct['stars'] = listStars
dfproduct['price'] = listPrice
dfproduct['image']=listImages
dfproduct['links']=listLinks
dfproduct['review']=listReviews

#turn products dataframe to dictionary
datalist=dfproduct.to_dict('records')

def index(request):
    page_obj=datalist
    return render(request, 'main/index.html', {'datalist': datalist, 'marqueList': marqueDict, 'sellerRating': sellerRatingDict})

#search function
def my_view(request):
    page_obj=datalist
    if request.method == 'POST':
        checkbox_values = request.POST.getlist('my_checkbox_name')           
        ratings=request.POST.get('rating')   
        minprice=request.POST.get('min')     
        maxprice=request.POST.get('max')       
        ratingcheck=request.POST.get('rating')
        page_obj=datalist    
        if checkbox_values:
            page_obj = [d for d in page_obj if any(val in d['name'] for val in checkbox_values)]
        if minprice:
            page_obj = [d for d in page_obj if float(d['price'].replace(",", "").split()[0]) > float(minprice)]
        if maxprice:
            page_obj = [d for d in page_obj if float(d['price'].replace(",", "").split()[0]) < float(maxprice)]
        if ratings:
            page_obj = [d for d in page_obj if int(d['Discount']) > int(ratings)]
    return render(request, 'main/index.html', {'datalist': page_obj, 'marqueList': marqueDict, 'sellerRating': sellerRatingDict})

