var forfile = ''
var calcfile = ''

$( document ).ready(function() {
    console.log( "MEGARA Online ETC ready!" );

//    $('html').animate({scrollTop:0}, 1);
//    $('body').animate({scrollTop:0}, 1);
    $(window).load(function(){ $("html,body").animate({scrollTop: 0}, 1); });
//    window.location = (""+window.location).replace(/#[A-Za-z0-9_]*$/,'')+"#outheaders";
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
            // Put the results in div
            posting.done(function (data) {
                console.log($(data))
                var content = $(data).find("#content");

//                $("#result2").empty().append($(data)[0]['outtext'] + $(data)[0]['textcout'] + $(data)[0]['textlout'] + $(data)[0]['textinput']);
                $("#result4").empty().append($(data)[0]['outtext'] + $(data)[0]['tablecout'] + $(data)[0]['tablelout'] + $(data)[0]['tableinput']);

                var outputhead1 = $(data)[0]['outhead1'];
                $("#outhead1").empty().append(outputhead1);

                var newpsf = $(data)[0]['tablenewpsf'];
                $("#resultnewpsf").empty().append(newpsf);

                var newpsfline = $(data)[0]['tablenewpsfline'];
                $("#resultnewpsfline").empty().append(newpsfline);

                // MathJax Typesetting:
                // Insert 'tablecalc' as a string into variable mathtable which
                // will appear in the HTML ID #resultmath.
                // Then, get the pre-defined id (in tablecalc), in this case mathid
                // and typeset the string.
                var mathtable = $(data)[0]['tablecalc'];
                $("#resultmath").empty().append(mathtable);
                var mathid = document.getElementById("mathid");
                MathJax.Hub.Queue(["Typeset",MathJax.Hub, "mathid"]);

                // Make 'store result' button visible
                $("#store_result").css('visibility', 'visible');
                forfile = $(data)[0]['forfile'];    // global variable update
                calcfile = $(data)[0]['forfile2'];  // global variable update
                // Graphics
                var thediv = $(data)[0]['thediv'];
                var thescript = $(data)[0]['thescript'];
                $("#othergraphic").empty().append(thediv);
                $("#othergraphic").append(thescript);

                //$('.btn-primary').css('color','#fff');
                //$('.btn-primary').css('background-color','#337ab7');
                //$('.btn-primary').css('border-color','#2e6da4');
            });
            $("input[type=submit]").css('visibility', 'hidden');
        }
    });
});


function downloadFile(forfile) {
    var save = document.createElement('a');
    save.href = 'data:attachment/txt,' + encodeURI(forfile);
    save.download = 'MEGARA-ETC-output.txt' || forfile;
    var event = document.createEvent("MouseEvents");
        event.initMouseEvent(
                "click", true, false, window, 0, 0, 0, 0, 0
                , false, false, false, false, 0, null
        );
    save.dispatchEvent(event);
//    var wnd = window.open("about:blank", "", 'height=900,width=740,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes,target=_blank');
//    wnd.document.write(forfile);
}

function downloadCalcFile(calcfile){
    var save = document.createElement('a');
    save.href = 'data:attachment/html,' + encodeURI(calcfile);
    save.download = 'MEGARA-ETC-details.html' || calcfile;
    var event = document.createEvent("MouseEvents");
        event.initMouseEvent(
                "click", true, false, window, 0, 0, 0, 0, 0
                , false, false, false, false, 0, null
        );
    save.dispatchEvent(event);
}

