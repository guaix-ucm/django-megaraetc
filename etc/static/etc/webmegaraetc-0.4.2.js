// by Alexandre BOUQUIN
// Start date: 27 May 2015
//
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
        document.getElementById("id_size").disabled = true;
        document.getElementById("id_size").style.color = "grey";
        document.getElementById("sizet").style.color = "grey";
    } else if (document.getElementById("id_stype_0").checked == false) {
        document.getElementById("id_size").disabled = false;
        document.getElementById("id_size").style.color = "black";
        document.getElementById("sizet").style.color = "black";
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
        document.getElementById("greylineflux").style.color = "grey";
        document.getElementById("id_lineflux").style.color = "grey";
        document.getElementById("greylinewave").style.color = "grey";
        document.getElementById("id_linewave").style.color = "grey";
        document.getElementById("greylineap").style.color = "grey";
        document.getElementById("id_lineap").style.color = "grey";
        document.getElementById("greycontap").style.color = "grey";
        document.getElementById("id_contap").style.color = "grey";

        document.getElementById("id_rline_0").disabled = true;
        document.getElementById("id_rline_1").disabled = true;

        document.getElementById("id_lineflux").disabled = true;
        document.getElementById("id_linewave").disabled = true;
        document.getElementById("id_linefwhm").disabled = true;
        document.getElementById("id_lineap").disabled = true;
        document.getElementById("id_contap").disabled = true;

    } else if (document.getElementById("id_iflux_0").checked == false) {
        document.getElementById("greylineflux").style.color = "black";
        document.getElementById("id_lineflux").style.color = "black";
        document.getElementById("greylinewave").style.color = "black";
        document.getElementById("id_linewave").style.color = "black";
        document.getElementById("greylineap").style.color = "black";
        document.getElementById("id_lineap").style.color = "black";
        document.getElementById("greycontap").style.color = "black";
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
        document.getElementById("greylinefwhm").style.color = "grey";
        document.getElementById("id_linefwhm").style.color = "grey";
        document.getElementById("id_linefwhm").disabled = true;
    } else if (document.getElementById("id_rline_0").checked == false) {
        document.getElementById("greylinefwhm").style.color = "black";
        document.getElementById("id_linefwhm").style.color = "black";
        document.getElementById("id_linefwhm").disabled = false;
    }

}

// -->