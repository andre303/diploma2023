var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  function youtube_parser(url) {
    url = url.split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
    return (url[2] !== undefined) ? url[2].split(/[^0-9a-z_\-]/i)[0] : url[0];
  }
  var first = true;
  var previous_elem = undefined
  function videoOver(element, video_link) {
    if(previous_elem == undefined || previous_elem!=element){
    if (window.innerWidth > 768) {
      previous_elem = element
      var video = $('.video-wrapper')
      if (first || $(video).css("display") == "none") {
        $(video).css('display', 'flex');
        first = false
      }
      var pos = $(element).offset();
      $(video).offset({
        top: pos.top
      })
      
      $(".video-wrapper iframe").remove();
      $('<iframe width="420" height="315" frameborder="0" allowfullscreen></iframe>')
        .attr("src", "https://www.youtube.com/embed/" + youtube_parser(video_link))
        .appendTo(".video-wrapper");
    }
  }
  }

