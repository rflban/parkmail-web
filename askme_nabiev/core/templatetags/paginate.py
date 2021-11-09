from django.template import Library


register = Library()


@register.inclusion_tag('core/pagination.html')
def paginate(paginator, page_obj, gap=2):
    pages_range = range(page_obj.number - gap, page_obj.number + gap + 1)
    pages_range = filter(lambda page: 0 < page and page <= paginator.num_pages, pages_range)
    pages_range = tuple(pages_range)
    pagination = {'range': pages_range, 'lskip': pages_range[0] - 1 > 1, 'rskip': paginator.num_pages - pages_range[-1] > 1}

    return {'paginator': paginator, 'page_obj': page_obj, 'pagination': pagination}
