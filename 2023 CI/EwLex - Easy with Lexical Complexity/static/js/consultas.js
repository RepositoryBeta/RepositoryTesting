function getTextoConsultas(IdConsulta) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/texto_consulta",
    data: "IdConsulta=" + IdConsulta,
    success: function (response) {
      if (response) {
        $("#IdTgresado").val(response);
      }
      $("#IdTgresado").text("");
      getPalabrasEncontradas(IdConsulta)
    },
  });
  $("#modal-pconsultas").modal("show");
}
function getPalabrasEncontradas(IdConsulta) {
  var html = "";
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/palabras_encontradas",
    data: "IdConsulta=" + IdConsulta,
    beforeSend: function () {
      $(".loader_imagen").show();
    },
    success: function (response) {
      $(".loader_imagen").hide();
      if (response) {
        al = 0;
        $.each(response, function (i, item) {
          al = al + 1;
          html +=
            '<a class="btn btn-outline-info" href="#" onclick="getBuscarSinonimosConsulta(' +
            item[0] +
            ');" title="Buscar"><i class="fa fa-search"';
          html += 'aria-hidden="true"></i> ' + item[1] + "</a>&nbsp;";
          $("#IdPalabras").html(html);
        });
        $("#NroPalabras").text(al);
      }
      if (response == "null") {
        window.location.href = "/";
      }
    },
  });
}
function getBuscarPalabraSeleccionada(idp){
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_palabra",
    data: "IdPalabra=" + idp,
    success: function (response) {
      if (response) {
        $("#IdPalabraSnm").text(" " + response[0]);
        $("#IdPalabraDf").text(" " + response[0]);
      }
      $("#sinonimos").text("");
      $("#definiciones").text("");
    },
  });
}
function getBuscarSinonimosConsulta(idp){
  getBuscarPalabraSeleccionada(idp)
  var html = "";
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_sinonimos_consulta",
    data: "IdPalabra=" + idp,
    beforeSend: function () {
			$('.loader_imagen').show();
		},
    success: function (response) {
      $('.loader_imagen').hide();
      if (response) {
        $.each(response, function (i, item) {
          html += '<cite style="color: green;"> | '+item+'</cite>';
          $("#sinonimos").html(html);
          $("#IdSinonim").text(item[1]);
        });
        getBuscarDeficicionesConsultadas(idp)
      }
      else {
        alert(response);
        window.location.href = "/";
      }
    },
  });
}
function getBuscarDeficicionesConsultadas(idp){
  var html = "";
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_deficiciones_consulta",
    data: "IdPalabra=" + idp,
    beforeSend: function () {
			$('.loader_imagen').show();
		},
    success: function (response) {
      $('.loader_imagen').hide();
      if (response) {
        $.each(response, function (i, item) {
          html += '<cite style="color: blue;"> | '+item+'</cite>';
          $("#definiciones").html(html);
        });
      }
      else {
        alert(response);
        window.location.href = "/";
      }
    },
  });
}
function getBuscarConsultas(){
  var html = "";
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_consultas",
    beforeSend: function () {
			$('.loader_imagen').show();
		},
    success: function (response) {
      $('.loader_imagen').hide();
      if (response) {
        alert(response);
        $.each(response, function (i, item) {
          alert(item);
          //html += '<cite style="color: blue;"> | '+item+'</cite>';
          //$("#definiciones").html(html);
        });
      }
      else {
        alert(response);
        window.location.href = "/";
      }
    },
  });
}
$(document).ready(function () {
	//$('.loader_imagen').hide();
  //getBuscarConsultas();
});
