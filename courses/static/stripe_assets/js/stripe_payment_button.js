// 1

var paymentRequest = stripe.paymentRequest ({
    country: 'US' ,
    currency: 'usd' ,
    total: {
        label: 'Demo total' ,
        amount: 1099 ,
    } ,
    requestPayerName: true ,
    requestPayerEmail: true ,
});


// 2

var elements = stripe.elements ();
var prButton = elements.create ('paymentRequestButton' , {
    paymentRequest: paymentRequest ,
});

// Check the availability of the Payment Request API first.
paymentRequest.canMakePayment ().then (function (result) {
    if (result) {
        prButton.mount ('#payment-request-button');
    } else {
        document.getElementById ('payment-request-button').style.display = 'none';
    }
});

// 3
paymentRequest.on ('paymentmethod' , function (ev) {
    // Confirm the PaymentIntent without handling potential next actions (yet).
    stripe.confirmCardPayment (
        clientSecret ,
        {payment_method: ev.paymentMethod.id} ,
        {handleActions: false}
    ).then (function (confirmResult) {
        if (confirmResult.error) {
            // Report to the browser that the payment failed, prompting it to
            // re-show the payment interface, or show an error message and close
            // the payment interface.
            ev.complete ('fail');
        } else {
            // Report to the browser that the confirmation was successful, prompting
            // it to close the browser payment method collection interface.
            ev.complete ('success');
            // Check if the PaymentIntent requires any actions and if so let Stripe.js
            // handle the flow. If using an API version older than "2019-02-11" instead
            // instead check for: `paymentIntent.status === "requires_source_action"`.
            if (confirmResult.paymentIntent.status === "requires_action") {
                // Let Stripe.js handle the rest of the payment flow.
                stripe.confirmCardPayment (clientSecret).then (function (result) {
                    if (result.error) {
                        // The payment failed -- ask your customer for a new payment method.
                    } else {
                        // The payment has succeeded.
                    }
                });
            } else {
                // The payment has succeeded.
            }
        }
    });
});


//   5

var paymentRequest = stripe.paymentRequest ({
    country: 'US' ,
    currency: 'usd' ,
    total: {
        label: 'Demo total' ,
        amount: 1099 ,
    } ,

    requestShipping: true ,
    // `shippingOptions` is optional at this point:
    shippingOptions: [
        // The first shipping option in this list appears as the default
        // option in the browser payment interface.
        {
            id: 'free-shipping' ,
            label: 'Free shipping' ,
            detail: 'Arrives in 5 to 7 days' ,
            amount: 0 ,
        } ,
    ] ,
});


// 6
paymentRequest.on ('shippingaddresschange' , function (ev) {
    if (ev.shippingAddress.country !== 'US') {
        ev.updateWith ({status: 'invalid_shipping_address'});
    } else {
        // Perform server-side request to fetch shipping options
        fetch ('/calculateShipping' , {
            data: JSON.stringify ({
                shippingAddress: ev.shippingAddress
            })
        }).then (function (response) {
            return response.json ();
        }).then (function (result) {
            ev.updateWith ({
                status: 'success' ,
                shippingOptions: result.supportedShippingOptions ,
            });
        });
    }
});

elements.create ('paymentRequestButton' , {
    paymentRequest: paymentRequest ,
    style: {
        paymentRequestButton: {
            type: 'default' ,
            // One of 'default', 'book', 'buy', or 'donate'
            // Defaults to 'default'

            theme: 'dark' ,
            // One of 'dark', 'light', or 'light-outline'
            // Defaults to 'dark'

            height: '64px'
            // Defaults to '40px'. The width is always '100%'.
        } ,
    } ,
});