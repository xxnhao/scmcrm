import openpyxl
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def export_excel(request):
    data = request.POST.get('data')  # 获取POST请求发送的表格数据
    wb = openpyxl.Workbook()  # 创建一个新的Excel工作簿
    ws = wb.active
    rows = data.split('\n')
    for i,row in enumerate(rows):
        row_data = row.split(',')
        for j,cell in enumerate(row_data):
            ws.cell(row=i + 1,column=j + 1,value=cell)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=myfile.xlsx'
    wb.save(response)
    return response
