function js_save_product(csrf_token, product_id, user_id){
    $.ajax({
        url: "save_product/", // Django route
        type: "POST",
        data: { 
            csrfmiddlewaretoken: csrf_token,
            product_id: product_id,
            user_id: user_id
        },

        success: function(json){
            $('#fav-product-' + product_id + '-form').remove();
            $('#fa-' + product_id).remove();

            if(typeof json.success_message !== 'undefined'){
                $('#fav-product-' + product_id).append('<i class="fas fa-check-square fa-green"></i>');
                $('#fav-product-' + product_id).append('<span class="saved-product">' + json.success_message + '</span>');
            }
            else{
                $('#fav-product-' + product_id).append('<i class="fas fa-times-circle fa-red"></i>');
                $('#fav-product-' + product_id).append('<span class="not-saved-product">' + json.error_message + '</span>');
            }
        },

        error: function(json){
            $('#fav-product-' + product_id + '-form').remove();
            $('#fa-' + product_id).remove();

            $('#fav-product-' + product_id).append('<i class="fas fa-times-circle fa-red"></i>');
            $('#fav-product-' + product_id).append('<span class="not-saved-product">' + json.error_message + '</span>');
        }
    });
}