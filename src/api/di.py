from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.data_source.wikiwiki import WikiWikiDataSource


class DIContainer(containers.DeclarativeContainer):
    data_source = providers.Factory(WikiWikiDataSource)


@inject
def get_context(data_source=Depends(Provide[DIContainer.data_source])):
    return {"data_source": data_source}
