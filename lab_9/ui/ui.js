"use strict";

// RPC wrapper
function invoke_rpc(method, args, timeout, on_done){
  $("#crash").hide();
  $("#timeout").hide();
  $("#rpc_spinner").show();
  //send RPC with whatever data is appropriate. Display an error message on crash or timeout
  var xhr = new XMLHttpRequest();
  xhr.open("POST", method, true);
  xhr.setRequestHeader('Content-Type','application/json; charset=UTF-8');
  xhr.timeout = timeout;
  xhr.send(JSON.stringify(args));
  xhr.ontimeout = function () {
    $("#timeout").show();
    $("#rpc_spinner").hide();
    $("#crash").hide();
  };
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      $("#rpc_spinner").hide();
      var result = JSON.parse(xhr.responseText)
      $("#timeout").hide();
      if (typeof(on_done) != "undefined"){
        on_done(result);
      }
    } else {
      $("#crash").show();
    }
  }
}

// Resource load wrapper
function load_resource(name, on_done) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", name, true);
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      on_done(result);
    }
  }
  xhr.send();
}

// Code that runs first
$(document).ready(function(){
  restart();
  init();
});

function restart(){
  invoke_rpc( "/restart", {} )
}

//  LAB CODE

// this is inlined into infra/ui/ui.js

function on_done(result_tuple){
  // Show label
  $("#running").hide();
  $("#crash").hide();
  $("#timeout").hide();

  var printout = result_tuple[0];
  var result = result_tuple[1];
  var player = result_tuple[2];

  result = result.replace(/ /g, "&emsp;");
  result = result.replace(/\{/g, '<span class="special">');
  result = result.replace(/\}/g, "</span>");
  var strings = result.split("\n");

  if (printout != null){
    $("#log").append('<p class="special">' + printout + "</p>");
  }

  for (var i in strings){
    var text = strings[i];
    $("#log").append("<p>"+text+"<p>");
  }

  $("#log").append('<p class="result">(' + player + ", it's your turn!)</p>");

  $("#input").val("");
  $("#user_input").show();
}

function init(){
  $("#log").empty();

  $("#crash").hide();
  $("#timeout").hide();
  $("#running").show();
  $("#user_input").hide();

  invoke_rpc("/ui_init", {}, 500, on_done);
}

function handle_init(){
  init();
}

$("#input").keyup(function(event){
    if(event.keyCode == 13){
      on_input($("#input").val());
    }
});

function on_input(input){
  if (input === undefined) { input = ""; }

  $("#log").append('<p class="input">&gt; '+input+"<p>");

  $("#crash").hide();
  $("#timeout").hide();
  $("#running").show();
  $("#user_input").hide();

  // Run student algorithm
  var args = {
    "input": input
  };
  invoke_rpc("/ui_handle_input", args, 500, on_done );
}

