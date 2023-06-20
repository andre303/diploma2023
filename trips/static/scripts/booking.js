$('.booking-form-wrapper select').select2()
$(document).mouseup(function (e){ // событие клика по веб-документу
    var div1 = $(".booking-form-wrapper"); // тут указываем ID элемента
    if (div1.is(e.target) // если клик был не по нашему блоку
        && div1.has(e.target).length === 0) { // и не по его дочерним элементам
        $('.booking-form-wrapper').fadeToggle(400)
    }
    });