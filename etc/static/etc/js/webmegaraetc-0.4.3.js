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
        $('label[for="id_isize_0"]').each(function() {
            this.style.color = "grey"
        });
//        document.getElementById("id_isize_0").checked = true;
        document.getElementById("id_isize_0").disabled = true;
        document.getElementById("id_isize_1").disabled = true;
        document.getElementById("id_size").disabled = true;
        document.getElementById("id_size").style.color = "grey";
        document.getElementById("id_radius").disabled = true;
        document.getElementById("id_radius").style.color = "grey";

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
        if (document.getElementById("id_isize_0").checked == true) {
            document.getElementById("id_size").disabled = false;
            document.getElementById("id_size").style.color = "black";
            document.getElementById("id_radius").disabled = true;
            document.getElementById("id_radius").style.color = "grey";
        }
        else if (document.getElementById("id_isize_0").checked == false){
            document.getElementById("id_size").disabled = true;
            document.getElementById("id_size").style.color = "grey";
            document.getElementById("id_radius").disabled = false;
            document.getElementById("id_radius").style.color = "black";
        }
//        document.getElementById("id_size").disabled = true;
//        document.getElementById("id_size").style.color = "black";

        document.getElementById("id_isize_0").disabled = false;
        document.getElementById("id_isize_1").disabled = false;

        document.getElementById("id_isize_0").style.color = "black";
        document.getElementById("id_radius").style.color = "black";

        $('label[for="id_isize_0"]').each(function() {
            this.style.color = "black"
        });
        $('label[for="id_isize_1"]').each(function() {
            this.style.color = "black"
        });

    }
}

// for input area type
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
//        document.getElementById("id_rline_0").checked = true;

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

// FOR COOKIES
// get cookie = read cookie and return
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length,c.length);
		}
	}
	return "";
}

// set cookie = create the cookie with name, value, and expiration days
function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires;
}

// store values of form
function storeValues(form)
  {
    if (document.getElementById("id_stype_0").checked == true) {
        setCookie("the_stype", myform.id_stype_0.value, 365);
    }
    else if (document.getElementById("id_stype_1").checked == true) {
        setCookie("the_stype", myform.id_stype_1.value, 365);
    }
    if (document.getElementById("id_isize_0").checked == true) {
        setCookie("the_isize", myform.id_isize_0.value, 365);
    }
    else if (document.getElementById("id_isize_1").checked == true) {
        setCookie("the_isize", myform.id_isize_1.value, 365);
    }

    setCookie("the_area", myform.id_size.value, 365);
    setCookie("the_radius", myform.id_radius.value, 365);

    if (document.getElementById("id_iflux_0").checked == true) {
        setCookie("the_iflux", myform.id_iflux_0.value, 365);
    }
    else if (document.getElementById("id_iflux_1").checked == true) {
        setCookie("the_iflux", myform.id_iflux_1.value, 365);
    }
    if (document.getElementById("id_rline_0").checked == true) {
        setCookie("the_rline", myform.id_rline_0.value, 365);
    }
    else if (document.getElementById("id_rline_1").checked == true) {
        setCookie("the_rline", myform.id_rline_1.value, 365);
    }

    setCookie("the_spectype", myform.id_spectype.value, 365);
    setCookie("the_pfilter", myform.id_pfilter.value, 365);

    if (document.getElementById("id_contmagflux_0").checked == true) {
        setCookie("the_contmagflux", myform.id_contmagflux_0.value, 365);
    }
    else if (document.getElementById("id_contmagflux_1").checked == true) {
        setCookie("the_contmagflux", myform.id_contmagflux_1.value, 365);
    }

    setCookie("the_contmagval", myform.id_contmagval.value, 365);
    setCookie("the_contfluxval", myform.id_contfluxval.value, 365);
    setCookie("the_lineflux", myform.id_lineflux.value, 365);
    setCookie("the_linewave", myform.id_linewave.value, 365);
    setCookie("the_linefwhm", myform.id_linefwhm.value, 365);

    setCookie("the_om_val", myform.id_om_val.value, 365);
    setCookie("the_vph", myform.id_vph.value, 365);
    setCookie("the_skycond", myform.id_skycond.value, 365);
    setCookie("the_moonph", myform.id_moonph.value, 365);
    setCookie("the_airmass", myform.id_airmass.value, 365);
    setCookie("the_seeing", myform.id_seeing.value, 365);
    setCookie("the_numframes", myform.id_numframes.value, 365);
    setCookie("the_exptimepframe", myform.id_exptimepframe.value, 365);
    setCookie("the_nfibers", myform.id_nfibers.value, 365);
    setCookie("the_lineap", myform.id_lineap.value, 365);
    setCookie("the_contap", myform.id_contap.value, 365);
//    setCookie("field3", form.field3.value, 365);
//    setCookie("field4", form.field4.value, 365);
    return true;
  }