// pop-up window
function newPopup(url) {
popupWindow = window.open(
url,'popUpWindow','height=400,width=300,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}

// bigger pop-up window
function newPopupBig(url) {
popupWindow = window.open(
url,'popUpWindow','height=900,width=740,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
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


//change 'fibers' (in LCB mode) to 'bundles' (in MOS mode)
function selectorOmode() {
    if (document.getElementById('id_om_val').value=='LCB') {
        var nst = 'Number of Sky Fibers';
        var nsdefval = 56;
        var ntdefval = 567;
        var ntt = 'Number of Target Fibers';
    }
    else if (document.getElementById('id_om_val').value=='MOS') {
        var nst = 'Number of Sky Bundles';
        var nsdefval = 1;
        var ntdefval = 91;
        var ntt = 'Number of Target Bundles';
    }
    document.getElementById('id_nst').innerHTML = nst;
    document.getElementById('id_ntt').innerHTML = ntt;
    document.getElementById('id_nsbundles').value = nsdefval;
    document.getElementById('id_ntbundles').value = ntdefval;
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
    setCookie("the_seeing", myform.id_seeing.options[myform.id_seeing.selectedIndex].text, 365);
    setCookie("the_seeing_pk", myform.id_seeing.value, 365);

    setCookie("the_numframes", myform.id_numframes.value, 365);
    setCookie("the_exptimepframe", myform.id_exptimepframe.value, 365);
    setCookie("the_nsbundles", myform.id_nsbundles.value, 365);
    setCookie("the_ntbundles", myform.id_ntbundles.value, 365);
    if (document.getElementById("id_om_val").value == 'MOS') {
        setCookie("the_nst", "Number of Sky Bundles", 365);
        setCookie("the_ntt", "Number of Target Bundles", 365);
    }
    else if (document.getElementById('id_om_val').value == 'LCB') {
        setCookie("the_nst", "Number of Sky Fibers", 365);
        setCookie("the_ntt", "Number of Target Fibers", 365);
    }
    setCookie("the_lineap", myform.id_lineap.value, 365);
    setCookie("the_contap", myform.id_contap.value, 365);
    if (document.getElementById("id_plotflag_0").checked == true) {
        setCookie("the_plotflag", myform.id_plotflag_0.value, 365);
    }
    else if (document.getElementById("id_plotflag_1").checked == true) {
        setCookie("the_plotflag", myform.id_plotflag_1.value, 365);
    }
    if (window.counter%2==0) {
        setCookie("the_colorflag", 0, 365);
    }
    else if (window.counter%2==1) {
        setCookie("the_colorflag", 1, 365);
    }
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
    var fname_seeing_pk=getCookie("the_seeing_pk");

    var fname_numframes=getCookie("the_numframes");
    var fname_exptimepframe=getCookie("the_exptimepframe");
    var fname_nsbundles=getCookie("the_nsbundles");
    var fname_ntbundles=getCookie("the_ntbundles");
    var fname_nst=getCookie("the_nst");
    var fname_ntt=getCookie("the_ntt");

    var fname_lineap=getCookie("the_lineap");
    var fname_contap=getCookie("the_contap");

    var fname_plotflag=getCookie("the_plotflag");
    var fname_colorflag=getCookie("the_colorflag");

	if (fname_radius==null) {fname_radius="";}
	if (fname_radius!="" && fname_radius!="") {fname_radius="the_radius="+fname_radius;}
	alert ('These are the cookies currently stored in your browser:'+
	'\nstype = '+fname_stype+
	'\ninput size = '+fname_isize+
	'\nwith area = '+fname_area+
	'\nwith radius = '+fname_radius+
	'\nwith iflux = '+fname_iflux+
	'\nwith rline = '+fname_rline+
	'\nwith spectype = '+fname_spectype+
	'\nwith pfilter = '+fname_pfilter+
	'\nwith contmagflux = '+fname_contmagflux+
	'\nwith contmagval = '+fname_contmagval+
	'\nwith contfluxval = '+fname_contfluxval+
	'\nwith lineflux = '+fname_lineflux+
	'\nwith linewave = '+fname_linewave+
	'\nwith linefwhm = '+fname_linefwhm+

	'\nwith om_val = '+fname_om_val+
	'\nwith vph = '+fname_vph+
	'\nwith skycond = '+fname_skycond+
	'\nwith moonph = '+fname_moonph+
	'\nwith airmass = '+fname_airmass+
	'\nwith seeing = '+fname_seeing+' (pk='+fname_seeing_pk+')'+
	'\nwith numframes = '+fname_numframes+
	'\nwith exptimepframe = '+fname_exptimepframe+
	'\nwith nsbundles = '+fname_nsbundles+
	'\nwith ntbundles = '+fname_ntbundles+
	'\nwith nst = '+fname_nst+

	'\nwith lineap = '+fname_lineap+
	'\nwith contap = '+fname_contap+
	'\nwith plotflag = '+fname_plotflag+
	'\nwith colorflag = '+fname_colorflag+
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
  document.cookie = "the_seeing_pk=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_numframes=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_exptimepframe=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_nsbundles=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_ntbundles=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_nst=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_ntt=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_lineap=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_contap=; expires=Thu, 01 Jan 2000 00:00:00 GMT";

  document.cookie = "the_plotflag=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  document.cookie = "the_colorflag=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
  alert ('Cookies deleted.');
  window.location.reload();
  myform.reset();
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
        document.getElementById('id_seeing').value = getCookie('the_seeing_pk');

        document.getElementById('id_numframes').value = getCookie('the_numframes');
        document.getElementById('id_exptimepframe').value = getCookie('the_exptimepframe');
        document.getElementById('id_nsbundles').value = getCookie('the_nsbundles');
        document.getElementById('id_ntbundles').value = getCookie('the_ntbundles');
        document.getElementById('id_nst').innerHTML = getCookie('the_nst');
        document.getElementById('id_ntt').innerHTML = getCookie('the_ntt');

        document.getElementById('id_lineap').value = getCookie('the_lineap');
        document.getElementById('id_contap').value = getCookie('the_contap');
        if (getCookie("the_plotflag") == 'no') {
            document.getElementById('id_plotflag_0').checked = true;
            }
        else {
            document.getElementById('id_plotflag_1').checked = true;
        }
        if (getCookie("the_colorflag") == '1') {
            twofunc();
        }

    }
}

//compute number of free ("target") bundles from nsbundle
function calculateNtbund() {
    var nsbundles_var = document.getElementById('id_nsbundles').value;
    if (document.getElementById('id_om_val').value=='LCB') {
        var ntbundles = 623 - nsbundles_var;
    }
    else if (document.getElementById('id_om_val').value=='MOS') {
        var ntbundles = 92 - nsbundles_var;
    }
    document.getElementById('id_ntbundles').value = parseInt(ntbundles);
}
//compute number of sky bundles from ntbundle
function calculateNsbund() {
    var ntbundles_var = document.getElementById('id_ntbundles').value;
    if (document.getElementById('id_om_val').value=='LCB') {
        var nsbundles = 623 - ntbundles_var;
    }
    else if (document.getElementById('id_om_val').value=='MOS') {
        var nsbundles = 92 - ntbundles_var;
    }
    document.getElementById('id_nsbundles').value = parseInt(nsbundles);
}

function chBackcolor(color) {
   document.body.style.backgroundColor = color;
}

function changeALL(){
    var css='html {-webkit-filter: invert(100%);'+'-moz-filter: invert(100%);'+'-o-filter: invert(100%);'+'-ms-filter: invert(100%); }',head=document.getElementsByTagName('head')[0],style=document.createElement('style');
        if(!window.counter){
            window.counter=1;
            }
        else{window.counter++;
            if(window.counter%2==0){
                var css='html {-webkit-filter: invert(0%); -moz-filter: invert(0%); -o-filter: invert(0%); -ms-filter: invert(0%); }'
                }
            };
            style.type='text/css';
            if(style.styleSheet){
                style.styleSheet.cssText=css;
                }
            else{
                style.appendChild(document.createTextNode(css));
                }
            head.appendChild(style);
}

function twofunc() {
    changeALL();
    if(window.counter%2==0){
        chBackcolor('white');
        }
    else {
        chBackcolor('black');
    }
}
// -->