$(document).ready(function() {
    $('.rich-editor').summernote({
        height: 300,
        toolbar: [
            // [groupName, [list of button]]
            ['style', ['style', 'bold', 'italic', 'underline', 'strikethrough', 'clear']],
            // ['font', ['strikethrough']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
        ]
    })
});