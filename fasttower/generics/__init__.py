from fasttower.db import get_object_or_404
from fasttower.db.models import Model
from fasttower.routers import APIRouter
from fasttower.serializers import ModelSerializer

non_lookup_methods = {
    'list': 'GET',
    'create': 'POST',
}

lookup_methods = {
    'retrieve': 'GET',
    'update': 'PUT',
    'destroy': 'DELETE',
}


class GenericViewSet:
    queryset: Model = None
    serializer_class: ModelSerializer = None

    lookup_field: str = '{pk}'

    extra_router_kwargs: dict = {}
    router = APIRouter(**extra_router_kwargs)

    action = None

    def __init__(self, prefix):
        self.prefix = prefix
        self.dispatch()

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_class

    def dispatch(self):
        for action, method in {**non_lookup_methods,
                               **lookup_methods}.items():
            if not hasattr(self, action):
                continue
            self.action = action
            self.add_route(action, method)

    def add_route(self, action: str, method: str, ):
        path = '/' if action in non_lookup_methods else f'/{self.lookup_field}'
        response_model = list[self.get_serializer_class()] if action == 'list' else self.get_serializer_class()
        self.router.add_api_route(
            path,
            getattr(self, action),
            response_model=response_model,
            methods=[method],
        )

    async def get_object(self, pk):
        return await get_object_or_404(self.queryset, pk=pk)
