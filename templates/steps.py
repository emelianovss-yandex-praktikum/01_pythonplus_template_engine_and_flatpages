
POSTS = [{'name': f'Post name {i}', 'id': i} for i in range(5)]


def posts_list(posts):
    return f'{[post["name"] for post in posts]}'


print(posts_list(POSTS))


def posts_list(context):
    posts = (
        [post["name"] for post in context["posts"]]
        if 'posts' in context else ''
    )
    return f'{posts}'


print(posts_list({'posts': POSTS}))


def get(name: str, context) -> str:
    if name not in context:
        return ''

    value = context[name]
    return value() if callable(value) else value


def posts_list(context):
    posts = get("posts", context)
    return posts and f'{[post["name"] for post in posts]}'


print(posts_list({'posts': POSTS}))


def get(name: str, context) -> str:
    first, *others = name.split('.')
    if first not in context:
        return ''

    value = context[first]
    if callable(value):
        return value()
    elif len(others) and isinstance(value, dict):
        return get('.'.join(others), value)
    else:
        return value


def posts_list(context):
    posts = get("posts", context)
    return posts and f'{[get("post.name", {"post": post}) for post in posts]}'


print(posts_list({'posts': POSTS}))


def base_template(context: dict, blocks: dict) -> str:
    return f'''
<head>
<title>{get('title', blocks) or 'Последние обновления на сайте'}</title>
</head>
<body>
<h1>{get('header', blocks) or 'Последние обновления на сайте'}</h1>
{get('content', blocks)}
</body>
'''


print(base_template({}, {}))


def extends(extended_func):
    def decorator(func):
        def wrapper(context):
            blocks = func(context)
            return extended_func(context, blocks)
        return wrapper
    return decorator


@extends(base_template)
def posts_lists(context):
    return {
        'header': f'Всего постов на сайте {len(get("posts", context))}',
    }


print(posts_lists({'posts': POSTS}))


filters = {
    'length': lambda value, _: len(value)
}


def filter_(value, name, arg: str = None):
    func = filters.get(name)
    if func:
        return func(value, arg)
    else:
        return ''


@extends(base_template)
def posts_lists(context):
    return {
        'header': f'Всего постов на сайте {filter_(get("posts", context), "length")}',
    }


print(posts_lists({'posts': POSTS}))

new_line = '\n'


@extends(base_template)
def posts_lists(context):
    return {
        'header': f'Всего постов на сайте {filter_(get("posts", context), "length")}',
        'content': f'''
            <p>Список постов/p>
{new_line.join([get('post.name', {"post": post}) for post in get("posts", context)])}
        '''
    }


print(posts_lists({'posts': POSTS}))


def post_item(context):
    return f'<a href="#">Post: {get("post.name", context)}</a>\n'


print(post_item({"post": POSTS[0]}))


def include(func, context, with_=None):
    if with_ is None:
        with_ = {}
    return func({**context, **with_})


@extends(base_template)
def posts_lists(context):
    content = '\n'.join([
        include(post_item, context, with_={"post": post})
        for post in get("posts", context)
    ])
    return {
        'header': f'Всего постов на сайте {filter_(get("posts", context), "length")}',
        'content': f'''
            <p>Список постов/p>
{content}
        '''
    }


print(posts_lists({'posts': POSTS}))


