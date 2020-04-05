$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-kyc').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    $('#btn-kyc').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Get kyc details
        $.ajax({
            type: 'POST',
            url: '/auto_kyc',
            data: form_data,
            contentType: false,
            dataType: 'json',
            cache: false,
            processData: false,
            async: true,
            success: function (response) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + JSON.stringify(response, null, 2));
            },
        });
    });

});
