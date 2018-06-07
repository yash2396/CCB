$( document ).ready(function(){

    $(".button-collapse").sideNav({
        draggable: true,
        onOpen: function() {document.getElementById('logout').style.display = "block";},
        onClose: function() {document.getElementById('logout').style.display = "none";},
    });

    $('select').material_select();

    $('.modal').modal({
          dismissible: true
    });

});

function load_animation(id) {
    Materialize.fadeInImage('.success-response');
    setTimeout(function(){Materialize.fadeInImage('.total-response');}, 200);
    setTimeout(function(){Materialize.fadeInImage('.color-code');}, 400);
    setTimeout(function(){Materialize.fadeInImage('.main-card');}, 200);
    setTimeout(function(){Materialize.showStaggeredList(id + "-list");}, 500);

    $('.count').each(function() {
      $(this).prop('Counter', 0).animate({
        Counter: $(this).text()
      }, {
        duration: 1000,
        easing: 'swing',
        step: function(now) {
          $(this).text(Math.ceil(now));
        }
      });
    });
}

function tab_link(id, flag) {
    var id_ = $(id).attr("href");

    $(id_ + "-height").css("height", "54px");

    $(".side-nav li.active").removeClass("active");
    $(id_ + "-li").addClass("active");

    $(".hide-fix").css("display","none");
    document.getElementById('change-password').style.display = "none";
    if (flag) {
        document.getElementById('change-email').style.display = "none";
    }

    $(".success-response").css("opacity","0");
    $(".total-response").css("opacity","0");
    $(".color-code").css("opacity","0");
    $(".main-card").css("opacity","0");
    $(".list-response > li").css("opacity","0");

    $(id_).css("display","block");

    load_animation(id_);
}

function open_modal(id) {
      $(id).modal('open');
}

function editable(id) {
    document.getElementById('edit-modal-' + id).innerHTML = document.getElementById('input-' + id).value;
}

function submit_data(prefix_id, list_id, modal_id) {
    var department = document.getElementsByName(prefix_id)[0].value;

    for (var i = 0; i < list_id.length; i++) {
        var data_ = document.getElementById('input-' + prefix_id + "-" + list_id[i]).value;
        if(data_ === ""){
            document.getElementById('error-' + prefix_id + "-"  + modal_id).innerHTML = "Please fill all before clicking on update button.";
            return false;
        }
    }

    $('#btn-' + prefix_id + "-"  + modal_id).addClass("disabled");
    $('#load-' + prefix_id + "-"  + modal_id).addClass(" loading-btn");

    var full_data = "{";

    for (var i = 0; i < list_id.length; i++) {
        full_data += "'" + document.getElementsByName(list_id[i])[0].value + "': '" + document.getElementById('input-' + prefix_id + "-" + list_id[i]).value + "', ";
    }
    full_data += "}";

    $.ajax({
        type: "POST",
        url: "/update-data",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        data: 'department=' + department + "&full_data=" + full_data,

        success: function (data) {
            for (var i = 0; i < list_id.length; i++) {
                var data_ = document.getElementById('input-' + prefix_id + "-" + list_id[i]).value;
                document.getElementById('edited-' + prefix_id + "-"  + list_id[i]).innerHTML = data_;
                document.getElementById('edited-modal-' + prefix_id + "-"  + list_id[i]).innerHTML = data_;
                document.getElementById('edit-modal-' + prefix_id + "-"  + list_id[i]).innerHTML = data_;
                document.getElementById('input-' + prefix_id + "-"  + list_id[i]).value = "";
                $('#input-' + prefix_id + "-"  + list_id[i]).blur();
            }

            $('#modal-' + modal_id).modal('close');
            Materialize.toast(data, 8000, 'light-green');
        },

        error: function () {
            $('#modal-' + modal_id).modal('close');
            Materialize.toast("Failed to Update.", 8000, 'red');
        }
    });

    $('#btn-' + prefix_id + "-"  + modal_id).removeClass("disabled");
    $('#load-' + prefix_id + "-"  + modal_id).removeClass(" loading-btn");
}

function change_password(flag) {
    $("#password-height").css("height", "54px");

    $(".side-nav li.active").removeClass("active");
    $("#password-li").addClass("active");

    $(".hide-fix").css("display","none");

    if (flag) {
        document.getElementById('change-email').style.display = "none";
    }

    document.getElementById('change-password').style.display = "block";

    $("#password-card").css("opacity","0");
    Materialize.fadeInImage('#password-card');
}

function update_password() {
    var role = document.getElementById('password-role').value;
    var password = document.getElementById('password').value;
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;

    if(password === "" || password1 === "" || password2 === ""){
        document.getElementById('error-password').innerHTML = "Please fill all before clicking on update button.";
        return false;
    }
    else if (password1.localeCompare(password2) !== 0){
        document.getElementById('error-password').innerHTML = "Both New Password and Confirm Password must be same.";
        return false;
    }
    else {
        $('#btn-password').addClass("disabled");
        $('#load-password').addClass(" loading-btn");

        $.ajax({
                type: "POST",
                url: "/update-password",
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                data: 'role=' + role + '&old_password=' + MD5(password) + "&new_password=" + MD5(password1),
                success: function (data) {
                    Materialize.toast(data.message, 8000, data.color);

                    document.getElementById('password').value = "";
                    document.getElementById('password1').value = "";
                    document.getElementById('password2').value = "";

                    $('#password').blur();
                    $('#password1').blur();
                    $('#password2').blur();

                    document.getElementById('error-password').innerHTML = "";
                },
                error: function () {
                    Materialize.toast("Failed to Update.", 8000, 'red');
                }
        });

        $('#btn-password').removeClass("disabled");
        $('#load-password').removeClass(" loading-btn");
    }
}
