from django.urls import path
from . import views

app_name = "savings_goals"

urlpatterns = [
    path("", views.savings_goals_list, name="list"),
    path("crear/", views.create_savings_goal, name="create"),
    path("<int:goal_id>/", views.goal_detail, name="detail"),
    path("<int:goal_id>/agregar-fondos/", views.add_funds, name="add_funds"),
    path("<int:goal_id>/retirar-fondos/", views.withdraw_funds, name="withdraw_funds"),
    path("<int:goal_id>/eliminar/", views.delete_goal, name="delete"),
]
