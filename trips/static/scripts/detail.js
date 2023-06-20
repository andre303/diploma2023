function prevPage(page, trip_pk, numPages) {
  page = parseInt(page) - 1;
  numPages = parseInt(numPages)
  changePage(page, trip_pk, numPages)
}

function nextPage(page, trip_pk, numPages) {
  page = parseInt(page) + 1;
  numPages = parseInt(numPages)
  changePage(page, trip_pk, numPages)
}

function changePage(page, trip_pk, numPages) {
  $.ajax({
    url: "/trip/" + trip_pk + "/",
    type: "GET",
    dataType: 'json',
    data: {
      "page": page,
    },
    success: function (data) {
      cards = $(".review-cards").empty()
      for (item in data) {
        card = $('<div class="card"></div>');
        // $(card).append('<h1>HI</h1>')
        stars = '';
        for (let i = 0; i < data[item]['rate']; i++) {
          stars += '<i class="fa fa-star" aria-hidden="true"></i>';
        }
        card_body = $('<div class="card-body"></div>');
        card_title = $('<h5 class="card-title"></h5>');
        $(card_title).html(stars + "<br />" + data[item]['name'] + "<br />" + '<small style="color:grey">' + data[item]['date'] + "</small>");
        $(card_body).append(card_title);
        $(card_body).append(data[item]['text']);
        $(card).append(card_body);
        $(cards).append($(card))
      }
      prevBtn = $('#prevPage');
      nextBtn = $('#nextPage');
      if (page == 2) {
        $(prevBtn).prop('disabled', false)
        if (numPages == 2) {
          $(nextBtn).prop('disabled', true)
        }
      } else if (page == 1) {
        $(prevBtn).prop('disabled', true)
        if (numPages == 2) {
          $(nextBtn).prop('disabled', false)
        }
      } else if (page == numPages) {
        $(nextBtn).prop('disabled', true)
      } else if ($(nextBtn).prop('disabled') == true) {
        $(nextBtn).prop('disabled', false)
      }
      $(prevBtn).attr('onclick', "prevPage('" + page + "','" + trip_pk + "','" + numPages + "')")
      $(nextBtn).attr('onclick', "nextPage('" + page + "','" + trip_pk + "','" + numPages + "')")
    },
    error: function (data) {
      console.log(data);
    }
  });
}

var stars = document.querySelectorAll('#review_form i.fa-star')
            var stars_field = document.querySelector('#rating_field')
            stars.forEach(function (item, index) {
              item.addEventListener('click', function () {
                stars_field.value = (index + 1)
                new_stars = document.querySelectorAll('#review_form i.fa-star');
                for (var i = 0; i <= 5; i++) {
                  $(new_stars [i]).addClass('faa')
                  $(new_stars [i]).removeClass('fas')
                }
                for (var i = 0; i <= index; i++) {
                  $(new_stars [i]).removeClass('faa')
                  $(new_stars [i]).addClass('fas')
                }
              })
            })