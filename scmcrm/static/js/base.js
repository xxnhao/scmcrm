    $(function (){

        $('.select2').select2()

    })

    function del(url){
        Modal.confirm({
        msg: "确定要删除吗？",
        title: ' 信息提示',
        btnok: '确定',
        btncl:'取消'
      }).on(function (e){
        if(e){
          window.location.href=url;
          //Modal.alert({msg: "成功删除",title: ' 信息提示',btnok: '确定',btncl:'取消'});
        }
      });
    }

    /**
     * 为了实现弹窗提醒，使用ajax提交from请求
     */
   $('#myform').submit(function(event) {
        event.preventDefault(); // 阻止表单默认提交
        // 提交表单数据
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            success: function(response) {
                // 根据返回内容弹窗提示
                Modal.alert({msg: response ,title: ' 信息提示', btnok: '确定', btncl:'取消'});
            },
            error: function(xhr, status, error) {

            console.log(xhr.responseText);
            }
        });
    });
