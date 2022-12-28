
$(document).ready(function () {
     console.log("Sales Collections called")
     customer_id = $("#customer-change").val();
      getPreviousDueByCustomer(customer_id);
     $('.previousdue ').on('select2:select', function (e) {
            console.log("On Customer changed")
            var data = e.params.data;
            console.log(data);
            getPreviousDueByCustomer(data.id);
        });

});


    function getPreviousDueByCustomer( customer_id) {
        console.log("getPreviousDueByCustomer")
        let send_parameters = {};
        send_parameters ['customer_id'] = customer_id;

         $.ajax({
         url: '/accounts/previous-due-by-customer/',
         data: send_parameters,
         dataType: 'json',
         success: function (data) {
              console.log(data['previous_due']);
              $('#previous_due').val(data['previous_due']);
            }
         });
    }