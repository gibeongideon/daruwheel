
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

@login_required(login_url="/users/login")
def index(request):
    print(request.user)
    return render(request, "core/index.html")

@login_required(login_url="users/login")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('spinchannel/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))



@login_required(login_url="/users/login")
def icons(request):

    return render(request, "core/ui-icons.html")


@login_required(login_url="/users/login")
def maps(request):
 
    return render(request, "core/ui-maps.html")

@login_required(login_url="/users/login")
def topo(request):
 
    return render(request, "core/ui-typography.html")


@login_required(login_url="/users/login")
def support(request):
 
    return render(request, "core/page-rtl-support.html")





# # ADMIN VIEW

# @login_required(login_url='/users/login/')
# def adminsettings(request):

#     stake_form = StakeForm()
#     trans_logz =Stake.objects.filter(user =request.user).order_by('-created_at')[:12]
#     if request.method == 'POST':
#         #QF
#         #is this secure# normal dic generated from imuttable dic//automatic user                
#         data = {}
#         data['user'] = request.user
#         data['marketselection'] = request.POST['marketselection']
#         data['amount'] = request.POST['amount'] 

#         stake_form = StakeForm(data=data)
#         # stake_form = StakeForm(data=request.POST)
        
#         if stake_form.is_valid():

#             stake_form.save()
#             print('STAKE DONE')
#             # return redirect(reverse('cash_trans:trans_log'))
#         else:
#             print('ERRRRR',stake_form.errors)

#     context = {'user': request.user,'stake_form':stake_form,'trans_logz':trans_logz}

#     return render(request, 'spinchannel/daru_spin.html',context)
    
