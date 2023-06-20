
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    function youtube_parser(url) {
        url = url.split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
        return (url[2] !== undefined) ? url[2].split(/[^0-9a-z_\-]/i)[0] : url[0];
    }
    document.getElementById("id_youtube_video_url").addEventListener('change', function () {
        $(".profile-video iframe").remove();
        $('<iframe width="480" height="320" frameborder="0" allowfullscreen></iframe>')
            .attr("src", "http://www.youtube.com/embed/" + youtube_parser($('#id_youtube_video_url')
                .val()))
            .appendTo(".profile-video");
    })
    $('select').select2()



    const imageForm = document.getElementById('avatar_changing_form')
    const confirmBtn = document.getElementById('crop')
    const input = document.getElementById('upload_image')
    const csrf = document.getElementsByName('csrfmiddlewaretoken')


    var $modal = $('#modal');

    var image = document.getElementById('sample_image');

    var cropper;

    $('#upload_image').change(function (event) {
        var files = event.target.files;

        var done = function (url) {
            image.src = url;
            $modal.modal('show');
        };

        if (files && files.length > 0) {
            reader = new FileReader();
            reader.onload = function (event) {
                done(reader.result);
            };
            reader.readAsDataURL(files[0]);
        }
    });

    $modal.on('shown.bs.modal', function () {
        cropper = new Cropper(image, {
            aspectRatio: 1,
            viewMode: 3,
            preview: '.preview'
        });
    }).on('hidden.bs.modal', function () {
        cropper.destroy();
        cropper = null;
    });

    $('#crop').click(function () {
        $modal.modal('hide')
        $('.load-wrapper').toggle();
        cropper.getCroppedCanvas().toBlob((blob) => {
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('file', blob, 'avatar.png');      
            $.ajax({
                type: 'POST',
                url: imageForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                async:false,
                success: function (response) {
                    // document.location.reload();
                    console.log(response);
                    $('#uploaded_image').attr('src',response['success'])
                    $('.load-wrapper').toggle();
                },
                error: function (error) {
                    alert(error)
                    document.location.reload();
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        });
    });
