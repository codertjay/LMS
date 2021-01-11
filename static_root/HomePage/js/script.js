$(document).ready(function() {
    $('.card-wrapper .card_header a').click(function() {
        $(this).parents(".card-wrapper").addClass('active').siblings().removeClass('active');
    });
    $('.card-collapse .card_header1 a').click(function() {
        $(this).parents(".card-collapse").addClass('active').siblings().removeClass('active');
    });
    



    $('.blog-slider').owlCarousel({
        loop: true,
        margin: 10,
        responsiveClass: true,
        dots: false,
        addClassActive: true,
        navText: ["<i class='far fa-chevron-left'></i>", "<i class='far fa-chevron-right'></i>"],
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            768: {
                items: 2,
                nav: true
            },
            1000: {
                items: 2,
                nav: true,
                loop: false,
                margin: 60
            }
        }
    })

})



$(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
        $('.meet-innovative').addClass('animate');
    } else {
        $('.meet-innovative').addClass('animate');
    }
});

$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('header').addClass("sticky");
    } else {
        $('header').removeClass("sticky");
    }
});
new WOW().init();




(function () {
  "use strict";

  var carousels = function () {
    $(".owl-carousel1").owlCarousel({
      loop: true,
      center: true,
      margin: 0,
      responsiveClass: true,
      nav: false,
      responsive: {
        0: {
          items: 1,
          nav: false
        },
        680: {
          items: 2,
          nav: false,
          loop: false
        },
        1000: {
          items: 3,
          nav: true
        }
      }
    });
  };

  (function ($) {
    carousels();
  })(jQuery);
})();