// === COMPRESSED FOR SECURITY QUESTIONS === //
$(document).ready(function() {
    $('form input').focusout(function(event) {
        var input = $(this);
        var user = $(this).val();
        if (user) {
            input.removeClass("invalid").addClass("valid")
        } else {
            input.removeClass("valid").addClass("invalid")
        }
    })
});
$(function() {
    $('#tou').avgrund({
        width: 380,
        height: 280,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'Close',
        template: '<div class="tou_popup"><center><h2>Flux - Terms of Use</h2></center><br><p>By accessing this web site, you are agreeing to be bound by these web site Terms and Conditions of Use, all applicable laws and regulations, and agree that you are responsible for compliance with any applicable local laws. If you do not agree with any of these terms, you are prohibited from using or accessing this site. The materials contained in this web site are protected by applicable copyright and trade mark law.</p><br><center><a href="http://termsfeed.com/terms-service/generator/#get_started" target="_blank">Terms of use generator</a></center></div>'
    })
});
$(function() {
    $('#about').avgrund({
        width: 380,
        height: 300,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'Close',
        template: '<div class="about_popup"><center><h2>Flux - About</h2></center><br><p>Lorem ipsum dolor sit amet, wisi aliquet accumsan magna purus nulla tincidunt. Malesuada quisque suspendisse nec lobortis, cursus nec rutrum duis commodo volutpat tempus, integer natoque lacinia sed, rutrum erat ipsum lobortis viverra. Gravida aliquet nostra commodo massa malesuada, dis facilisis sed, urna ultrices luctus vivamus, nam magnam. Ligula parturient ullamcorper arcu. Massa tortor in, ut erat dui, nascetur nunc velit arcu amet dictum id, placerat cras hymenaeos velit pellentesque, in nonummy. Elit pede a praesent ut in, maecenas nec ipsum inceptos.</p></div>'
    })
});
$(function() {
    $('#contact').avgrund({
        width: 380,
        height: 300,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'Close',
        template: '<div class="contact_popup"><center><h2>Flux - Contact</h2></center><br><p>Lorem ipsum dolor sit amet, wisi aliquet accumsan magna purus nulla tincidunt. Malesuada quisque suspendisse nec lobortis, cursus nec rutrum duis commodo volutpat tempus, integer natoque lacinia sed, rutrum erat ipsum lobortis viverra. Gravida aliquet nostra commodo massa malesuada, dis facilisis sed, urna ultrices luctus vivamus, nam magnam. Ligula parturient ullamcorper arcu. Massa tortor in, ut erat dui, nascetur nunc velit arcu amet dictum id, placerat cras hymenaeos velit pellentesque, in nonummy. Elit pede a praesent ut in, maecenas nec ipsum inceptos.</p></div>'
    })
});
$(function() {
    $('#info').avgrund({
        width: 380,
        height: 300,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'Close',
        template: '<div class="info_popup"><center><h2>Flux - Info</h2></center><br><p>Lorem ipsum dolor sit amet, wisi aliquet accumsan magna purus nulla tincidunt. Malesuada quisque suspendisse nec lobortis, cursus nec rutrum duis commodo volutpat tempus, integer natoque lacinia sed, rutrum erat ipsum lobortis viverra. Gravida aliquet nostra commodo massa malesuada, dis facilisis sed, urna ultrices luctus vivamus, nam magnam. Ligula parturient ullamcorper arcu. Massa tortor in, ut erat dui, nascetur nunc velit arcu amet dictum id, placerat cras hymenaeos velit pellentesque, in nonummy. Elit pede a praesent ut in, maecenas nec ipsum inceptos.</p></div>'
    })
});
$(function() {
    if ($.browser.msie && $.browser.version <= 9) {
        $("[placeholder]").focus(function() {
            if ($(this).val() == $(this).attr("placeholder")) $(this).val("")
        }).blur(function() {
            if ($(this).val() == "") $(this).val($(this).attr("placeholder"))
        }).blur();
        $("[placeholder]").parents("form").submit(function() {
            $(this).find('[placeholder]').each(function() {
                if ($(this).val() == $(this).attr("placeholder")) {
                    $(this).val("")
                }
            })
        })
    }
});
$(document).ready(function() {
    $('.btn_register').click(function() {
        valReg()
    });
    function valReg() {
        var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
        var user = $('#user').val();
        var email = $('#email').val();
        var password = $('#password').val();
        var rpassword = $('#rpassword').val();
        var inputVal = new Array(user, email, password, rpassword);
        var error = new Array("Username", "Email", "Password", "Password");
        if (inputVal[0] == "") {
            $('#user').attr('placeholder', 'Please enter an ' + error[0]);
            $('#user').addClass('invalid_placeholder');
            $('#user').removeClass("valid").addClass("invalid")
        } else {
            $('#user').removeClass('invalid_placeholder');
            $('#user').removeClass("invalid").addClass("valid")
        }
        if (inputVal[1] == "") {
            $('#email').attr('placeholder', 'Please enter your ' + error[1]);
            $('#email').addClass('invalid_placeholder');
            $('#email').removeClass("valid").addClass("invalid")
        } else if (!emailReg.test(email)) {
            $('#email').attr('placeholder', 'Please enter a valid Email address');
            $('#email').addClass('invalid_placeholder');
            $('#email').removeClass("valid").addClass("invalid")
        } else {
            $('#email').removeClass('invalid_placeholder');
            $('#email').removeClass("invalid").addClass("valid")
        }
        if (inputVal[2] == "") {
            $('#password').attr('placeholder', 'Please enter a ' + error[2]);
            $('#password').addClass('invalid_placeholder');
            $('#password').removeClass("valid").addClass("invalid")
        } else {
            $('#password').removeClass('invalid_placeholder');
            $('#password').removeClass("invalid").addClass("valid")
        }
        if (inputVal[3] == "") {
            $('#rpassword').attr('placeholder', 'Please repeat the ' + error[3]);
            $('#rpassword').addClass('invalid_placeholder');
            $('#rpassword').removeClass("valid").addClass("invalid")
        } else {
            $('#rpassword').removeClass('invalid_placeholder');
            $('#rpassword').removeClass("invalid").addClass("valid")
        }
    }
    $('.btn_login').click(function() {
        valLogin()
    });
    function valLogin() {
        var user = $('#l_user').val();
        var password = $('#l_password').val();
        var inputVal = new Array(user, password);
        var error = new Array("Username", "Password");
        if (inputVal[0] == "") {
            $('#l_user').attr('placeholder', 'Enter ' + error[0]);
            $('#l_user').addClass('invalid_placeholder');
            $('#l_user').removeClass("valid").addClass("invalid")
        } else {
            $('#l_user').removeClass('invalid_placeholder');
            $('#l_user').removeClass("invalid").addClass("valid")
        }
        if (inputVal[1] == "") {
            $('#l_password').attr('placeholder', 'Enter ' + error[1]);
            $('#l_password').addClass('invalid_placeholder');
            $('#l_password').removeClass("valid").addClass("invalid")
        } else {
            $('#l_password').removeClass('invalid_placeholder');
            $('#l_password').removeClass("invalid").addClass("valid")
        }
    }
});
$(document).ready(function() {
    var $div = $('#box');
    var height = $div.height();
    $div.css({
        marginTop: 100
    });
    $div.animate({
        marginTop: 180
    },
    {
        duration: 800,
        complete: function() {
            $div.animate({
                marginTop: 170
            },
            {
                duration: 400,
                complete: function() {}
            })
        }
    });
    setTimeout(function() {
        $('.buy_btn').fadeIn()
    },
    1000)
});