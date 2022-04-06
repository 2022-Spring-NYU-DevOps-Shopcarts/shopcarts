$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#user_id").val(res.user_id);
        $("#item_id").val(res.item_id);
        $("#item_name").val(res.item_name);
        $("#quantity").val(res.quantity);
        $("#price").val(res.price);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#user_id").val("");
        $("#item_id").val("");
        $("#item_name").val("");
        $("#quantity").val("");
        $("#price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Create an empty Shopcart
    // ****************************************

    $("#create-shopcart-btn").click(function () {

        let user_id = Number($("#user_id").val());

        let data = {
            "user_id": user_id
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            flash_message("Successfully Added an empty Shopcart")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-btn").click(function () {

        let user_id = parseInt($("#user_id").val());
        let item_id = parseInt($("#item_id").val());
        let item_name = $("#item_name").val();
        let quantity = parseInt($("#quantity").val());
        let price = parseInt($("#price").val());

        let data = {
            "item_id": item_id,
            "user_id": user_id,
            "item_name": item_name,
            "quantity": quantity,
            "price": price
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${user_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            flash_message("Successfully Added an Item")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-btn").click(function () {

        let pet_id = $("#pet_id").val();
        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";
        let gender = $("#pet_gender").val();
        let birthday = $("#pet_birthday").val();

        let data = {
            "name": name,
            "category": category,
            "available": available,
            "gender": gender,
            "birthday": birthday
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/pets/${pet_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-btn").click(function () {

        let user_id = $("#user_id").val();

        if (isNaN(user_id))
        {
            flash_message("Please enter a valid user id");
            return;
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${user_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Item ID</th>'
            table += '<th class="col-md-2">Item Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '</tr></thead><tbody>'
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.item_id}</td><td>${item.item_name}</td><td>${item.quantity}</td><td>${item.price}</td></tr>`;
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // List All Shopping Carts
    // ****************************************
    $("#list-all-shopcarts-btn").click(function () {

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts`,
            contentType: "application/json",
            data: ''
        })
        ajax.done(function(res){
            $("#shopcarts_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-5">Shopcart ID</th>'
            table += '</tr></thead><tbody class="scrollTbody">'
            var shopcart_list = [];
            for(let i = 0; i < res.length; i++) {
                shopcart_list.push(res[i].user_id);   
            }
            shopcart_list = Array.from(new Set(shopcart_list));
            for(let i = 0; i < shopcart_list.length; i++) {
                table +=  `<tr id="row_${i}"><td>${shopcart_list[i]}</td></tr>`;
            }
            if(res.length == 0){
                table +=  `<tr><td>No shopcarts in database</td></tr>`;
            }
            table += '</tbody></table>';
            $("#shopcarts_results").append(table);

            flash_message("Successfully list all the shopcarts")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-btn").click(function () {

        let pet_id = $("#pet_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/pets/${pet_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/pets?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '</tr></thead><tbody>'
            let firstPet = "";
            for(let i = 0; i < res.length; i++) {
                let pet = res[i];
                table +=  `<tr id="row_${i}"><td>${pet._id}</td><td>${pet.name}</td><td>${pet.category}</td><td>${pet.available}</td><td>${pet.gender}</td><td>${pet.birthday}</td></tr>`;
                if (i == 0) {
                    firstPet = pet;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
