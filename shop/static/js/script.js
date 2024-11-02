var time = 7; // time in seconds

var $progressBar,
    $bar,
    $elem,
    isPause,
    tick,
    percentTime;


//Init progressBar where elem is $("#owl-demo")
function progressBar(elem) {
    $elem = elem;
    //build progress bar elements
    buildProgressBar();
    //start counting
    start();
}

//create div#progressBar and div#bar then prepend to $("#owl-demo")
function buildProgressBar() {
    $progressBar = $("<div>", {
        id: "progressBar"
    });
    $bar = $("<div>", {
        id: "bar"
    });
    $progressBar.append($bar).prependTo($elem);
}

function start() {
    //reset timer
    percentTime = 0;
    isPause = false;
    //run interval every 0.01 second
    tick = setInterval(interval, 10);
};
var currentItemIndex;

function showCaption() {

    var currentSlide = $elem.find('.owl-item').eq(currentItemIndex);
    currentSlide.find('.caption').addClass('show');
}

function removeCaption() {

    var currentSlide = $elem.find('.owl-item').eq(currentItemIndex);
    currentSlide.find('.caption').removeClass('show');
}

function interval() {
    if (isPause === false) {
        percentTime += 1 / time;
        $bar.css({
            width: percentTime + "%"
        });
        //if percentTime is equal or greater than 100
        if (percentTime >= 100) {
            //slide to next item 
            $elem.trigger('owl.next');

        }
    }
}

//pause while dragging 
function pauseOnDragging() {
    isPause = true;
}

//moved callback
function moved() {
    currentItemIndex = this.owl.currentItem;
    //clear interval
    clearTimeout(tick);
    //start again
    start();
    showCaption();
}







