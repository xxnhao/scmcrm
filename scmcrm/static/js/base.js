$(function () {

    $('.select2').select2()

})

// 获取CSRF令牌的cookie值
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getStore(url) {
    Modal.confirm({
        msg: "更新客户门店列表，可能会需要一些时间，确定要执行吗？",
        title: ' 信息提示',
        btnok: '确定',
        btncl: '取消'
    }).on(function (e) {
        if (e) {
            //window.location.href = url;
            Modal.alert({msg: "正在更新，请稍后！", title: ' 信息提示', btnok: '确定', btncl: '取消'});
            $.ajax({
                url: url,
                type: "GET",
                success: function (response) {
                    console.log(response);
                    Modal.alert({msg: response, title: ' 信息提示', btnok: '确定', btncl: '取消'});
                },
                error: function (xhr) {
                    console.log(xhr.responseText);
                }
            });
        }
    });
}

function del(url) {
    Modal.confirm({
        msg: "确定要删除吗？",
        title: ' 信息提示',
        btnok: '确定',
        btncl: '取消'
    }).on(function (e) {
        if (e) {
            window.location.href = url;
            //Modal.alert({msg: "成功删除",title: ' 信息提示',btnok: '确定',btncl:'取消'});
        }
    });
}

/**
 * 为了实现弹窗提醒，使用ajax提交from请求
 */
$('#myform').submit(function (event) {
    event.preventDefault(); // 阻止表单默认提交
    // 提交表单数据
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize(),
        success: function (response) {
            // 根据返回内容弹窗提示
            Modal.alert({msg: response, title: ' 信息提示', btnok: '确定', btncl: '取消'});
        },
        error: function (xhr, status, error) {

            console.log(xhr.responseText);
        }
    });
});

function excledl(url) {
    // 获取表格数据
    var table = document.getElementById('data-table');
    var rows = table.rows;
    var data = [];
    for (var i = 0; i < rows.length; i++) {
        var rowData = [];
        var cells = rows[i].cells;
        for (var j = 0; j < cells.length; j++) {
            rowData.push(cells[j].innerText);
        }
        data.push(rowData);
    }
    //设置csrf证书
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
    // 发送数据给Django
    $.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        responseType: 'blob',
        success: function (response) {
            // 生成Excel成功后，返回的response是一个文件下载链接
            console.log(response)
            const blob = new Blob([response], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'data.xlsx';
            link.click();
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('Error:', errorThrown);
        }
    })
}
