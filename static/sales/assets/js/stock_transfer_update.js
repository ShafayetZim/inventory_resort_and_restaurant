
$(document).ready(function () {
     console.log("Stock update view called")

     var product_id = document.getElementById("id_transferable_qty").value;
     var warehouse_id = document.getElementById("id_from_warehouse").value;
     //send_parameters['product_id'] = product_id;
     //send_parameters['warehouse_id'] = warehouse_id;
     call_transferable_qty_api(product_id, warehouse_id);

     $('#id_transferable_qty').on('change', function () {
        console.log("On Product selected")
        //let product = $(this).children('option:selected').val();
        //send_parameters['product_id'] = product;
       // send_parameters['warehouse_id'] = "";
       let product_id = document.getElementById("id_transferable_qty").value;
       let warehouse_id = document.getElementById("id_from_warehouse").value;
        call_transferable_qty_api(product_id,warehouse_id);

    });

     $('#id_from_warehouse').on('change', function () {
            console.log("On Transfer Warehouse called ");
            //let warehouse = $(this).children('option:selected').val();
            //send_parameters['warehouse_id'] = warehouse;
            //console.log(warehouse);
            let product_id = document.getElementById("id_transferable_qty").value;
            let warehouse_id = document.getElementById("id_from_warehouse").value;
            call_transferable_qty_api(product_id,warehouse_id);
      });

});



    function call_transferable_qty_api(product_id, warehouse_id) {
        console.log("call_transferable_qty_api called")
        let send_parameters = {};
        send_parameters ['product_id'] = product_id;
        send_parameters ['warehouse_id'] = warehouse_id;

         $.ajax({
         url: '/stock/transferable-stock-qty/',
         data: send_parameters,
         dataType: 'json',
         success: function (data) {
              console.log(data);
                //document.getElementById("id_transferable_stock_qty").value = data["supervisors"];
                $("#id_transferable_stock_qty").val(data["transferable_qty"]);
            }
         });
    }