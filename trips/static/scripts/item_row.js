function expandthis(elem) {
    var list_item = $(elem).closest('.list-item');
    if ($(elem).css("-webkit-line-clamp") == 1) {
      $(elem).css("-webkit-line-clamp", "unset")
      $(list_item).css("max-height", "100vh")
    } else {
      $(elem).css("-webkit-line-clamp", "1")
      $(list_item).css("max-height", "42vh")
    }
  }

  function text_expand(elem) {
    var list_item = $(elem).closest('.list-item');
    let text = $(list_item).find('.main-text')
    if ($(text).css("-webkit-line-clamp") == 3) {
      $(text).css("-webkit-line-clamp", "unset")
      $(list_item).css("max-height", "100vh")
      $(elem).text("Згорнути")
    } else {
      $(text).css("-webkit-line-clamp", "3")
      $(elem).text("Детальніше")
    }
  }
//   
// 
