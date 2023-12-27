console.log('working fine');

const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June", "July",
    "Aug", "Sept", "Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()
    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("Comment Saved to DB");
            console.log(response); // Log the entire response to inspect its structure

            if(response.bool == true){
                $("#review-res").html("Review added successfully.")
                $(".hide-comment-form").hide()
                let __html = '<h6>' + response.average_reviews.rating.toFixed(1) + " out of 5" + '</h6>'
                $("#rating").html(__html)

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html += '<div class="user justify-content-between d-flex">'
                _html +='<div class="thumb text-center">'
                _html +='<img src="{% static "/assets/imgs/theme/icons/icon-user.svg" %}" alt="" />'
                _html +='<a href="#" class="font-heading text-brand">' + response.context.user +'</a>'
                _html +='</div>'

                _html +='<div class="desc">'
                _html +='<div class="d-flex justify-content-between mb-10">'
                _html +='<div class="d-flex align-items-center">'
                _html +='<span class="font-xs text-muted"> '+ time +'</span>'
                _html +='</div>'

                for(let i = 1; i<=response.context.rating; i++){
                    _html += '<i class="fas fa-star text-warning"></i>'
                }

                _html +='</div>'
                _html +='<p class="mb-10">' + response.context.review + '</p>'

                _html +='</div>'
                _html +='</div>'
                _html +='</div>'
                $(".comment-list").prepend(_html)
                let ___html = '<div class="progress">'
                let percentage1 = response.ratings_count[1].percentage.toFixed(0)
                ___html += '<span>1 star</span>'
                ___html += `<div class="progress-bar" role="progressbar" style="width: ${percentage1}%" aria-valuenow="${percentage1}" aria-valuemin="0" aria-valuemax="100">${percentage1}%</div>`
                ___html += '</div>'
                let percentage2 = response.ratings_count[2].percentage.toFixed(0)
                ___html += '<div class="progress">'
                ___html += '<span>2 star</span>'
                ___html += `<div class="progress-bar" role="progressbar" style="width: ${percentage2}%" aria-valuenow="${percentage2}" aria-valuemin="0" aria-valuemax="100">${percentage2}%</div>`
                ___html += '</div>'
                let percentage3 = response.ratings_count[3].percentage.toFixed(0)
                ___html += '<div class="progress">'
                ___html += '<span>3 star</span>'
                ___html += `<div class="progress-bar" role="progressbar" style="width: ${percentage3}%" aria-valuenow="${percentage3}" aria-valuemin="0" aria-valuemax="100">${percentage3}%</div>`
                ___html += '</div>'
                let percentage4 = response.ratings_count[4].percentage.toFixed(0)
                ___html += '<div class="progress">'
                ___html += '<span>4 star</span>'
                ___html += `<div class="progress-bar" role="progressbar" style="width: ${percentage4}%" aria-valuenow="${percentage4}" aria-valuemin="0" aria-valuemax="100">${percentage4}%</div>`
                ___html += '</div>'
                let percentage5 = response.ratings_count[5].percentage.toFixed(0)
                ___html += '<div class="progress">'
                ___html += '<span>5 star</span>'
                ___html += `<div class="progress-bar" role="progressbar" style="width: ${percentage5}%" aria-valuenow="${percentage5}" aria-valuemin="0" aria-valuemax="100">${percentage5}%</div>`
                ___html += '</div>'
                $(".rating-bar").html(___html)
                let ____html = '<a class="nav-link" id="Reviews-tab" data-bs-toggle="tab" href="#Reviews">Reviews ('+ response.reviews +')</a>'
                $("#Reviews-holder").html(____html)
                let _____html = '<div class="product-rate d-inline-block">'
                _____html +='<div class="product-rating" style="width: '+ response.average_rating_percentage +'%"></div>'
                _____html +='</div>'
                _____html +='<span class="font-small ml-5 text-muted"> ('+ response.reviews +' reviews)</span>'
                $(".rating-big").html(_____html)
            }

        }
    })
})

