
$(document).ready(function () {

         $(document).ready(function() {
             $('select').select2({
             theme: 'bootstrap4',

             });
          });
    getCustomers();

})




function getCustomers() {
    let url = $("#client_name").attr("url");
    console.log(url);
    console.log("getCustomers");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            console.log(result)
            countries_option = "<option value='all' selected>--Select Client--</option>";
            $.each(result["customers"], function (a, b) {
                countries_option += "<option>" + b + "</option>"
            });
            $("#client_name").html(countries_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}
