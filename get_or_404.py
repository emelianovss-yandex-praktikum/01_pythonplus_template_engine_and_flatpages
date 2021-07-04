def get_object_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except DoesNotExists:
        raise HttpError(404)




get_object_or_404(MyModel, pk=1)


