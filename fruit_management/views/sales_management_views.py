import csv
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import make_aware

from constant import type_conversion_to_datetime, is_valid_datetime
from fruit_management.models.fruit import Fruit, Sales
from fruit_management.forms import SalesForm


def csv_validate(row):
    """読み込んだCSVデータが正常か検証する

    NGデータはFalseとなり、Insert対象から除外される
    """

    count = 0
    csv_fruit_name = row.get("果物")
    csv_quantity = row.get("個数")
    csv_sales_date = row.get("販売日時")
    fruit = Fruit.objects.filter(name=csv_fruit_name).exists()

    if csv_fruit_name and fruit:
        count += 1
    if csv_quantity and csv_quantity.isdecimal():
        count += 1
    if csv_sales_date and is_valid_datetime(csv_sales_date):
        count += 1

    if count == 3:
        return True

    return False


def csv_insert(file):
    """CSV Insert

    ToDo:
        例外処理の実装
    """

    csv_dict_reader = csv.DictReader(file)
    validated_data = []

    try:
        for row in csv_dict_reader:
            is_valid = csv_validate(row)
            if is_valid:
                validated_data.append(row)
    except Exception as e:
        print(e)

    # Insert処理
    try:
        for dict in validated_data:
            fruit_name = dict["果物"]
            quantity = dict["個数"]
            sales_date = make_aware(type_conversion_to_datetime(dict["販売日時"]))

            # 該当するfruitのデータを取得する
            fruit = Fruit.objects.get(name=fruit_name)
            # 販売金額を計算する
            sum_price = fruit.price * int(quantity)

            # objectを生成し、DBに保存する
            sales = Sales.objects.create(
                fruit_name=fruit.name,
                quantity=quantity,
                sales=sum_price,
                sales_date=sales_date,
            )
            sales.save()

        return True

    except Exception as e:
        print(e)


@login_required
def sales_list(request):
    """sales index"""

    success_redirect = "sales_index"

    # POST
    if request.method == "POST":
        # Uploadファイルを取得する
        upload_file = request.FILES.get("upload_file")
        # InMemoryUploadedFileなので利用できる形に変換する
        file_data = TextIOWrapper(upload_file.file, encoding="utf-8")
        finish_flag = csv_insert(file_data)

        if finish_flag:
            return redirect(success_redirect)

    # GET
    template_name = "sales_management/index.html"
    sales_obj = Sales.objects.all().order_by("-sales_date")
    context = {"object_list": sales_obj}

    return render(request, template_name, context)


@login_required
def sales_register(request):
    """salesの登録関数
    ClassBasedViewでは時間がかかりそうだったため、一旦関数ベースで実装する
    """
    template_name = "sales_management/register.html"
    success_redirect = "sales_index"

    if request.method == "POST":
        create_form = SalesForm(request.POST or None)
        if create_form.is_valid():
            # Postされたフォーム値を取得する
            fruit_name = create_form.cleaned_data["fruit_name"]
            quantity = create_form.cleaned_data["quantity"]
            sum_price = 0
            sales_date = create_form.cleaned_data["sales_date"]

            # 該当するfruitのデータを取得する
            fruit = Fruit.objects.get(pk=fruit_name)
            # 販売金額を計算する
            sum_price = fruit.price * int(quantity)

            # objectを生成し、DBに保存する
            sales = Sales.objects.create(
                fruit_name=fruit.name,
                quantity=quantity,
                sales=sum_price,
                sales_date=sales_date,
            )
            sales.save()

            return redirect(success_redirect)
    else:
        create_form = SalesForm()

    return render(
        request,
        template_name,
        context={"form": create_form},
    )


@login_required
def sales_edit(request, pk):
    """salesの編集関数
    Createを関数ベースにした手前、Editも関数にする。
    ClassBasedViewでは時間がかかりそうだったため。
    """
    template_name = "sales_management/edit.html"
    success_redirect = "sales_index"
    sales_instance = Sales.objects.get(pk=pk)

    if request.method == "POST":
        edit_form = SalesForm(request.POST or None)
        if edit_form.is_valid():
            # Postされたフォーム値を取得する
            fruit_name = edit_form.cleaned_data["fruit_name"]
            quantity = edit_form.cleaned_data["quantity"]
            sum_price = 0
            sales_date = edit_form.cleaned_data["sales_date"]

            # 該当するfruitのデータを取得する
            fruit = Fruit.objects.get(pk=fruit_name)
            # 販売金額を計算する
            sum_price = fruit.price * int(quantity)

            sales_instance.fruit_name = fruit.name
            sales_instance.quantity = quantity
            sales_instance.sales = sum_price
            sales_instance.sales_date = sales_date
            sales_instance.save()

            return redirect(success_redirect)
    else:
        edit_form = SalesForm(request.POST or None, instance=sales_instance)

    return render(
        request,
        template_name,
        context={"form": edit_form},
    )


def sales_delete(request, pk):
    """Sales Delete"""
    template_name = "sales_management/delete.html"
    sales = get_object_or_404(Sales, pk=pk)

    if request.method == "POST":
        sales.delete()
        return redirect("sales_index")

    return render(request, template_name, {"object": sales})
