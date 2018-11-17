function js_save_product(csrf_token, product_id, user_id){
    $.ajax({
        url: "save_product/",
        type: "POST",
        data: { 
            csrfmiddlewaretoken: csrf_token,
            product_id: product_id,
            user_id: user_id
        },

        success: function(json){
            $('#fav-product-' + product_id + '-form').remove();
            $('#fa-' + product_id).remove();

            $('#fav-product-' + product_id).append('<i class="fas fa-check-square fa-green"></i>');
            $('#fav-product-' + product_id).append('<span class="saved-product">Produit sauvegardé</span>');
            console.log('success');
        },

        error: function(xhr, errmsg, err){
            $('.fav-product-error').append(response);
            console.log();
        }
    });
}