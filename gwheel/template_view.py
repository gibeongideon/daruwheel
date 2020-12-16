# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .forms import StakeForm


# @login_required(login_url='/spin/log_in/')
# def place_stake(request):

#     form = StakeForm()
#     if request.method == 'POST':
#         form = StakeForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             print('YES DONE')
#             # return redirect(reverse('cash_trans:trans_log'))
#         else:
#             print('ERRRRR',form.errors)
#     return render(request, '/.html', {'form': form})