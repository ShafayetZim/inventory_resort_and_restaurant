    function calc_total() {
        var sub_product = 0
        var gtotal = 0

        $('#product_list tbody tr').each(function() {
            var price = $(this).find('[name="product_price[]"]').val()
            var max = $(this).find('[name="product_available[]"]').val()
            var qty = $(this).find('[name="product_quantity[]"]').val()
            qty = qty > 0 ? qty : 0;
            price = price > 0 ? price : 0;
            sub_product += parseFloat(parseFloat(qty) * parseFloat(price))
            gtotal += parseFloat(parseFloat(qty) * parseFloat(price))
            $(this).find('.product_total').text(parseFloat(parseFloat(qty) * parseFloat(price)).toLocaleString('en-US'))
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
        // Select Box
        new TomSelect("#client",{
            create: false,
            sortField: {
                field: "text",
                direction: "asc",
            }
        });
        new TomSelect("#products",{
            create: false,
            placeholder: "Please Select Product Here",
            sortField: {
                field: "text",
                direction: "asc",
            }
        });
        $('#road').select2({
            placeholder: "Please Select Road Name Here",
            width: "100%",
            selectionCssClass: "form-control form-control-sm rounded-0"
        })

        $('#product_list tbody').find('[name="product_price[]"]').on('input change', function() {
            calc_total()
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
            if (pid < '1') {
                return false
            }
            var unit = $('#products option[value="' + pid + '"]').attr('data-unit')
            var buy = $('#products option[value="' + pid + '"]').attr('data-buy')
            var price = $('#products option[value="' + pid + '"]').attr('data-price')
            var max = $('#products option[value="' + pid + '"]').attr('data-available')
            var product_name = $('#products option[value="' + pid + '"]').text()
            var tr = $($('noscript#product-clone').html()).clone()
            tr.find('.product_type').text(product_name)
            tr.find('.product_unit').text(String(unit).toLocaleString('en-US'))
            tr.find('.product_buy').text(parseFloat(buy).toLocaleString('en-US'))
            tr.find('.product_price').text(parseFloat(price).toLocaleString('en-US'))
            tr.find('.product_total').text(parseFloat(price).toLocaleString('en-US'))
            tr.find('.product_available').text(parseFloat(max).toLocaleString('en-US'))
            tr.find('[name="product_id[]"]').val(pid)
            tr.find('[name="product_unit[]"]').val(unit)
            tr.find('[name="product_price[]"]').val(price)
            tr.find('[name="product_available[]"]').val(max)
            tr.find('[name="product_quantity[]"]').val()

            $('#product_list tbody').append(tr)
            calc_total()
            $('#products').val('').trigger('change')
            tr.find('[name="product_quantity[]"]').on('input change', function() {
                calc_total()
            })
            calc_total()
            $('#products').val('').trigger('change')
            tr.find('[name="product_price[]"]').on('input change', function() {
                calc_total()
            })

            tr.find('.rem-product').click(function() {
                if (confirm("Are you sure to remove this item?") == true) {
                    tr.remove()
                    calc_total()
                }
            })
        })


        $('input[name="total_amount"]').change(function(){
            var sub = $(this).val();
            var paid = $('input[name="paid"]').val();
            var due = parseFloat(sub) - parseFloat(paid);
            $('#due_amount').val(due);

        });

         $('input[name="paid"]').on('input',function(){
                var paid = $(this).val();
                var sub = $('input[name="total_amount"]').val();
                var due = parseFloat(sub) - parseFloat(paid);
                $('#due_amount').val(due);
        });

        $('#pay_later').click(function() {
            $('#paid_amount').val(0).attr('required', false)
            $('#sell-form').submit()
        })
        $('#sell-submit-btn').click(function() {
            $('#paid_amount').attr('required', true)
        })

        $('#sell-form').submit(function(e) {
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
            if ($('#paid_amount').prop('required') == true) {
                var change = $('#change').text()
                change = change.replace(/,/gi, '')
                change = !isNaN(change) ? change : 0
                if (change < 0) {
                    alert("Paid amount is invalid.")
                    return false
                }
            }

            $.ajax({
                url: 'save_sell',
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
                        location.replace('view_invoice/' + resp.id)
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