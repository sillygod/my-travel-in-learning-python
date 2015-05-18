# What is django-zoo

django-zoo contains lots of apps I want to practice and implement. There is no speciifc type of apps. I just do what I want :)

# sturcutre

Basically, I follow the django-admin startapp's strucutre and every app should contains `urls.py`. The url patterns should be something like the following.


```
patterns =(
    '',
    url(r'^app_name/$', include('app_name.urls'), name=''),
    ...
)
```

It is a **good** habit to named the url pattern.

### about the templates and static folder

their structure follow the rule below

```
static
    app1/
        css/
        js/
        img/
        ..
    app2/
        css/
        js/
        img/
        ,,

templates/
    app1/
        xxx.html
        ..
    app2/
        ...
        .
```

well, maybe I should use reusable app structure here. That means every app should has the structure like the following.

```
app/
    static/
        ...
    template/
        ...
    urls.py
    models.py
    views.py
    ..
    .
```

I have not decided which one to use yet.
