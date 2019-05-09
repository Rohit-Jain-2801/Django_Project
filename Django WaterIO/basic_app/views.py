from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from basic_app.models import UserProfileInfo,GWL_inputs,Site_Name,FYear,City
from basic_app.modelforms2 import UserForm,UserProfileInfoForm,UserUpdateForm,ProfileUpdateForm,GWL,Site,Year,CityForm
from django.db import models

# from basic_app.modelforms2 import UserRegisterForm
# def register(request):
#         if request.method == "POST":
#                 form = UserRegisterForm(request.POST)
#                 if form.is_valid():
#                         form.save()
#                         username = form.cleaned_data.get('username')
#                         messages.success(request,f'Account created for {username}!')
#                         return redirect('page_one')
#         else:
#                 form = UserRegisterForm()
#         return render(request,'basic_app/register.html',{'form':form})


def page_one(request):
        return render(request,'basic_app/page_one.html')

def register(request):
        registered = False
        if request.method == "POST":
                user_form = UserForm(data=request.POST)
                profile_form = UserProfileInfoForm(data=request.POST)
                if user_form.is_valid() and profile_form.is_valid():
                        user = user_form.save()
                        user.set_password(user.password)
                        user.save()
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        if 'profile_pic' in request.FILES:
                                profile.profile_pic = request.FILES['profile_pic']
                        profile.save()
                        registered = True
                else:
                        print(user_form.errors,profile_form.errors)
        else:
                user_form = UserForm()
                profile_form = UserProfileInfoForm()
        return render(request,'basic_app/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
        if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username,password=password)
                if user:
                        if user.is_active:
                                login(request,user)
                                print("Username: {} and Password: {}".format(username,password))
                                return HttpResponseRedirect(reverse('page_one'))
                        else:
                                return HttpResponse("Account NOT Active")
                else:
                        print("Username: {} and Password: {}".format(username,password))
                        messages.warning(request,'Invalid Login Details!')
        return render(request,'basic_app/login.html')

@login_required
def user_logout(request):
        logout(request)
        return HttpResponseRedirect(reverse('page_one'))

def user_details(request):
        from django.conf import settings
        if request.method == 'POST':
                u = UserUpdateForm(request.POST, instance=request.user)
                p = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
                if u.is_valid() and p.is_valid():
                        u.save()
                        p.save()
                        return HttpResponseRedirect(reverse('page_one'))
        else:
                u = UserUpdateForm(instance=request.user)
                p = ProfileUpdateForm(instance=request.user.profile)
        return render(request,'basic_app/userdetails.html',{'chk':UserProfileInfo.objects.all(), 'media_url':settings.MEDIA_URL, 'u_update':u, 'p_update':p})

def groundwaterlevel(request):
        # messages.get_messages(request).used = True
        # messages.success(request,'You have to login first to access it!')
        # messages.add_message(request, messages.SUCCESS, 'You have to login first to access it!')
        # messages.get_messages(request).used = False
        form1 = GWL()
        form2 = Site()
        form3 = Year()
        return render(request,'basic_app/groundwaterlevel.html',context={'form1':form1,'form2':form2,'form3':form3})

def unique(list1): 
    unique_list = [] 
    for x in list1: 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

def load_sites(request):
        import os
        import pandas as pd

        current_directory = os.getcwd()+'\\basic_app\\website_data_20190225.csv'
        current_directory = current_directory.replace('\\','/')
        ori = pd.read_csv(current_directory)
        block = request.GET.get('block')
        chk=[]
        for i in range(0,ori.shape[0]):
                if ori['BLOCK_NAME'][i]==block:
                        chk.append(ori['SITE_NAME'][i])
        choices3 = unique(chk)
        print(choices3)
        return render(request, 'basic_app/dropdown.html', {'sites': choices3})

