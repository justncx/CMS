$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        zlalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/aboard/',
                    'data': {
                        'name': inputValue,
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        }else{
                           zlalert.alertInfo(data['message']);

                        }
                    },
                    'fail': function (error) {
                        zlalert.alertNetworkError();
                    }
                })
            }

        })
    })
});


$(function () {
    $(".edit-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');
        console.log(name);
        console.log(board_id);
        console.log(tr);

        zlalert.alertOneInput({
            'text': '请输入新的板块的名称',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/uboard/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
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
    $(".delete-board-btn").click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var board_id = tr.attr('data-id');
       event.preventDefault();
       zlalert.alertConfirm({
           'msg': '确定删除这个板块',
           'confirmCallback': function () {
               zlajax.post(
                   {
                   'url': '/cms/dboard/',
                   'data': {
                       'board_id': board_id
                   },
                   'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        }else {
                            console.log(data['message']);
                            zlalert.alertInfo(data['message'])
                        }
                    }
                })
            }
        })
    })
});