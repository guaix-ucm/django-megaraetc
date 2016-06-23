$( document ).ready(function() {
    console.log( "ready!" );

    $('html').animate({scrollTop:0}, 1);
    $('body').animate({scrollTop:0}, 1);

    $body = $("body");
    $(document).on({
        ajaxStart: function() { $body.addClass("loading");    },
        ajaxStop: function() { $body.removeClass("loading"); }
    });

    $( "#myform" ).submit(function( event ) {
        // Stop form from submitting normally
        event.preventDefault();
        if ($('#id_vph').val() == 1){
            alert('WARNING: VPH Setup is set to -empty-! Choose a VPH.')
        }
        else {
            //// Send the data using post
            var posting = $.post("/etc/do", $(this).serialize());
            //
            // Put the results in a div
            posting.done(function (data) {
                console.log($(data))
                $(data)[0]['graphic']
                var content = $(data).find("#content");
                $("#result").empty().append($(data)[0]['graphic']);
//                $("#result2").empty().append($(data)[0]['outtext'] + $(data)[0]['textcout'] + $(data)[0]['textlout'] + $(data)[0]['textinput']);
                $("#result4").empty().append($(data)[0]['outtext'] + $(data)[0]['tablecout'] + $(data)[0]['tablelout'] + $(data)[0]['tableinput']);
                $("#store_result").css('visibility', 'visible');
                //$('.btn-primary').css('color','#fff');
                //$('.btn-primary').css('background-color','#337ab7');
                //$('.btn-primary').css('border-color','#2e6da4');
            });
            $("input[type=submit]").css('visibility', 'hidden')
        }
    });
});

