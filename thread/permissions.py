from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    # CREATE, LIST
    def has_permission(self, request, view):
        print('11111111111111111111111')
        print(request.method)
        print('11111111111111111111111')
        print('22222222222222222222')
        # print(obj.author)
        print('33333333333333333333')
        print(request.user)
        print('44444444444444444444')
        print(dir(request))
        print('*******************************************')
        print(SAFE_METHODS)
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff

    # UPDATE, DELETE, RETRIEVE
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print('******************')
        print(obj.author)
        print('******************')
        print(view.name)
        if request.method == 'DELETE':
            return request.user == obj.author
        elif request.method == 'GET':
            return True
        return request.user.is_authenticated and request.user.is_staff
