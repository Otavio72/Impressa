        const swiper = new Swiper('.mySwiper', {
          loop: true,
          pagination: {
            el: '.swiper-pagination',
            clickable: true,
          },
          navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
          },
          loop: true,
          slidesPerView: 1,
          spaceBetween: 10,

        });