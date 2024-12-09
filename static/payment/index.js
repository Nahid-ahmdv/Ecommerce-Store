
//'use strict';
// document.cookie = "name=value; SameSite=None; Secure";

var stripe = Stripe('pk_test_51QPpMhBpSXWsClGe5m2XjTqwZUcCreFcHaXiZqt8Pz0phJdg8N9M9D7UuvH1oOgYr4mAlgJsUJa5L1NXggtyNTH700KqTgKMwR');
// we're now gonna build a simple stripe element for the payment. first we check out this address 'https://docs.stripe.com/payments/elements'.
var elem = document.getElementById('submit'); //identifying the submit button. we're gonna store that in a variable called 'elem'. so that's a submit element.
clientsecret = elem.getAttribute('data-secret'); // we're gonna need the client id in order to take a payment. we're gonna need that 'client-secret', we stored it in 'data-secret'on the homepay.html.
//To process a payment, we need the 'client_secret', which we previously collected. As you may recall, we generated this 'client_secret' in the 
// 'BasketView' where we created a payment intent using Stripe. We then passed this information to the 'homepay.html' template, where it is stored in the 'data-secret' attribute. 
// Now, we can easily access this 'client_secret' using JavaScript in this index.js file.



// Set up Stripe.js and Elements to use in checkout form:
var elements = stripe.elements(); // now we have access to the Stripe elements , so we can go ahead and add in some style.
var style = {
base: {
  color: "#000",
//   lineHeight: '2.4',
  fontSize: '16px'
}
}

//creating payment elements and displaying errors if any exist:
var card = elements.create("card", { style: style }); //for typing in the card number.
card.mount("#card-element"); // that creats the payment elements.


card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});
//Now what we want to perform is the action so when we press ‘pay’ button in the payment page (homepay.html), we’re going to then send the payment to Stripe.
var form = document.getElementById('payment-form'); // collecting all the information in the form.
//we're going to build up an event listener for the form we built in 'homepay.html'. so when the user presses 'pay' button with id="submit" we're gonna detect that, and then we can perform an action (doing a Stripe confirm payment). 
form.addEventListener('submit', function(ev) {
ev.preventDefault();
//collecting some data from the form:
var custName = document.getElementById("custName").value;
var custAdd = document.getElementById("custAdd").value;
var custAdd2 = document.getElementById("custAdd2").value;
var postCode = document.getElementById("postCode").value;

//   $.ajax({
//     type: "POST",
//     url: 'https://127.0.0.1:8000/orders/add/',
//     data: {
//       order_key: clientsecret,
//       csrfmiddlewaretoken: CSRF_TOKEN,
//       action: "post",
//     },
//     success: function (json) {
//       console.log(json.success)

stripe.confirmCardPayment(clientsecret, {
//sending the payment:this is what we're gonna be sending across in addition to the card details to Stripe:
payment_method: {
    card: card,
    billing_details: {
    address:{
        line1:custAdd,
        line2:custAdd2
    },
    name: custName
    },
}
}).then(function(result) {
//performing some error checking (because we want to know whether the payment was successful or not):
if (result.error) {
    console.log('payment error')
    console.log(result.error.message);
} else {
    if (result.paymentIntent.status === 'succeeded') { //This means that the payment has taken place.
    console.log('payment processed')
    // There's a risk of the customer closing the window before callback
    // execution. Set up a webhook or plugin to listen for the
    // payment_intent.succeeded event that handles any business critical
    // post-payment actions.
    window.location.replace("http://127.0.0.1:8000/payment/orderplaced/"); //forwarding the user to this page when the result is succeeded.
    }
}
});

// },
//     error: function (xhr, errmsg, err) {},
//   });



}
)