from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin(BaseListView):
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get_queryset(self):
        data = Filmwork.objects.annotate(
            genres=ArrayAgg('genre__name', distinct=True),

            actors=ArrayAgg('person__full_name',
                            filter=Q(personfilmwork__role='actor'), distinct=True),

            directors=ArrayAgg('person__full_name',
                               filter=Q(personfilmwork__role='director'), distinct=True),

            writers=ArrayAgg('person__full_name',
                             filter=Q(personfilmwork__role='writer'), distinct=True)
            )

        queryset = data.values(
            'id', 'title', 'description', 'creation_date', 'rating',
            'type', 'genres', 'actors', 'directors', 'writers'
        )

        return queryset


    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)



class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        previous = page.previous_page_number() if page.has_previous() else None
        nextt = page.next_page_number() if page.has_next() else None

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': previous,
            'next': nextt,
            'results': list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        context = kwargs['object']
        return context

