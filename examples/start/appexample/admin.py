from fastapi_admin.resources import Model, Dropdown
from fasttower import admin

from appexample import models


@admin.site.app.register
class AppexampleTabMenu(Dropdown):
    label = "Appexamples"
    icon = "fas fa-bars"
    resources = []
    title = "Appexamples"