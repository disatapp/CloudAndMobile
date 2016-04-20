$(function() {
  $(".container").on("click", ".button", function() { 
    // e.preventDefault();
    $("#display").html("<p>Hello<p>");
    // var name = $('#name').val();
    // var email = $('#email').val();
    // var phone = $('#phone').val();
    // var info = encodeURIComponent('name='+name+'&email='+email+'&phone='+phone);

    // $.ajax({
    //   url: 'http://localhost:10080/customer',
    //   type: 'POST',
    //   dataType: 'json',
    //   contentType: 'application/json',
    //   processData: false,
    //   data: info,
    //   success: function(data) {
    //     alert(JSON.stringify(data));
    //   },
    //   error: function(){
    //     alert("Cannot get data");
    //   }
    // });
  });
});