// show cookies in alert window
function displayCookies() {
    var fname_stype=getCookie("the_stype");
    var fname_isize=getCookie("the_isize");
    var fname_area=getCookie("the_area");
    var fname_radius=getCookie("the_radius");
    var fname_iflux=getCookie("the_iflux");
    var fname_rline=getCookie("the_rline");
    var fname_spectype=getCookie("the_spectype");
    var fname_pfilter=getCookie("the_pfilter");
    var fname_contmagflux=getCookie("the_contmagflux");
    var fname_contmagval=getCookie("the_contmagval");
    var fname_contfluxval=getCookie("the_contfluxval");
    var fname_lineflux=getCookie("the_lineflux");
    var fname_linewave=getCookie("the_linewave");
    var fname_linefwhm=getCookie("the_linefwhm");

    var fname_om_val=getCookie("the_om_val");
    var fname_vph=getCookie("the_vph");
    var fname_skycond=getCookie("the_skycond");
    var fname_moonph=getCookie("the_moonph");
    var fname_airmass=getCookie("the_airmass");
    var fname_seeing=getCookie("the_seeing");
    var fname_numframes=getCookie("the_numframes");
    var fname_exptimepframe=getCookie("the_exptimepframe");
    var fname_nfibers=getCookie("the_nfibers");
    var fname_lineap=getCookie("the_lineap");
    var fname_contap=getCookie("the_contap");

	if (fname_radius==null) {fname_radius="";}
	if (fname_radius!="" && fname_radius!="") {fname_radius="the_radius="+fname_radius;}
	alert ('The current stype is= '+fname_stype+
	'\ninput size= '+fname_isize+
	'\nwith area= '+fname_area+
	'\nwith radius= '+fname_radius+
	'\nwith iflux= '+fname_iflux+
	'\nwith rline= '+fname_rline+
	'\nwith spectype= '+fname_spectype+
	'\nwith pfilter= '+fname_pfilter+
	'\nwith contmagflux= '+fname_contmagflux+
	'\nwith contmagval= '+fname_contmagval+
	'\nwith contfluxval= '+fname_contfluxval+
	'\nwith lineflux= '+fname_lineflux+
	'\nwith linewave= '+fname_linewave+
	'\nwith linefwhm= '+fname_linefwhm+

	'\nwith om_val= '+fname_om_val+
	'\nwith vph='+fname_vph+
	'\nwith skycond ='+fname_skycond+
	'\nwith moonph ='+fname_moonph+
	'\nwith airmass ='+fname_airmass+
	'\nwith seeing ='+fname_seeing+
	'\nwith numframes ='+fname_numframes+
	'\nwith exptimepframe ='+fname_exptimepframe+
	'\nwith nfibers ='+fname_nfibers+
	'\nwith lineap ='+fname_lineap+
	'\nwith contap ='+fname_contap+
	' ');
}

// delete cookies
function deleteCookies(name) {
  document.cookie = "the_stype=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_isize=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_area=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_radius=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_iflux=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_rline=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_spectype=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_pfilter=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_contmagflux=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_contmagval=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_contfluxval=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_lineflux=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_linewave=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_linefwhm=; expires=Thu, 01 Jan 2000 00:00:00 GMT";

  document.cookie = "the_om_val=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_vph=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_skycond=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_moonph=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_airmass=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_seeing=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_numframes=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_exptimepframe=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_nfibers=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_lineap=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_contap=; expires=Thu, 01 Jan 2000 00:00:00 GMT";

  location.reload();
  alert ('Cookies deleted.');
}

function readCookies() {
    if (getCookie("the_stype") != ""){
        if (getCookie("the_stype") == 'P') {
            document.getElementById('id_stype_0').checked = true;
            }
        else if (getCookie("the_stype") == 'E') {
            document.getElementById('id_stype_1').checked = true;
            document.getElementById('id_stype_1').onload = selector();
        }
        if (getCookie("the_isize") == 'A') {
            document.getElementById('id_isize_0').checked = true;
            }
        else if (getCookie("the_isize") == 'R') {
            document.getElementById('id_isize_1').checked = true;
            document.getElementById('id_isize_1').onload = selectInputSize();
        }
        document.getElementById('id_size').value = getCookie('the_area');
        document.getElementById('id_radius').value = getCookie('the_radius');

        if (getCookie("the_iflux") == 'C') {
            document.getElementById('id_iflux_0').checked = true;
            }
        else if (getCookie("the_iflux") == 'L') {
            document.getElementById('id_iflux_1').checked = true;
            document.getElementById('id_iflux_1').onload = selectInputflux();
        }
        if (getCookie("the_rline") == 'N') {
            document.getElementById('id_rline_0').checked = true;
            }
        else if (getCookie("the_rline") == 'Y') {
            document.getElementById('id_rline_1').checked = true;
            document.getElementById('id_rline_1').onload = selectRline();
        }

        document.getElementById('id_spectype').value = getCookie('the_spectype');
        document.getElementById('id_pfilter').value = getCookie('the_pfilter');

        if (getCookie("the_contmagflux") == 'M') {
            document.getElementById('id_contmagflux_0').checked = true;
            }
        else if (getCookie("the_contmagflux") == 'F') {
            document.getElementById('id_contmagflux_1').checked = true;
            document.getElementById('id_contmagflux_1').onload = selectcontmagflux();
        }

        document.getElementById('id_contmagval').value = getCookie('the_contmagval');
        document.getElementById('id_contfluxval').value = getCookie('the_contfluxval');
        document.getElementById('id_lineflux').value = getCookie('the_lineflux');
        document.getElementById('id_linewave').value = getCookie('the_linewave');
        document.getElementById('id_linefwhm').value = getCookie('the_linefwhm');

        document.getElementById('id_om_val').value = getCookie('the_om_val');
        document.getElementById('id_vph').value = getCookie('the_vph');
        document.getElementById('id_skycond').value = getCookie('the_skycond');
        document.getElementById('id_moonph').value = getCookie('the_moonph');
        document.getElementById('id_airmass').value = getCookie('the_airmass');
        document.getElementById('id_seeing').value = getCookie('the_seeing');
        document.getElementById('id_numframes').value = getCookie('the_numframes');
        document.getElementById('id_exptimepframe').value = getCookie('the_exptimepframe');
        document.getElementById('id_nfibers').value = getCookie('the_nfibers');
        document.getElementById('id_lineap').value = getCookie('the_lineap');
        document.getElementById('id_contap').value = getCookie('the_contap');
    }
}

// -->