    $(document).ready(function () {
        console.log("On Page Loaded")
        $('#products').on('change', function () {
            console.log("On Product selected")
        });
    });


    function calc_total() {
        var sub_product = 0
        var gtotal = 0
        $('#product_list tbody tr').each(function() {
            var buy = $(this).find('[name="product_price[]"]').val()
            var qty = $(this).find('[name="product_quantity[]"]').val()
            var unit = $(this).find('[name="unit_value[]"]').val()
            qty = qty > 0 ? qty : 0;
            buy = buy > 0 ? buy : 0;
            sub_product += parseFloat(parseFloat(qty) * parseFloat(buy))
            gtotal += parseFloat(parseFloat(qty) * parseFloat(buy))
            $(this).find('.product_total').text(parseFloat(parseFloat(qty) * parseFloat(buy)).toLocaleString('en-US'))
        })
        $('.sub-total-product').text(parseFloat(sub_product).toLocaleString('en-US', {
            style: 'decimal',
            maximumFractionDigits: 2,
            minimumFractionDigits: 2
        }))
        $('[name="total_amount"]').val(gtotal)
        $('.gtotal').text(parseFloat(gtotal).toLocaleString('en-US', {
            style: 'decimal',
            maximumFractionDigits: 2,
            minimumFractionDigits: 2
        }))
        $
    }
    $(function() {
        calc_total()
        $('#brand').select2({
            placeholder: "Please Select Brand Here",
            width: "100%",
            selectionCssClass: "form-control form-control-sm rounded-0"
        })
        new TomSelect("#products",{
            create: false,
            placeholder: "Please Select Product Here",
            sortField: {
                field: "text",
                direction: "asc",
            }
        });

        $('#pay_later').click(function() {


        })

        $('#product_list tbody').find('[name="product_quantity[]"]').on('input change', function() {
            calc_total()
        })
        $('#product_list tbody').find('.rem-product').click(function() {
            if (confirm("Are you sure to remove this item?") == true) {
                $(this).closest('tr').remove()
                calc_total()
            }
        })

        $('#add_product').click(function() {
            var pid = $('#products').val()

            var buy = $('#products option[value="' + pid + '"]').attr('data-price')
            var unit = $('#products option[value="' + pid + '"]').attr('data-unit')
            var product_name = $('#products option[value="' + pid + '"]').text()
            var tr = $($('noscript#product-clone').html()).clone()
            tr.find('.product_type').text(product_name)
            tr.find('.product_unit').text(String(unit).toLocaleString('en-US'))
            tr.find('.product_price').text(parseFloat(buy).toLocaleString('en-US'))
            tr.find('.product_total').text(parseFloat(buy).toLocaleString('en-US'))
            tr.find('[name="product_id[]"]').val(pid)
            tr.find('[name="product_price[]"]').val(buy)
            tr.find('[name="product_unit[]"]').val(unit)

            $('#product_list tbody').append(tr)
            calc_total()
            $('#products').val('').trigger('change')
            tr.find('[name="product_quantity[]"]').on('input change', function() {
                calc_total()
            })
            tr.find('.rem-product').click(function() {
                if (confirm("Are you sure to remove this item?") == true) {
                    tr.remove()
                    calc_total()
                }
            })
        })
        $('#purchase-form').submit(function(e) {
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
                url: 'save_purchase',
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
                        location.replace('purchase')
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