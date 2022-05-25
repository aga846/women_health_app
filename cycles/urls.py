from django.urls import path
from . import views

app_name = "cycles"

urlpatterns = [
    path("baby/", views.baby, name="baby"),
    path("no_baby/", views.no_baby, name="no_baby"),
    path("add_new_cycle", views.add_new_cycle, name="add_new_cycle"),
    path("about/<int:pk>", views.about, name="about"),
    path("temperatures/<int:pk>", views.temperatures, name="temperatures"),
    path("add_temperature/<int:pk>", views.add_temperature, name="add_temperature"),
    path("cycles_list/<str:user>", views.cycles_list, name="cycles_list"),
    path("confirm_delete/<int:pk>", views.confirm_delete, name="confirm_delete"),
    path("delete_cycle/<int:pk>", views.delete_cycle, name="delete_cycle"),
    path("update_cycle/<int:pk>", views.update_cycle, name="update_cycle")
]