$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click",function(){
        console.log("the checkbox has been click");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") //vendor, category

            // console.log("Filter value is: ",filter_value);
            // console.log("Filter key is: ",filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter object", filter_object);
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data...");
            },
            success: function(response){
                console.log(response);
                console.log("Sent data");
                $("#filtered-product").html(response.data)
            }
        })
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("Current price is:", current_price);
        // console.log("Max price is:", max_price);
        // console.log("Min price is:", min_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            // console.log("Price error occur");

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            // console.log("##########################"),
            // console.log("##########################"),
            // console.log("##########################"),
            // console.log("Max Price is:", max_price),
            // console.log("Min Price is:", min_price)

            alert("Price must be between $" + min_price + " and $" + max_price)
            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()

            return false
        }
    })

    $(".add-to-cart-btn").on("click", function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()
    
        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Id:", product_id);
        console.log("PId:", product_pid);
        console.log("Image:", product_image);
        console.log("Price:", product_price);
        console.log("Index:", index);
    
        console.log("Current element:", this_val);
    
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to cart");
            },
            success: function(response){
                this_val.html("✅")
                console.log("Added product to cart");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })
    
    $(".delete-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product ID: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id" : product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                console.log("Product deleted");
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    $(".update-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-" + product_id).val()
    
        console.log("Product ID: ", product_id);
        console.log("Product QTY: ", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id" : product_id,
                "qty" : product_quantity,
            },
            dataType: "json",
            // beforeSend: function(){
            //     this_val.hide()
            // },
            success: function(response){
                this_val.show()
                console.log("Product refresh");
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    //Making Default Address
    $(document).on('click',".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID is ", id);
        console.log("Element is: ", this_val);

        $.ajax({
            url: "/make-default-address",
            data: {
                "id": id
            },
            dataType: "json",
            success: function(response){
                console.log("Address made default...");
                if(response.boolean == true){
                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check" + id).show()
                    $(".button"+id).hide()
                }
            }
        })
    })

    // Adding to wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product ID is ", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding to wishlist")
            },
            success: function(response){
                this_val.html("✅");
                if (response.bool === true){
                    console.log("Added to wishlist");
                }
            }
        })
    })

    // //Remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id is ", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function(response){
                console.log("Delete product from wishlist")
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
                console.log("Deleted product from wishlist")
            }
        })
    })

    $(document).on("submit","#contact-form-ajax", function(e){
        e.preventDefault()
        console.log("Submited...");
        let full_name=$("#full_name").val()
        let email=$("#email").val()
        let phone=$("#phone").val()
        let subject=$("#subject").val()
        let message=$("#message").val()

        console.log("Name:", full_name);
        console.log("Email:", email);
        console.log("Phone:", phone);
        console.log("Subject:", subject);
        console.log("Message:", message);

        $.ajax({
            url:"/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            },
            dataType: "json",
            beforeSend: function(response){
                console.log("Sending Data to server...")
            },
            success: function(response){
                console.log("Sent Data to server!")
                $(".contact-us").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message Sent Successfully.")
            }
        })
    })
    //Homepage product update 
    $(".filter-choice").on("click",function(){
        console.log("the checkbox has been click");

        let filter_category = $(this).val()

        console.log("Category is:", filter_category);

        $.ajax({
            url: '/filter-product-homepage',
            data: {"categories":filter_category},
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data...");
            },
            success: function(response){
                console.log(response);
                console.log("Sent data");
                $("#filtered1-product").html(response.data)
            }
        })
    })
    $(".search-category").on("click",function(){
        console.log("the checkbox has been click1");
        // let current_price = $(this).val()
        let category_value = $("#category_value").val()
        console.log(category_value);
        $.ajax({
            url: '/filter-category',
            data: {"cat":category_value},
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data...");
            },
            success: function(response){
                console.log(response);
                console.log("Sent data");
                $(".filtered-category").html(response.data)
            }
        })
    })
    $(".search-item").on("click",function(){
        console.log("the checkbox has been click2");
        // let current_price = $(this).val()
        let item_value = $("#item_value").val()
        console.log(item_value);
        $.ajax({
            url: '/filter-item',
            data: {"item":item_value},
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data...");
            },
            success: function(response){
                console.log(response);
                console.log("Sent data");
                $(".filtered-item").html(response.data)
            }
        })
    })
    $(".search-vendor").on("click",function(){
        console.log("the checkbox has been click2");
        // let current_price = $(this).val()
        let vendor_value = $("#vendor_value").val()
        console.log(vendor_value);
        $.ajax({
            url: '/filter-vendor',
            data: {"vendor":vendor_value},
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data...");
            },
            success: function(response){
                console.log(response);
                console.log("Sent data");
                $(".filtered-vendor").html(response.data)
            }
        })
    })
})


// productid = request.GET['id']
//     wishlist = wishlist_model.objects.filter(user=request.user)

//     product = wishlist_model.objects.get(id=productid)
//     delete_product = product.delete()
// // Add to cart functionality
// $("#add-to-cart-btn").on("click", function(){
    
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)

//     console.log("Quantity:", quantity);
//     console.log("Title:", product_title);
//     console.log("Id:", product_id);
//     console.log("Price:", product_price);
//     console.log("Current element:", this_val);

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("Adding product to cart");
//         },
//         success: function(response){
//             this_val.html("Item added to cart")
//             console.log("Added product to cart");
//             $(".cart-items-count").text(response.totalcartitems)
//         }
//     })
// })