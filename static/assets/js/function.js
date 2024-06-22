

$("#commentForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved to DB...")




            if (res.bool == true) {
                $("#review-res").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                const reviewDate = new Date(res.context.review_date);
                const options = { day: '2-digit', month: 'short', year: 'numeric' };
                const formattedDate = new Intl.DateTimeFormat('en-US', options).format(reviewDate);

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html += '<div class="user justify-content-between d-flex">'
                _html += '<div class="thumb text-center">'
                _html += '<img src="https://thumbs.dreamstime.com/b/default-avatar-profile-vector-user-profile-default-avatar-profile-vector-user-profile-profile-179376714.jpg" alt="" />'
                _html += '<a href="#" class="font-heading text-brand">' + res.context.user + '</a>'
                _html += '</div>'


                _html += '<div class="desc">'
                _html += '<div class="d-flex justify-content-between mb-10">'
                _html += '<div class="d-flex align-items-center">'


                _html += '<span class="font-xs text-muted">' + formattedDate + ' </span>'
                _html += '</div>'
                _html += '<div style="margin-left: 20px !important;">'
                for (var i = 1; i <= res.context.rating; i++) {
                    _html += '<i class="fas fa-star text-warning"></i>';
                }

                _html += '</div>'
                _html += '</div>'
                _html += '<p class="mb-10">' + res.context.review + '</p>'

                _html += '</div>'
                _html += '</div>'
                _html += ' </div>'

                $(".comment-list").prepend(_html)
            }
        }
    })
})




$(document).ready(function () {

    // $(".loader").hide()
    $(".filter-checkbox,#price-filter-btn").on("click", function () {
        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()


        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function (index) {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            // console.log(filter_value, filter_key);
            filter_object[filter_key] =
                Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function
                    (element) {
                    return element.value
                })
        })
        // console.log(filter_object);
        $.ajax({

            url: '/filter-products',
            data: filter_object,
            dataType: 'json',

            beforeSend: function () {
                console.log("Sending Data ..")
            },
            success: function (response) {
                console.log(response)
                console.log("Filtering Data ..")
                $("#filtered-product").html(response.data)
            }
        })

    })

    $("#max_price").on("blur", function () {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("Current Price is:", current_price);
        // console.log("Max Price is:", max_price);
        // console.log("Min Price is:", min_price);

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            // console.log("Price Error Occured");

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100


            // console.log("Max Price is:", min_Price);
            // console.log("Min Price is:", max_Price);

            alert("Price must between $" + min_price + ' and $' + max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()
            return false
        }
    })

    // Add To Cart
    $(document).on("click", '.add-to-cart-btn', function () {


        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let max_weight = parseInt($(".product-quantity-" + index).attr("max"))
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()
        let product_price = parseFloat($(".current-product-price-" + index).text())


        console.log(typeof product_price)
        console.log(product_price)

        if (quantity > max_weight || quantity <= 0) {
            alert("Quantite must between 1Kg and " + max_weight + "Kg")
            $("#product-quantity").val(1)
            $("#product-quantity").focus()
            return false

        } else {
            $.ajax({
                url: '/add-to-cart',
                data: {
                    'id': product_id,
                    'pid': product_pid,
                    'qty': quantity,
                    'title': product_title,
                    'price': product_price,
                    'image': product_image,
                    'max_weight': max_weight,

                },
                dataType: 'json',
                beforeSend: function () {
                    console.log("test1")
                },
                success: function (response) {
                    this_val.html("✓")
                    $(".cart-items-count").text(response.totalcartitems)
                    this_val.attr('disabled', false);
                }
            });
        }


    })


    
    // Delete From Cart
    $(document).on("click", '.delete-product', function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("PRoduct ID:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
                // window.location.reload()
            }
        })

    })


    $(document).on("click", '.update-product', function () {

        let this_val = $(this)
        let product_id = this_val.attr("data-product")
        let product_quantity = $(".product-qty-" + product_id).val()
        let max_weight = parseInt($(".product-qty-" + product_id).attr("max"))
        let product_qty_origin = parseInt($("#input-qty").attr("min"))

        console.log("PRoduct ID:", product_id);
        console.log("PRoduct QTY:", product_quantity);
        console.log("Max wieght:", max_weight);
        if (product_quantity > max_weight || product_quantity <= 0) {
            alert("Quantite must between 1Kg and " + max_weight + "Kg")
            $(".product-qty-" + product_id).val(product_qty_origin)
            $(".product-qty-" + product_id).focus()
            return false

        } else {
            $.ajax({
                url: "/update-cart",
                data: {
                    "id": product_id,
                    "qty": product_quantity,
                },
                dataType: "json",
                beforeSend: function () {
                    this_val.hide()
                },
                success: function (response) {
                    this_val.show()
                    $(".cart-items-count").text(response.totalcartitems)
                    $("#cart-list").html(response.data)
                    window.location.reload()
                }
            })
        }

    })


    // Adding to wishlist
    $(document).on("click", ".add-to-wishlist", function () {
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)


        console.log("PRoduct ID IS", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Adding to wishlist...")
            },
            success: function (response) {
                // this_val.html("✓")
                this_val.html("<i class='fas fa-heart text-danger'></i>")
                if (response.bool === true) {
                    console.log("Added to wishlist...");
                }
            }
        })
    })


    // Remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function () {
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id is:", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Deleting product from wishlist...");
            },
            success: function (response) {
                $("#wishlist-list").html(response.data)
            }
        })
    })

})


// Making Default Address
$(document).on("click", ".make-default-address", function () {
    let id = $(this).attr("data-address-id")
    let this_val = $(this)

    console.log("ID is:", id);
    console.log("Element is:", this_val);

    $.ajax({
        url: "/make-default-address",
        data: {
            "id": id
        },
        dataType: "json",
        success: function (response) {
            console.log("Address Made Default....");
            if (response.boolean == true) {

                $(".check").hide()
                $(".action_btn").show()

                $(".check" + id).show()
                $(".button" + id).hide()
            }
        }
    })
})


$(document).on("submit", "#contact-form-ajax", function (e) {
    e.preventDefault()
    console.log("Submited...");

    let full_name = $("#full_name").val()
    let email = $("#email").val()
    let phone = $("#phone").val()
    let subject = $("#subject").val()
    let message = $("#message").val()

    console.log("Name:", full_name);
    console.log("Email:", email);
    console.log("Phone:", phone);
    console.log("Subject:", subject);
    console.log("MEssage:", message);

    $.ajax({
        url: "/ajax-contact-form",
        data: {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
        },
        dataType: "json",
        beforeSend: function () {
            console.log("Sending Data to Server...");
        },
        success: function (res) {
            console.log("Sent Data to server!");
            $(".contact_us_p").hide()
            $("#contact-form-ajax").hide()
            $("#message-response").html("Message sent successfully.")
        }
    })
})



