from django.db.models import Count

from feedback.models import FeedbackResponse

def _get_responses(school=None, time_start=None, time_end=None):
    responses = FeedbackResponse.objects.all()
    if school:
        responses = responses.filter(school=school)
    if time_start:
        responses = responses.filter(added__gte=time_start)
    if time_end:
        responses = responses.filter(added__lt=time_end)
    return responses

def _pad_data(data_dict, expected_keys, value=0):
    for k in expected_keys:
        if k not in data_dict:
            data_dict[k] = value
    return data_dict

def _get_responses_dict(value_name, **kwargs):
    data = _get_responses(**kwargs).values(value_name).annotate(count=Count('pk'))
    data = dict(map(lambda i: (i[value_name], i['count']), data))
    return data

def texture_data(**kwargs):
    expected_categories = ['crunchy', 'mushy', 'soggy',]
    data = _get_responses_dict('texture', **kwargs)
    data = _pad_data(data, expected_categories)
    return data

def colors_data(**kwargs):
    expected_categories = ['1', '2', '3', '4']
    data = _get_responses_dict('colors', **kwargs)
    data = _pad_data(data, expected_categories)
    data['4 or more'] = data.pop('4')
    return data

def finish_data(**kwargs):
    expected_categories = range(11)
    data = _get_responses_dict('finish', **kwargs)
    data = _pad_data(data, expected_categories)

    # convert keys to strings so labels on chart work
    data = dict(map(lambda i: (str(i[0]), i[1]), data.items()))
    return data

def vegetables_data(**kwargs):
    expected_categories = range(1, 5)
    data = _get_responses_dict('vegetables', **kwargs)
    data = _pad_data(data, expected_categories)

    # convert keys to strings so labels on chart work
    data = dict(map(lambda i: (str(i[0]), i[1]), data.items()))
    data['4 or more'] = data.pop('4')
    return data

def energy_data(**kwargs):
    expected_categories = ['energetic', 'sleepy',]
    data = _get_responses_dict('energy', **kwargs)
    data = _pad_data(data, expected_categories)
    return data
