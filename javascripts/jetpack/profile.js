$( document ).ready(function() {
    // Handler for .ready() called.
    console.debug($("#profile_banner"));
    var cropperHeader = new Croppic('profile_banner');
    console.debug(cropperHeader);
});