def model(request):
        import numpy as np
        import pandas as pd
        import seaborn as sns
        import warnings
        warnings.filterwarnings('ignore')
        from datetime import datetime
        from statsmodels.tsa.arima_model import ARIMA
        from datetime import date
        import time
        import os
        
        current_directory = os.getcwd()+'\\basic_app\\website_data_20190225.csv'
        current_directory = current_directory.replace('\\','/')
        ori = pd.read_csv(current_directory)
        ori.drop(['STATE', 'DISTRICT', 'WLCODE', 'SITE_TYPE', 'TEH_NAME', 'LAT', 'LON'], axis=1, inplace=True)
        ori.replace(to_replace="'0", value=0, inplace=True)    

        dataset1 = pd.DataFrame().reindex_like(ori)
        dataset1.dropna(inplace=True)
        j = 0
        for i in range(0, ori.shape[0]):
                if ori['BLOCK_NAME'][i] == request.GET.get('block'):
                        dataset1.loc[j] = ori.iloc[i]
                        j += 1
        dataset1.drop(['BLOCK_NAME'], axis=1, inplace=True)
        dataset = pd.DataFrame().reindex_like(dataset1)
        dataset.dropna(inplace=True)

        j = 0
        for i in range(0, dataset1.shape[0]):
                if dataset1['SITE_NAME'][i] == request.GET.get('site'):
                        dataset.loc[j] = dataset1.iloc[i]
                        j += 1
        dataset.drop(['SITE_NAME'], axis=1, inplace=True)

        dataset['MONSOON'] = (dataset['MONSOON']).apply(np.float64)
        dataset['POMRB'] = (dataset['POMRB']).apply(np.float64)
        dataset['POMKH'] = (dataset['POMKH']).apply(np.float64)
        dataset['PREMON'] = (dataset['PREMON']).apply(np.float64)
        dataset['YEAR_OBS'] = (dataset['YEAR_OBS']).apply(np.int64)

        first = list(dataset['MONSOON'])
        second = list(dataset['POMRB'])
        third = list(dataset['POMKH'])
        fourth = list(dataset['PREMON'])
        dataset['MONSOON'] = pd.core.frame.DataFrame(x + y + z + w for x, y, z, w in zip(first, second, third, fourth))
        dataset.drop(['POMRB', 'POMKH', 'PREMON'], axis=1, inplace=True)
        dataset = dataset.iloc[::-1]

        dataset['YEAR_OBS'] = pd.to_datetime(dataset['YEAR_OBS'], yearfirst=True, format='%Y', infer_datetime_format=True)
        indexedDataset = dataset.set_index(['YEAR_OBS'])

        indexedDataset_logscale = np.log(indexedDataset)
        # for i in range(0,indexedDataset_logscale.shape[0]):
        #     if indexedDataset_logscale['MONSOON'][i]<=0:
        #         indexedDataset_logscale['MONSOON'][i]=None
        indexedDataset_logscale.dropna(inplace=True)

        dlds=indexedDataset_logscale-indexedDataset_logscale.shift()
        dlds.dropna(inplace=True)

        import itertools
        a={}
        p=d=q=range(0,6)
        pdq=list(itertools.product(p,d,q))
        for i in pdq:
            try:
                model_arima=(ARIMA(indexedDataset_logscale,order=i)).fit(disp=0)
                a[i]=model_arima.aic
            except:
                continue
        min(a, key=a.get)

        RSS=[]
        RSS1=[]
        ord=[]
        ord1=[]
        for i,j in a.items():    
            model = ARIMA(indexedDataset_logscale, order=i)
            results_ARIMA = model.fit(disp=-1)
            RSS.append(sum((results_ARIMA.fittedvalues-dlds['MONSOON'])**2))
            ord.append(i)
        for i in range(0,len(RSS)):
            if(~np.isnan(RSS[i])):
                RSS1.append(RSS[i])
                ord1.append(ord[i])
        try:
            m=min(RSS1)
        except:
            return "Algorithm Crashed!"
        for i in range(0,len(RSS1)):
            if(RSS1[i]==m):
                req=ord1[i]
                break

        model = ARIMA(indexedDataset_logscale, order=(req[0],req[1],req[2]))
        # try:
        #         model = ARIMA(indexedDataset_logscale, order=(5,1,2))
        # except:
        #         return "Algorithm Crashed!"
        results_ARIMA = model.fit(disp=-1)

        a = list(np.exp(results_ARIMA.forecast(steps=int(request.GET.get('year'))-2016)[0]))

        x2 = []
        for i in range(0, len(a)):
                t = date(int(2017+i),1,int(3+i))
                x2.append([time.mktime(t.timetuple()),a[i]])
        print(x2)

        x1 = []
        for i in range(0, indexedDataset.shape[0]):
                t = date(int(1995+i),1,int(3+i))
                x1.append([time.mktime(t.timetuple()),indexedDataset['MONSOON'][i]])
        print(x1)
        return render(request, 'basic_app/forecast.html', {'gwl1': x1, 'gwl2': 'a', 'gwl3': x2})

def weatherforecast(request):
        import requests,copy
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=7cd31de5dacf15b261c629966db01c4e'
        place,bookmark,places = [],[],[]

        if request.user.is_authenticated:
                place = City.objects.all().filter(user=request.user).values()
                print(place)
                for i in range(0,len(place)):
                        places.append(place[i]['name'])
                print(places)
                bookmark = copy.deepcopy(places)

        if request.method == 'POST':
                city = request.POST.get('name')
                if city not in places:
                        places.insert(0,city)

        form = CityForm()
        w=[]
        for c in places:
                r = requests.get(url.format(c)).json()
                try:
                        details = {
                                'city': c,
                                'main': r['weather'][0]['main'],
                                'icon': r['weather'][0]['icon'],
                                'temp': r['main']['temp'],
                                'pressure': r['main']['pressure'],
                                'humidity': r['main']['humidity'],
                                'wind_speed': r['wind']['speed']
                        }
                        print(details)
                        w.append(details)
                except:
                        print('Error while loading data!')
                        messages.success(request,'Please Enter a Valid CITY Name!')
                        # request.method = 'GET'
                        # return weatherforecast(request)
                        return render(request, 'basic_app/weather.html',{'form':form})
        return render(request, 'basic_app/weather.html',{'w':w, 'form':form, 'b':bookmark})

def addbookmark(request,c):
        article = City.objects.create(name=c,user=request.user)
        article.save()
        return HttpResponseRedirect(reverse('app:weatherforecast'))

def deletebookmark(request,c):
        City.objects.filter(name=c,user=request.user).delete()
        return HttpResponseRedirect(reverse('app:weatherforecast'))
