class ListModelMixin:
    async def list(self) -> 'serializer_class':
        return await self.get_queryset()


class CreateModelMixin:
    async def create(self) -> 'serializer_class':
        return

    async def perform_create(self, instance: 'queryset'):
        instance.save()


class RetrieveModelMixin:
    async def retrieve(self, pk) -> 'serializer_class':
        obj = await self.get_object(pk)
        return obj


class UpdateModelMixin:
    async def update(self, pk) -> 'serializer_class':
        obj = await self.get_object(pk)
        await self.perform_update(obj)
        return obj

    async def perform_update(self, instance: 'queryset'):
        await instance.save()


class DeleteModelMixin:
    async def destroy(self, pk) -> 'serializer_class':
        obj = await self.get_object(pk)
        await self.perform_destroy(obj)
        return obj

    async def perform_destroy(self, instance: 'queryset'):
        await instance.delete()
