def user_access_flags(request):
    if not request.user.is_authenticated:
        return {"user_belongs_to_central": False}

    return {"user_belongs_to_central": request.user.groups.filter(name="Central").exists()}
