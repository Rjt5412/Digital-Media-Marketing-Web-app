from django.shortcuts import render, get_object_or_404, redirect
from . import services,convert
from . import ml


# Create your views here.

def index(request):
    twitter_trends = services.get_twitter_trends()
    gplus_trends,tumblr_trends = services.get_tumblr_and_gplus_trends()
    return render(request, 'dmm/index.html',{'twitter_trends': twitter_trends, 'gplus_trends': gplus_trends, 'tumblr_trends': tumblr_trends})

def search(request):
    return render(request, 'dmm/search.html')

def get_params(request):
    '''
    form = forms.Search_form(request.POST)
    print(form.errors)
    if form.is_valid():
        print("is valid")
        keyword = form.cleaned_data["search"]
        twitter = form.cleaned_data["twitter"]
        gplus = form.cleaned_data["gplus"]
        tumblr = form.cleaned_data["tumblr"]
        category = form.cleaned_data["category"]
        sub_category = form.cleaned_data["sub_category"]
        print(keyword)
        return render(request, 'dmm/search.html')
    print("is not valid")
    return render(request, 'dmm/search.html')
'''
    if request.method == "POST":
        keyword = request.POST.get('search')
        twitter = request.POST.get('twitter')
        gplus = request.POST.get('gplus')
        tumblr = request.POST.get('tumblr')
        main_category = request.POST.get('Main_Category')
        sub_category = request.POST.get('Sub_Category')


        if gplus!= None:
            gplus_data = services.g_plus_data(keyword)
            gplus_max = max(gplus_data['Likes'])
            gplus_min = min(gplus_data['Likes'])
            for i in range(0, (len(gplus_data['Likes']) - 1)):
                gplus_data['coefficient'][i] = convert.normalize(gplus_data['Likes'][i], (int(sub_category) - 9),
                                                                 int(sub_category), gplus_min, gplus_max)
        else:
            gplus_max = 0
            gplus_min = 0

        if twitter!= None:
            twitter_data = services.get_twitter_data(keyword)
            twitter_max = max(twitter_data['Likes'])
            twitter_min = min(twitter_data['Likes'])
            for i in range(0, (len(twitter_data['Likes']) - 1)):
                twitter_data['coefficient'][i] = convert.normalize(twitter_data['Likes'][i], (int(sub_category) - 9),
                                                                   int(sub_category), twitter_min, twitter_max)
        else:
            twitter_max = 0
            twitter_min = 0


        if tumblr!= None:
            tumblr_data = services.get_tumblr_data(keyword)
            tumblr_max = tumblr_data['Likes']
            tumblr_min = tumblr_data['Likes']
            for i in range(0, (len(tumblr_data['Likes']) - 1)):
                tumblr_data['coefficient'][i] = convert.normalize(tumblr_data['Likes'][i], (int(sub_category) - 9),
                                                                  int(sub_category), tumblr_min, tumblr_max)
        else:
            tumblr_max = 0
            tumblr_min = 0



        ml_out = ml.ml_func(main_category,sub_category)


        print(ml_out)

        return render(request, 'dmm/search.html')
    else:
        return render(request, 'dmm/search.html')
