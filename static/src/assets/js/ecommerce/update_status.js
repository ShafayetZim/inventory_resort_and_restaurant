    $(function() {
        $('#status-form').submit(function(e) {
            e.preventDefault();
            var _this = $(this)
            $('.err-msg').remove();
            var el = $('<div>')
            el.addClass("alert alert-danger err-msg")
            el.hide()
            if (_this[0].checkValidity() == false) {
                _this[0].reportValidity();
                return false;
            }

            $.ajax({

                url: "update_transaction_status",
                data: new FormData($(this)[0]),
                cache: false,
                contentType: false,
                processData: false,
                method: 'POST',
                type: 'POST',
                dataType: 'json',
                error: err => {
                    console.log(err)
                    alert("An error occured", 'error');
                    end_loader();
                },
                success: function(resp) {
                    if (typeof resp == 'object' && resp.status == 'success') {
                        location.reload()
                    } else if (resp.status == 'failed' && !!resp.msg) {
                        el.text(resp.msg)
                    } else {
                        el.text("An error occured", 'error');
                        end_loader();
                        console.err(resp)
                    }
                    _this.prepend(el)
                    el.show('slow')
                    $("html, body, .modal").scrollTop(0);
                    end_loader()
                }
            })
        })
    })