// pop-up window
function newPopup(url) {
popupWindow = window.open(
url,'popUpWindow','height=400,width=300,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}

// bigger pop-up window
function newPopupBig(url) {
popupWindow = window.open(
url,'popUpWindow','height=800,width=740,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}

// close window alert
function closeWin() {
	alert("Just close the browser's tab to quit.")
}

// for source type
function selector() {
    if (document.getElementById("id_stype_0").checked == true) {
        document.getElementById("id_isize_0").disabled = true;
        document.getElementById("id_isize_1").disabled = true;
        document.getElementById("id_size").disabled = true;
        document.getElementById("id_size").style.color = "grey";
//        $('label[for="id_size"]').each(function() {
//            this.style.color = "grey"
//        });
        $('label[for="id_isize_0"]').each(function() {
            this.style.color = "grey"
        });
        $('label[for="id_isize_1"]').each(function() {
            this.style.color = "grey"
        });

        //document.getElementById("sizet").style.color = "grey";
    } else if (document.getElementById("id_stype_0").checked == false) {
        $('label[for="id_isize_0"]').each(function() {
            this.checked = true
        });
        $('label[for="id_isize_0"]').each(function() {
            this.style.color = "black"
        });
        document.getElementById("id_size").disabled = false;
        document.getElementById("id_size").style.color = "black";
        document.getElementById("id_isize").disabled = false;
        document.getElementById("id_isize_0").disabled = false;
        document.getElementById("id_isize_1").disabled = false;
        document.getElementById("id_isize_0").checked = true;
        document.getElementById("id_isize_0").style.color = "black";
        $('label[for="id_size"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_isize_0"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_isize_1"]').each(function() {
            this.style.color = "black"
        });

    }
}

// for source type
function selectInputSize() {
    if (document.getElementById("id_isize_0").checked == true) {
        document.getElementById("id_size").disabled = false;
        document.getElementById("id_size").style.color = "black";
        document.getElementById("id_radius").disabled = true;
        document.getElementById("id_radius").style.color = "grey";
    } else if (document.getElementById("id_isize_0").checked == false) {
        document.getElementById("id_size").disabled = true;
        document.getElementById("id_size").style.color = "grey";
        document.getElementById("id_radius").disabled = false;
        document.getElementById("id_radius").style.color = "black";
     }
}

// for continuum magnitude or flux
function selectcontmagflux() {
    if (document.getElementById("id_contmagflux_0").checked == true) {
        document.getElementById("id_contmagval").style.color = "black";
        document.getElementById("id_contmagval").disabled = false;
        document.getElementById("id_contfluxval").style.color = "grey";
        document.getElementById("id_contfluxval").disabled = true;
    } else if (document.getElementById("id_contmagflux_0").checked == false) {
        document.getElementById("id_contmagval").style.color = "grey";
        document.getElementById("id_contmagval").disabled = true;
        document.getElementById("id_contfluxval").style.color = "black";
        document.getElementById("id_contfluxval").disabled = false;
    }

}

// for input flux
function selectInputflux() {
    if (document.getElementById("id_iflux_0").checked == true) {
        $('label[for="id_lineflux"]').each(function() {
            this.style.color = "grey"
        });
        $('label[for="id_linewave"]').each(function() {
            this.style.color = "grey"
        });
        $('label[for="id_linefwhm"]').each(function() {
            this.style.color = "grey"
        });
        $('label[for="id_lineap"]').each(function() {
            this.style.color = "grey"
        });
        $('label[for="id_contap"]').each(function() {
            this.style.color = "grey"
        });
        $('label[for="id_rline_0"]').each(function() {
            this.style.color = "grey"
        });

        //document.getElementById("greylineflux").style.color = "grey";
        document.getElementById("id_lineflux").style.color = "grey";
        //document.getElementById("greylinewave").style.color = "grey";
        document.getElementById("id_linewave").style.color = "grey";
        //document.getElementById("greylinefwhm").style.color = "grey";
        document.getElementById("id_linefwhm").style.color = "grey";
        //document.getElementById("greylineap").style.color = "grey";
        document.getElementById("id_lineap").style.color = "grey";
        //document.getElementById("greycontap").style.color = "grey";
        document.getElementById("id_contap").style.color = "grey";

        document.getElementById("id_rline_0").disabled = true;
        document.getElementById("id_rline_1").disabled = true;

        document.getElementById("id_lineflux").disabled = true;
        document.getElementById("id_linewave").disabled = true;
        document.getElementById("id_linefwhm").disabled = true;
        document.getElementById("id_lineap").disabled = true;
        document.getElementById("id_contap").disabled = true;

    } else if (document.getElementById("id_iflux_0").checked == false) {
        $('label[for="id_lineflux"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_linewave"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_lineap"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_contap"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_rline_0"]').each(function() {
            this.style.color = "black"
        });

        document.getElementById("id_lineflux").style.color = "black";
        document.getElementById("id_linewave").style.color = "black";
        document.getElementById("id_lineap").style.color = "black";
        document.getElementById("id_contap").style.color = "black";


        document.getElementById("id_rline_0").disabled = false;
        document.getElementById("id_rline_1").disabled = false;
        document.getElementById("id_rline_0").checked = true;

        document.getElementById("id_lineflux").disabled = false;
        document.getElementById("id_linewave").disabled = false;
        document.getElementById("id_linefwhm").disabled = true;
        document.getElementById("id_lineap").disabled = false;
        document.getElementById("id_contap").disabled = false;

    }
}

// for resolved line
function selectRline() {
    if (document.getElementById("id_rline_0").checked == true) {
        $('label[for="id_linefwhm"]').each(function() {
            this.style.color = "grey"
        });
        document.getElementById("id_linefwhm").style.color = "grey";
        document.getElementById("id_linefwhm").disabled = true;
    } else if (document.getElementById("id_rline_0").checked == false) {

        $('label[for="id_linefwhm"]').each(function() {
            this.style.color = "black"
        });
        document.getElementById("id_linefwhm").style.color = "black";
        document.getElementById("id_linefwhm").disabled = false;
    }

}

// -->