var send_data = {}
//stores the total no of item forms
 var total = 0;
 var initial_form_count = 0;
$(document).ready(function () {
      console.log("Total Form length: "+ $('.form-row').length);
      total = $('.form-row').length;
      initial_form_count = $('.form-row').length;

     $('#id_customer').on('change', function () {
        console.log("On Customer selected")
        let customer_code = $(this).children('option:selected').val();
        console.log(customer_code);
        $.ajax({
            url: 'customer-information',
            data: {
              'customer_code': customer_code
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $("#id_address").val(data.address);
                $("#id_phone").val(data.phone);

            }
        });
    });


    $('#id_warehouse').on('change', function () {
        console.log("On Warehouse selected")
        let warehouse_id = $(this).children('option:selected').val();
        console.log(warehouse_id);
        updateStockQtyOnWarehouseChange(warehouse_id);
    });

});

     //creates custom alert object
        //var custom_alert = new custom_alert();

        function updateElementIndex(el, prefix, ndx) {
            var id_regex = new RegExp('(' + prefix + '-\\d+)');
            var replacement = prefix + '-' + ndx;
            if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
            if (el.id) el.id = el.id.replace(id_regex, replacement);
            if (el.name) el.name = el.name.replace(id_regex, replacement);
        }


        function cloneMore(selector, prefix) {
            var newElement = $(selector).clone(true);
            //var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
            newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
                var name = $(this).attr('name')
                if(name) {
                    name = name.replace('-' + (total-1) + '-', '-' + total + '-');
                    var id = 'id_' + name;
                    $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
                }
            });
            newElement.find('label').each(function() {
                var forValue = $(this).attr('for');
                if (forValue) {
                forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
                $(this).attr({'for': forValue});
                }
            });
            total++;
            $('#id_' + prefix + '-TOTAL_FORMS').val(total);
            $(selector).after(newElement);
            return false;
        }

        function deleteForm(prefix, btn) {
            //var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
            if (total > 1){
                btn.closest('.form-row').remove();
                var forms = $('.form-row');
                $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
                for (var i=0, formCount=forms.length; i<formCount; i++) {
                    $(forms.get(i)).find(':input').each(function() {
                        updateElementIndex(this, prefix, i);
                    });
                }
                total--;
            } else {
                alert("Must have at least one item");

            }
            return false;
        }

        $(document).on('click', '.add-form-row', function(e){
            e.preventDefault();
            cloneMore('.form-row:last', 'form');
            return false;
        });

        $(document).on('click', '.remove-form-row', function(e){
            e.preventDefault();
            deleteForm('form', $(this));
            setTotalQtyAndAmount();
            return false;
        });


        //updates the total price by multiplying 'price per item' and 'quantity'
        $(document).on('change', '.setprice', function(e){
            e.preventDefault();
            //gets the values
            var element = $(this);
            var item = element.parents('.form-row').find('.product').val();
            var quantity = element.parents('.form-row').find('.quantity').val();
            var perprice = element.parents('.form-row').find('.price').val();

            //calculates the total
            var tprice = quantity * perprice;
            //sets it to field
            element.parents('.form-row').find('.amount').val(tprice);

           setTotalQtyAndAmount();
           getAvailableStockByWarehouse(element, item);

            //Set Total
             //$("#sales_total_amount").val(total_price);
             //$("#sales_total_qty").val(total_qty);
            return false;
        });

        function updateStockQtyOnWarehouseChange(warehouse_id){

                for (var i=0;  i<total; i++) {
                     let item = document.getElementById("id_form-"+i+"-product").value;
                     var element = document.getElementById("id_form-"+i+"-extra_field");
                      console.log("Item: "+item);
                      console.log("Warehouse: "+warehouse_id);

                      getAvailableStockByWarehouseAll(element, item, warehouse_id);
                }

        }

        function getAvailableStockByWarehouseAll(element, item, warehouse_id) {
            $.ajax({
                url: '/sales/get-available-stock-by-warehouse',
                data: {
                  'warehouse_id': warehouse_id,
                  'item': item,
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    element.value = data.stock;
                    console.log(element);
                }
            });

        }

        function getAvailableStockByWarehouse(element, item) {
            console.log("On Item Selected for Stock ")
             var warehouse_id = $('#id_warehouse').val();
             console.log("WarehouseID: "+ warehouse_id);
             console.log("Item : "+ item);

            $.ajax({
                url: '/sales/get-available-stock-by-warehouse',
                data: {
                  'warehouse_id': warehouse_id,
                  'item': item,
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    element.parents('.form-row').find('.extra_field').val(data["stock"]);
                    //element.parents('.form-row').find('.stock-qty').val(data["stock"]);
                }
            });

        }


        function setTotalQtyAndAmount() {
            console.log("Set Total Qty and Amount called");
            var total_price = 0
            var total_qty = 0

             for (var i=0;  i<total; i++) {
                     console.log("Form length count: "+i)
                     var amount = document.getElementById("id_form-"+i+"-amount").value;
                     var qty = document.getElementById("id_form-"+i+"-quantity").value;
                     console.log("Amount: "+amount);
                     console.log("Qty: "+qty);

                     if(amount != '' && qty != ''){
                        total_price += parseFloat(amount);
                        total_qty += parseFloat(qty);
                     }

                }

             var paid_amount = document.getElementById("sales_paid_amount").value;
             var due_amount = total_price - paid_amount;

             //Set total calculation
             $("#sales_total_amount").val(total_price);
             $("#sales_total_qty").val(total_qty);
             $("#sales_due_amount").val(due_amount);

        }

     $('#sales_paid_amount').keyup(function () {
        var paid_amount = $(this).val();
        var total_amount = document.getElementById("sales_total_amount").value;
        var due_amount = total_amount - paid_amount;
        $("#sales_due_amount").val(due_amount);

   });
