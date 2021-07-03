
URLS = {
    'about': '/abount/me'
}


def url(name, *args, **kwargs):
    if name in URLS:
        return URLS[name]
    else:
        raise ValueError('Url not found')


print(url('about'))


def get_user(user_id):
    return '/users/{user_id}'.format(user_id=user_id)


URLS['user'] = get_user


def url(name, *args, **kwargs):
    if name in URLS:
        url_ = URLS[name]
        return url_(*args, **kwargs) if callable(url_) else url_
    else:
        raise ValueError('Url not found')


print(url('user', 1))
print(url('user', user_id=1))


import re


def get_user(user_id):
    string = '/users/{user_id}'.format(user_id=user_id)
    match = re.match(r'/users/(?P<used_id>\d+)', string)
    if match:
        return match.groupdict()
    else:
        raise ValueError('Not regex match')


URLS['user'] = get_user


def url(name, *args, **kwargs):
    if name in URLS:
        url_ = URLS[name]
        return url_(*args, **kwargs) if callable(url_) else url_
    else:
        raise ValueError('Url not found')


print(url('user', 1))
print(url('user', user_id='string'))
