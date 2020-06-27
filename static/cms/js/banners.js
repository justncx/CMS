$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name=name]");
        var imageInput = $("input[name=image-url]");
        var linkInput = $("input[name=link-url]");
        var priorityInput = $("input[name=priority]");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr('data-id');

        console.log(name);
        console.log(image_url);
        console.log(link_url);
        console.log(priority);
        if (!name || !image_url || !link_url || !priority){
            zlalert.alertInfoToast('请输入完整的轮播图数据');
            return;
        }
        var url = '';
        if (submitType == 'upgrade'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/abanner/'
        }
        zlajax.post({
            'url': url,
            'data':{
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                dialog.modal('hide');
                if (data['code'] == 200){
                // 重新加载整个页面
                    window.location.reload();
                    zlalert.alertSuccessToast('添加成功');
                }else {
                    console.log('error');
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function () {
                console.log('error');
                zlalert.alertNetworkError();
            }
        })
    });
});


$(function () {
    $(".edit-banner").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal('show');

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name=name]");
        var imageInput = dialog.find("input[name=image-url]");
        var linkInput = dialog.find("input[name=link-url]");
        var priorityInput = dialog.find("input[name=priority]");

        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type", 'upgrade');
        saveBtn.attr("data-id", tr.attr('data-id'));

        console.log(name);
        console.log(image_url);
        console.log(link_url);
        console.log(priority);

        // if (!name || !image_url || !link_url || !priority){
        //     zlalert.alertInfoToast('请输入完整的轮播图数据');
        //     return;
        // }


    });
});


$(function () {
   $(".delete-banner").click(function (event) {
       var self = $(this);
       var tr = self.parent().parent();
       var banner_id = tr.attr('data-id');
       event.preventDefault();
       zlalert.alertConfirm({
           'msg': '确定删除这个轮播图',
           'confirmCallback': function () {
               zlajax.post({
                   'url': '/cms/dbanner/',
                   'data': {
                       'banner_id': banner_id
                   },
                   'success': function (data) {
                       if (data['code']==200){
                           window.location.reload()
                       }else {
                           zlalert.alertInfo(data['message'])
                       }
                   }
               })
           }
       })
   })
});

$(function () {
    zlqiniu.setUp({
        'domain': 'http://qcjhplfsu.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/common/uptoken/',
        'success': function (up,file,info) {
            var imageInput = $("input[name='image-url']");
            imageInput.val(file.name);
        }
    });
});