from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction as db_transaction
from decimal import Decimal
from .models import SavingsGoal, SavingsTransaction
from .forms import SavingsGoalForm, AddFundsForm, WithdrawFundsForm


@login_required
def savings_goals_list(request):
    goals = SavingsGoal.objects.filter(user=request.user).exclude(status="CANCELADO")

    total_saved = sum(goal.current_amount for goal in goals)
    total_target = sum(goal.target_amount for goal in goals)
    overall_progress = 0
    if total_target > 0:
        overall_progress = (float(total_saved) / float(total_target)) * 100

    # Enriquecer cada objetivo con colores de progreso
    for goal in goals:
        progress = goal.progress_percentage
        if progress >= 100:
            goal.progress_color = "success"
        elif progress >= 50:
            goal.progress_color = "info"
        elif progress >= 25:
            goal.progress_color = "warning"
        else:
            goal.progress_color = "danger"

    context = {
        "goals": goals,
        "total_saved": total_saved,
        "total_target": total_target,
        "overall_progress": round(overall_progress, 2),
        "wallet_balance": (
            request.user.wallet.balance if hasattr(request.user, "wallet") else 0
        ),
    }
    return render(request, "savings_goals/list.html", context)


@login_required
def create_savings_goal(request):
    if request.method == "POST":
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()

            messages.success(request, f'Objetivo "{goal.name}" creado exitosamente!')
            return redirect("savings_goals:list")
    else:
        form = SavingsGoalForm()

    return render(request, "savings_goals/create.html", {"form": form})


@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
    transactions = goal.transactions.all()[:10]

    context = {
        "goal": goal,
        "transactions": transactions,
        "progress_percentage": goal.progress_percentage,
    }
    return render(request, "savings_goals/detail.html", context)


@login_required
def add_funds(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)

    if goal.status != "ACTIVO":
        messages.error(request, "No puedes agregar fondos a un objetivo inactivo")
        return redirect("savings_goals:list")

    if not hasattr(request.user, "wallet"):
        messages.error(request, "No tienes una billetera configurada")
        return redirect("savings_goals:list")

    user_wallet = request.user.wallet

    if request.method == "POST":
        form = AddFundsForm(request.POST, user_wallet=user_wallet)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            description = form.cleaned_data.get("description", "")

            try:
                with db_transaction.atomic():
                    user_wallet.update_balance(amount, "subtract")
                    goal.add_funds(amount)

                    SavingsTransaction.objects.create(
                        savings_goal=goal,
                        transaction_type="DEPOSIT",
                        amount=amount,
                        description=description or f"Depósito a {goal.name}",
                    )

                    user_wallet.add_transaction(
                        transaction_type="SAVINGS_DEPOSIT",
                        amount=amount,
                        description=f"Depósito a objetivo: {goal.name}",
                        status="COMPLETED",
                    )

                messages.success(
                    request, f'${amount} agregados exitosamente a "{goal.name}"'
                )
                return redirect("savings_goals:list")

            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = AddFundsForm(user_wallet=user_wallet)

    context = {
        "form": form,
        "goal": goal,
        "wallet_balance": user_wallet.balance,
    }
    return render(request, "savings_goals/add_funds.html", context)


@login_required
def withdraw_funds(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)

    if goal.current_amount <= 0:
        messages.error(request, "No hay fondos disponibles para retirar")
        return redirect("savings_goals:detail", goal_id=goal_id)

    if not hasattr(request.user, "wallet"):
        messages.error(request, "No tienes una billetera configurada")
        return redirect("savings_goals:detail", goal_id=goal_id)

    user_wallet = request.user.wallet

    if request.method == "POST":
        form = WithdrawFundsForm(request.POST, savings_goal=goal)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            description = form.cleaned_data.get("description", "")

            try:
                with db_transaction.atomic():
                    goal.withdraw_funds(amount)
                    user_wallet.update_balance(amount, "add")

                    SavingsTransaction.objects.create(
                        savings_goal=goal,
                        transaction_type="WITHDRAWAL",
                        amount=amount,
                        description=description or f"Retiro de {goal.name}",
                    )

                    user_wallet.add_transaction(
                        transaction_type="SAVINGS_WITHDRAWAL",
                        amount=amount,
                        description=f"Retiro de objetivo: {goal.name}",
                        status="COMPLETED",
                    )

                messages.success(
                    request, f'${amount} retirados exitosamente de "{goal.name}"'
                )
                return redirect("savings_goals:detail", goal_id=goal_id)

            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = WithdrawFundsForm(savings_goal=goal)

    context = {
        "form": form,
        "goal": goal,
        "available_amount": goal.current_amount,
    }
    return render(request, "savings_goals/withdraw_funds.html", context)
