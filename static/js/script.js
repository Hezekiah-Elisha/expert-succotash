$(document).ready(function(){ 
    $(window).scroll(function(){
      if ($(window).width() < 960) {
        let scrollBottom = $(window).scrollTop();
        if (scrollBottom > 30){
          $("#brandc").animate({
            left: '10%',
          }, 800);
        }
      } else {
  
      }
    });
  
    $('.myc').slick({
      slidesToShow: 2,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 2000,
    });
  
  });