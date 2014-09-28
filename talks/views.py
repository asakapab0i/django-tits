from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib import messages

from braces import views
from . import forms

from . import models

class RestrictToUserMixin(views.LoginRequiredMixin):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class TalkListDetailView(RestrictToUserMixin,generic.DetailView):
    http_method_names = ['get', 'post']
    form_class = forms.TalkForm
    model = models.TalkList

    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView,
                self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or None)})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = self.get_object()
            talk = form.save(commit=False)
            talk.talk_list = obj
            talk.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(obj)


class TalkListListView(RestrictToUserMixin, generic.ListView):
    model = models.TalkList

    def get_queryset(self):
        queryset = super(TalkListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('talks'))
        return queryset

class TalkListCreateView(RestrictToUserMixin,
        views.SetHeadlineMixin, generic.CreateView):

    form_class = forms.TalkListForm
    headline = 'Create'
    model = models.TalkList

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)

class TalkListUpdateView(RestrictToUserMixin,views.SetHeadlineMixin,
        generic.UpdateView):
    form_class = forms.TalkListForm
    headline = 'Update'
    model = models.TalkList

class TalkListRemoveTalkView(RestrictToUserMixin,
        generic.RedirectView):
    model = models.Talk

    def get_redirect_url(self, *args, **kwargs):
        return self.talklist.get_absolute_url()

    def get_object(self, pk, talklist_pk):
        try:
            talk = self.model.objects.get(
                        pk=pk,
                        talk_list_id=talklist_pk,
                        talk_list__user=self.request.user,
                    )
        except models.Talk.DoesNotExists:
            raise Http404
        else:
            return talk

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
                    kwargs.get('pk'),
                    kwargs.get('talklist_pk')
                )
        self.talklist = self.object.talk_list
        messages.success(
                    request,
                    u'{0.name} was removed from {1.name}'.format(
                        self.object, self.talklist)
                        )
        self.object.delete()
        return super(TalkListRemoveTalkView, self).get(request, *args, **kwargs)

class TalkListScheduleView(
        RestrictToUserMixin,
        views.PrefetchRelatedMixin,
        generic.DeleteView
        ):

    model = models.TalkList
    prefetch_related = ('talks',)
    template_name = 'talks/schedule.html'


class TalkDetailView(RestrictToUserMixin, generic.DetailView):
    model = models.Talk

    def get_queryset(self):
        return self.model.objects.filter(talk_list__user=self.request.user)












