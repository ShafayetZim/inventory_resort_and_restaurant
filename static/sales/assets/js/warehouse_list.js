var lc_transaction_no;

$(document).ready(function () {
     getWarehouse();
     $('.warehouse_name').on('change', function () {
        console.log("On Warehouse selected")
        $('#closemodal'+lc_transaction_no).find('.modal-body').find('.warehouse_error_message').html('');
    });


})


$(document).on('click', '.closed_lc_btn', function () {
    console.log("Closed LC Button Clicked ")
    var url = 'new-lc-closed';
    lc_transaction_no = $(this).attr('id');
    //var element = document.getElementById("warehouse_id");
	var element = $('#closemodal'+lc_transaction_no).find('.modal-body').find('#warehouse_id');
    var warehouse_id = element.val();
    console.log(warehouse_id)

    if (warehouse_id==='all'|| warehouse_id === null || warehouse_id === ""){
        console.log("Please select warehouse")
       $('#closemodal'+lc_transaction_no).find('.modal-body').find('.warehouse_error_message').html('Please select warehouse');

    }else{
     $('#closemodal'+lc_transaction_no).find('.modal-body').find('.warehouse_error_message').html('');
     console.log("Ready to go...")
     document.location.href = url + "/" + lc_transaction_no + "/" + warehouse_id;
    }
    // Construct the full URL with "id"
});

$(document).on('click', '#process_btn_id', function () {
    console.log("Process Button Clicked ")
    getWarehouse();
});

function getWarehouse() {
        console.log("getWarehouse Called")
        let url = $(".warehouse_name").attr("url");
        $.ajax({
            method: 'GET',
            url: url,
            data: {},
            success: function (result) {
                console.log(result)
                countries_option = "<option value='all' selected>Select....</option>";
                $.each(result, function (a, b) {
                    countries_option += "<option value="+b.id+">" + b.warehouse_name + "</option>"
                });
                $(".warehouse_name").html(countries_option)
            },
            error: function(response){
                console.log(response)
            }
        });
    }


function sendWarehouseName() {
        console.log("getWarehouse Called")
        let url = $(".warehouse_name").attr("url");
        $.ajax({
            method: 'GET',
            url: url,
            data: {},
            success: function (result) {
                console.log(result)
                countries_option = "<option value='all' selected>Select....</option>";
                $.each(result, function (a, b) {
                    countries_option += "<option value="+b.id+">" + b.warehouse_name + "</option>"
                });
                $(".warehouse_name").html(countries_option)
            },
            error: function(response){
                console.log(response)
            }
        });
    }