(function($) {
    "use strict";


    $(window).bind("load", function() {
        $('#status').fadeOut(); // will first fade out the loading animation
        $('#preloader').delay(1000).fadeOut('slow'); // will fade out the white DIV that covers the website.
        //$('body').delay(1000).css({'overflow-x': 'hidden'}).css({'overflow-y': 'auto'});
        //checkContactForm();




    });


    $(window).ready(function() {

        var wow = new WOW({
            boxClass: 'wow', // animated element css class (default is wow)
            animateClass: 'animated', // animation css class (default is animated)
            offset: '-200px', // distance to the element when triggering the animation (default is 0)
            mobile: true, // trigger animations on mobile devices (default is true)
            live: true // act on asynchronously loaded content (default is true)
        });

        new WOW().init();

        //    Homepage2 slider trigger
        if ($('.homeslider').length > 0) {



            //Init the carousel
            $(".homeslider .owl-carousel").owlCarousel({
                slideSpeed: 500,
                paginationSpeed: 500,
                singleItem: true,
                afterInit: progressBar,
                afterMove: moved,
                beforeMove: removeCaption,
                startDragging: pauseOnDragging
            });


        }
        if ($('.bg-image[data-bg-image]').length > 0) {
            $('.bg-image[data-bg-image]').each(function() {
                var el = $(this);
                var sz = getImgSize(el, el.attr("data-bg-image"));
                el.css('background-position', 'center').css('background-image', "url('" + el.attr("data-bg-image") + "')").css('background-size', 'cover').css('background-repeat', 'no-repeat');
            });
        }

        if ($('.bg-color[data-bg-color]').length > 0) {
            $('.bg-color[data-bg-color]').each(function() {
                var el = $(this);
                el.css('background-color', el.attr("data-bg-color"));
            });
        }

        //products carousel
        $(".product-carousel").owlCarousel({
            pagination: true,
            items: 4, //10 items above 1000px browser width
            itemsDesktop: [1200, 3], //5 items between 1000px and 901px
            itemsDesktopSmall: [990, 2], // betweem 900px and 601px
            itemsTablet: [570, 1], //2 items between 600 and 0

            itemsMobile: false // itemsMobile disabled - inherit from itemsTablet option
        });
        var owl = $(".product-carousel").data('owlCarousel');

        $(".product-carousel").parent().find('.nav-buttons .btn-prev').click(function(e) {
            e.preventDefault();
            owl.prev();
        });

        $(".product-carousel").parent().find('.nav-buttons .btn-next').click(function(e) {
            e.preventDefault();
            owl.next();
        });


        //  Banner slider carousel  
        $(".banner-carousel").owlCarousel({
            afterInit: function(el) {


                // console.log(el.find('.banner-carousel'));
                el.parent().find(".btn-next,.btn-prev").prependTo(el);
            },
            pagination: false,
            navigation: false, // Show next and prev buttons
            slideSpeed: 300,
            paginationSpeed: 400,
            singleItem: true


        });

        var bannerowl = $(".banner-carousel").data('owlCarousel');
        $(".banner-carousel").find('.btn-prev').click(function(e) {
            e.preventDefault();
            bannerowl.prev();
        });

        $(".banner-carousel").find('.btn-next').click(function(e) {
            e.preventDefault();
            bannerowl.next();
        });


        //Defauld carousel
        $(".default-carousel").each(function() {

            $(this).owlCarousel({
                afterInit: function(el) {



                    el.parent().find(".btn-next,.btn-prev").prependTo(el);
                },
                pagination: false,
                navigation: false, // Show next and prev buttons
                slideSpeed: 300,
                paginationSpeed: 400


            });
            var defowl = $(this).data('owlCarousel');


            $(this).find('.btn-prev').click(function(e) {
                e.preventDefault();
                defowl.prev();
            });

            $(this).find('.btn-next').click(function(e) {
                e.preventDefault();
                defowl.next();
            });
        });



        if ($('.triangled').length > 0) {
            $('.triangled li').append('<div class="triangle"></div>');
        }

        //    top cart
        $('.basket .close-btn').click(function() {
            $(this).parent().parent().fadeOut(function() {
                $(this).remove();
                checkBasketDropdown(true);
            });
        });
        $('[data-hover="dropdown"]').dropdownHover();
        checkBasketDropdown();

        function checkBasketDropdown(remove) {
            if (remove) {
                cn = parseInt($('.basket-item-count').text());
                nn = cn - 1;
                $('.basket-item-count').text(nn);
            }
            if ($('.basket .basket-item').length <= 0) {
                $('.basket .dropdown-menu').prepend("<li class='empty'>Empty</li>");
            }
        }
        //Quantity element
        $('.le-quantity a').click(function(e) {

            e.preventDefault();
            var currentQty = $(this).parent().parent().find('input').val();

            if ($(this).hasClass('minus') && currentQty > 0) {
                $(this).parent().parent().find('input').val(parseInt(currentQty) - 1);
            } else {

                if ($(this).hasClass('plus')) {

                    $(this).parent().parent().find('input').val(parseInt(currentQty) + 1);
                }
            }

        });


        //Rating Star activator
        if ($('.star').length > 0) {
            $('.star').raty({
                space: false,
                starOff: 'images/star-off.png',
                starOn: 'images/star-on.png',
                score: function() {
                    return $(this).attr('data-score');
                }
            });
        }

        function getImgSize(el, imgSrc) {
            var newImg = new Image();
            newImg.onload = function() {
                var height = newImg.height;
                var width = newImg.width;

                el.css('height', height);

            };
            newImg.src = imgSrc;
        }



        //SinglePage slide activator
        if ($('.single-product-slider').length > 0) {





            var singlePSlider = $(".single-product-slider").owlCarousel({

                pagination: false,
                navigation: false, // hide next and prev buttons
                slideSpeed: 300,
                paginationSpeed: 400,
                singleItem: true

            });

            var gallery = singlePSlider.data('owlCarousel');





            var thumbSlider = $('.single-product-gallery .gallery-thumbs ul').owlCarousel({
                items: 5, //10 items above 1000px browser width
                itemsDesktop: [1000, 4], //5 items between 1000px and 901px
                itemsDesktopSmall: [900, 3], // betweem 900px and 601px
                itemsTablet: [400, 2], //2 items between 600 and 0

                itemsMobile: false // itemsMobile disabled - inherit from itemsTablet option
            });

            var thumbCtrls = thumbSlider.data('owlCarousel');



            $(".single-product-gallery .gallery-thumbs .horizontal-thumb").click(function(event) {
                event.preventDefault();
                $(this).parent().parent().parent().find('.active').removeClass('active');

                $(this).parent().addClass('active');

                var tid = $(this).attr('href');
                var targetSlide = $(".single-product-gallery-item" + tid);

                var targetSlide = $(targetSlide).parent().index();

                gallery.goTo(targetSlide);


            });



            if ($('.single-product-vertical-gallery').length > 0) {
                $('.single-product-vertical-gallery ul').carouFredSel({
                    direction: 'up',
                    auto: false,
                    items: 4,
                    circular: true
                });

                $(".single-product-vertical-gallery .up-btn").click(function(event) {
                    event.preventDefault();
                    $('.single-product-vertical-gallery ul').trigger("next", 1);

                });


                $(".single-product-vertical-gallery .down-btn").click(function(event) {
                    event.preventDefault();
                    $('.single-product-vertical-gallery ul').trigger("prev", 1);

                });


                $(".single-product-vertical-gallery .vertical-gallery-item").click(function(event) {
                    event.preventDefault();
                    tid = $(this).attr('href');
                    targetSlide = $(".single-product-gallery-item" + tid);

                    singlePSlider.trigger('slideTo', targetSlide);

                });

            }





            //        Horizontal Single page gallery

            if ($('.single-product-horizontal-gallery').length > 0) {
                $('.single-product-horizontal-gallery ul').carouFredSel({
                    auto: false,
                    circular: true
                });

                $(".single-product-horizontal-gallery .next-btn").click(function(event) {
                    event.preventDefault();
                    $('.single-product-horizontal-gallery ul').trigger("next", 1);

                });


                $(".single-product-horizontal-gallery .prev-btn").click(function(event) {
                    event.preventDefault();
                    $('.single-product-horizontal-gallery ul').trigger("prev", 1);

                });


                $(".single-product-horizontal-gallery .horizontal-gallery-item").click(function(event) {
                    event.preventDefault();
                    tid = $(this).attr('href');
                    targetSlide = $(".single-product-gallery-item" + tid);
                    console.log(targetSlide)
                    singlePSlider.trigger('slideTo', targetSlide);

                });

            }
        }


        //Brand Slider activator

        if ($(".brands-slider").length > 0) {
            $(".brands-slider img").lazyload({
                event: "loadImagesNow",
                effect: "fadeIn"
            });
        }

        //    Lightbox activator

        if ($('a[data-rel="prettyphoto"]').length > 0) {
            $('a[data-rel="prettyphoto"]').prettyPhoto();
        }


        //Image lazy activator
        if ($("img.lazy").length > 0) {
            var allImgs = $("img.lazy").length;
            $("img.lazy").each(function(i) {

                var src = $(this).attr('src');
                $(this).attr('data-original', src);
                if (i + 1 >= allImgs) {

                    $("img.lazy").lazyload({
                        effect: "fadeIn"
                    });

                }


            });



        }



        /*
         * Replace all SVG images with inline SVG
         */
        $('img.svg').each(function() {
            var $img = jQuery(this);
            var imgID = $img.attr('id');
            var imgClass = $img.attr('class');
            var imgURL = $img.attr('src');

            jQuery.get(imgURL, function(data) {
                // Get the SVG tag, ignore the rest
                var $svg = jQuery(data).find('svg');

                // Add replaced image's ID to the new SVG
                if (typeof imgID !== 'undefined') {
                    $svg = $svg.attr('id', imgID);
                }
                // Add replaced image's classes to the new SVG
                if (typeof imgClass !== 'undefined') {
                    $svg = $svg.attr('class', imgClass + ' replaced-svg');
                }

                // Remove any invalid XML tags as per http://validator.w3.org
                $svg = $svg.removeAttr('xmlns:a');

                // Replace image with new SVG
                $img.replaceWith($svg);

            }, 'xml');
        });

        if ($('.search-button').length > 0) {
            $('.search-button').click(function(e) {
                e.preventDefault();
                var fld = $(this).find('+ .field');
                fld.addClass('open');

            });

            $('html').click(function() {
                $('.search-holder .field').removeClass('open');
            });

            $('.search-holder').click(function(event) {
                event.stopPropagation();
            });
        }

        $('[data-placeholder]').focus(function() {
            var input = $(this);
            if (input.val() == input.attr('data-placeholder')) {
                input.val('');
            }
        }).blur(function() {
            var input = $(this);
            if (input.val() == '' || input.val() == input.attr('data-placeholder')) {
                input.addClass('placeholder');
                input.val(input.attr('data-placeholder'));
            }
        }).blur();

        $('[data-placeholder]').parents('form').submit(function() {
            $(this).find('[data-placeholder]').each(function() {
                var input = $(this);
                if (input.val() == input.attr('data-placeholder')) {
                    input.val('');
                }
            });
        });



    });




    $('.goto-top').click(function(e) {
        e.preventDefault();
        $('html,body').animate({
            scrollTop: 0
        }, 2000);
    });

    if ($('a[data-rel="prettyphoto"]').length > 0) {
        $('a[data-rel="prettyphoto"]').prettyPhoto();
    }
    if ($('a[data-rel="prettyPhoto"]').length > 0) {
        $('a[data-rel="prettyPhoto"]').prettyPhoto();
    }


    //Contact form setup
    function checkContactForm() {
        if ($(".contact-form").length > 0) {
            var formStatus = $(".contact-form").validate();
            //   ===================================================== 
            //sending contact form
            $(".contact-form").submit(function(e) {
                e.preventDefault();

                //  triggers contact form validation
                if (formStatus.errorList.length === 0) {
                    $(".contact-form .submit").fadeOut(function() {
                        $('#loading').css('visibility', 'visible');
                        $.post('submit.php', $(".contact-form").serialize(),
                            function(data) {
                                $(".contact-form input,.contact-form textarea").not('.submit').val('');
                                $('.message-box').html(data);
                                $('#loading').css('visibility', 'hidden');
                                $(".contact-form").css('display', 'none');
                                //$(".contact-form .submit").removeClass('disabled').css('display', 'block');
                            }
                        );
                    });
                }
            });
        }
    }


    //Custom select buttons trigger
    if ($('.selectpicker').length > 0) {

        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
            $('.selectpicker').selectpicker('mobile');
        } else {
            $('.selectpicker').selectpicker();
        }

    }



    //Sidebar Price Slider
    if ($('.price-slider').length > 0) {
        $('.price-slider').slider({
            min: 100,
            max: 700,
            step: 10,
            value: [100, 400],
            handle: "square"

        });
    }


    $('select.nav').change(function() {
        var loc = ($(this).find('option:selected').val());
        scrollToSection(loc);
    });

    function scrollToSection(destSection) {
        location.href = destSection;
        //    $('html, body').stop().animate({
        //      scrollTop: $(destSection).offset().top + scrollOffset
        //    }, 2000, 'easeInOutExpo');
    }

    //  $('.nav-menu a').bind('click', function (event) {
    //    event.preventDefault();
    //    var clickedMenu = $(this);
    //    $('.nav-menu .active').toggleClass('active');
    //    clickedMenu.parent().toggleClass('active');
    //    scrollToSection(clickedMenu.attr('href'));
    //  });

})(jQuery);



// Sticky Nav
$(window).scroll(function(e) {
    var nav_anchor = $(".top-menu-holder");
    var gotop = $(document);
    if ($(this).scrollTop() >= 500) {
        $('.goto-top').css({
            'opacity': 1
        });
    } else if ($(this).scrollTop() < 500) {
        $('.goto-top').css({
            'opacity': 0
        });
    }
    if ($(this).scrollTop() >= $('header').height()) {
        nav_anchor.addClass('split');
    } else if ($(this).scrollTop() < $('header').height()) {
        nav_anchor.removeClass('split');
    }
});




/**
 Provides requestAnimationFrame in a cross browser way.
 @author paulirish / http://paulirish.com/ */
if (!window.requestAnimationFrame) {
    window.requestAnimationFrame = (function() {
        return window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame ||
            window.oRequestAnimationFrame ||
            window.msRequestAnimationFrame ||
            function( /* function FrameRequestCallback / callback, / DOMElement Element */ element) {};
    })();

}