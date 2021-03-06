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
        $("#hold").val(res.hold);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#user_id").val("");
        $("#item_id").val("");
        $("#item_name").val("");
        $("#quantity").val("");
        $("#price").val("");
        $("#hold").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Create Empty Shopcart
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
            flash_message("Successfully added an empty shopcart")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Create Item
    // ****************************************

    $("#add-to-shopcart-btn").click(function () {

        let user_id = parseInt($("#user_id").val());
        let item_id = parseInt($("#item_id").val());
        let item_name = $("#item_name").val();
        let quantity = parseInt($("#quantity").val());
        let price = parseFloat($("#price").val());
        let hold = $("#hold").val();

        let data = {
            "item_id": item_id,
            "user_id": user_id,
            "item_name": item_name,
            "quantity": quantity,
            "price": price,
            "hold": hold
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${user_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            flash_message("Successfully added an Item")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve Item
    // ****************************************
    $("#get-item-btn").click(function (){
        let user_id = parseInt($("#user_id").val());
        let item_id = parseInt($("#item_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${user_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Item ID</th>'
            table += '<th class="col-md-2">Item Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Hold</th>'
            table += '</tr></thead><tbody>'

            let item = res;
            table += `<tr><td>${item.item_id}</td><td>${item.item_name}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.hold}</td></tr>`;
            table += '</tbody></table>';
            $("#search_results").append(table);
            flash_message("Successfully retrieved the item")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });



    // ****************************************
    // Update Item
    // ****************************************

    $("#update-item-btn").click(function () {

        let user_id = parseInt($("#user_id").val());
        let item_id = parseInt($("#item_id").val());
        let quantity = parseInt($("#quantity").val());
        let price = parseFloat($("#price").val());
        
        // alert($("#price").val())
        let data = {};
        if ($("#quantity").val() == "0") {
            data["quantity"] = 0;
        }
        else if (!isNaN(quantity)) {
            data["quantity"] = quantity;
        }
        else if ($("#quantity").val() != "") {
            data["quantity"] = $("#quantity").val()
        }
        if ($("#price").val() == "0") {
            data["price"] = 0.0;
        }
        else if (!isNaN(price)) {
            data["price"] = price;
        }
        else if($("#price").val() != "") {
            data["price"] = $("#price").val()
        }
        // alert(data["price"])
        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/shopcarts/${user_id}/items/${item_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Item ID</th>'
            table += '<th class="col-md-2">Item Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Hold</th>'
            table += '</tr></thead><tbody>'

            let item = res;
            table += `<tr><td>${item.item_id}</td><td>${item.item_name}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.hold}</td></tr>`;
            table += '</tbody></table>';
            $("#search_results").append(table);
            flash_message(`Successfully updated the item`)
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {

        let user_id = Number($("#user_id").val());

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
            table += '<th class="col-md-2">Hold</th>'
            table += '</tr></thead><tbody>'
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.item_id}</td><td>${item.item_name}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.hold}</td></tr>`;
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            flash_message("Successfully retrieved the shopcart")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // List All Shopcarts
    // ****************************************
    $("#list-all-shopcarts-btn").click(function () {

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts`,
            // contentType: "application/json",
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

            flash_message("Successfully listed all the shopcarts")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Delete an Item
    // ****************************************

    $("#remove-btn").click(function () {

        let user_id = parseInt($("#user_id").val());
        let item_id = parseInt($("#item_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${user_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            clear_form_data()
            flash_message("Successfully deleted an item")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message("Successfully deleted an item")
        });
    });

    // ****************************************
    // Hold Item
    // ****************************************
    $("#hold-for-later-btn").click(function (){
        let user_id = Number($("#user_id").val());
        let item_id = Number($("#item_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${user_id}/items/${item_id}/hold`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            // alert(res.toSource())
            // $("#search_results").empty();
            // let table = '<table class="table table-striped" cellpadding="10">'
            // table += '<thead><tr>'
            // table += '<th class="col-md-2">Item ID</th>'
            // table += '<th class="col-md-2">Item Name</th>'
            // table += '<th class="col-md-2">Quantity</th>'
            // table += '<th class="col-md-2">Price</th>'
            // table += '<th class="col-md-2">Hold</th>'
            // table += '</tr></thead><tbody>'

            // let item = res;
            // let i = 0;
            // table += `<tr id="row_${i}><td>${item.item_id}</td><td>${item.item_name}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.hold}</td></tr>`;
            // table += '</tbody></table>';
            // $("#search_results").append(table);
            clear_form_data()
            flash_message("Successfully put item on hold")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

     // ****************************************
     // Resume Item
     // ****************************************
     $("#resume-for-purchase-btn").click(function (){
        let user_id = Number($("#user_id").val());
        let item_id = Number($("#item_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${user_id}/items/${item_id}/resume`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            // alert(res.toSource())
            // $("#search_results").empty();
            // let table = '<table class="table table-striped" cellpadding="10">'
            // table += '<thead><tr>'
            // table += '<th class="col-md-2">Item ID</th>'
            // table += '<th class="col-md-2">Item Name</th>'
            // table += '<th class="col-md-2">Quantity</th>'
            // table += '<th class="col-md-2">Price</th>'
            // table += '<th class="col-md-2">Hold</th>'
            // table += '</tr></thead><tbody>'

            // let item = res;
            // table += `<tr><td>${item.item_id}</td><td>${item.item_name}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.hold}</td></tr>`;
            // table += '</tbody></table>';
            // $("#search_results").append(table);
            clear_form_data()
            flash_message("Successfully resumed item for purchase")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Clear Shopcart
    // ****************************************
    $("#clear-shopcart-btn").click(function() {

        let user_id = Number($("#user_id").val());

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${user_id}`,
            contentType: "application/json",
        });

        ajax.done(function(res){
            flash_message("Successfully cleared the shopcart" )
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    
    // ****************************************
    // Query Shopcart
    // ****************************************
    $("#search-shopcarts-btn").click(function () {

        let item_id = $("#item_id").val();

        let queryString = 'item-id=' + item_id;

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts?${queryString}`,
            //contentType: "application/json",
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
                table +=  `<tr><td>No shopcarts contains item ${item_id}</td></tr>`;
            }
            table += '</tbody></table>';
            $("#shopcarts_results").append(table);

            flash_message("Successfully listed search results.")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear the Form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search Item
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
