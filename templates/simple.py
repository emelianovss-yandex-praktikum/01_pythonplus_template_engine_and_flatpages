filters = {
    'len': lambda value, _: len(value)
}


def extends(extended_func):
    def decorator(func):
        def wrapper(context):
            updated_context = func(context)
            return extended_func(updated_context)
        return wrapper
    return decorator


def include(func, context, with_ = None):
    if with_ is None:
        with_ = {}
    return func({**context, **with_})


def get(name: str, context, default: str = None) -> str:
    first, *other = name.split('.')
    if name not in context:
        return default if default is not None else ''

    value = context.get(first)
    if callable(value):
        return value()
    elif len(other) and isinstance(value, dict):
        return get('.'.join(other), context, default)
    else:
        return value


def filter_(value, name, arg: str = None):
    func = filters.get(name)
    if func:
        return func(value, arg)
    else:
        return ''


def post_item(context):
    return f'<a href="#">Post: {get("post.name", context)}</a>\n'


def base_template(context) -> str:
    return f'''
<head>
<title>{get('title', context, 'Последние обновления на сайте')}</title>
</head>
<body>
<h1>{get('header', context, 'Последние обновления на сайте')}</h1>
{get('content', context)}
</body>
'''


@extends(base_template)
def posts_lists(context):
    return {
        'header': f'Всего постов на сайте {filter_(get("posts", context), "len")}',
        'content': f'''
<p>Список постов/p>
{"".join([include(post_item, context, with_={"post": post}) for post in get("posts", context)])}
        '''
    }


if __name__ == '__main__':
    posts = [
        {'name': f'Post name {i}', 'id': i}
        for i in range(5)
    ]
    rendered = posts_lists({'posts': posts})
    print(rendered)