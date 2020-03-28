from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        email_address = request.session['email_address']
        if email_address != '':
            context = {
                'email_address': email_address
            }
            return render(request, self.template_name, context=context)
        else:
            return HttpResponseRedirect("/login")
