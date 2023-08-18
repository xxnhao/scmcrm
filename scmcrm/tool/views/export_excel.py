from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from openpyxl import Workbook

@csrf_exempt
def export_excel(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        # 生成 Excel 文件
        wb = Workbook()
        sheet = wb.active

        for row in data:
            sheet.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=data.xlsx'

        wb.save(response)

        return response

    return HttpResponse('Method Not Allowed', status=405)