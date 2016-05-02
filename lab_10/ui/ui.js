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

// State
var test_cases = {};
var current_test_case = null;

var draw;
var startspeed = 80;
var step_time = 0.1;
var paddle_speed = 10;
var paddles = [0, 0];
var timeout = 500;
var frame_rate_cap = 30;

function render(primitives){
  //window.console.log(primitives);
  render_circles(primitives.circles);
  render_rectangles(primitives.rectangles);
}

var circle_cache = [];
var rectangle_cache = [];

function render_circles(C){
  var i = 0;
  // for each circle in circles, grab next from cache (create if needed)
  for (var i in C){
    if (circle_cache.length < (i+1)) {
      circle_cache.push(draw.circle(1));
    }
    circle_cache[i].radius(C[i][2]).center(C[i][0], C[i][1]).fill(C[i][3]).show();
  }

  i = C.length

  while (i < circle_cache.length){
    circle_cache[i].hide();
    i++;
  }
}

function render_rectangles(R){
  var i = 0;
  // for each circle in circles, grab next from cache (create if needed)
  for (var i in R){
    if (rectangle_cache.length < (i+1)) {
      rectangle_cache.push(draw.rect(1,1));
    }
    rectangle_cache[i].width(R[i][2]-R[i][0]).height(R[i][3]-R[i][1]).move(R[i][0],R[i][1]).fill(R[i][4]).show();
  }

  i = R.length
  while (i < rectangle_cache.length){
    rectangle_cache[i].hide();
    i++;
  }
}

function on_restart(){
  $("#crash").hide();
  $("#timeout").hide();

  simulation_flag = true;
  adjust_score();

  draw.viewbox(0, 0, initial_state.width, initial_state.height);
  draw.width = initial_state.width;
  draw.height = initial_state.height;
  SVG.on(window, 'resize', function() { draw.spof() });
  $("#drawing").width(initial_state.width+"px");
  $("#drawing").height(initial_state.height+"px");

  // Run student algorith
  paddles = [initial_state.paddle1X, initial_state.paddle2X];

  var args = {
    "width": initial_state.width,
    "height": initial_state.height,
    "ball_position": initial_state.ballPosition,
    "ball_velosity": initial_state.ballVelocity,
    "blocks": initial_state.blocks
  };
  invoke_rpc("/init", args, 0, function(){ simulate(); } );
}

function naturalCompare(a, b) {
    var ax = [], bx = [];

    a.replace(/(\d+)|(\D+)/g, function(_, $1, $2) { ax.push([$1 || Infinity, $2 || ""]) });
    b.replace(/(\d+)|(\D+)/g, function(_, $1, $2) { bx.push([$1 || Infinity, $2 || ""]) });

    while(ax.length && bx.length) {
        var an = ax.shift();
        var bn = bx.shift();
        var nn = (an[0] - bn[0]) || an[1].localeCompare(bn[1]);
        if(nn) return nn;
    }

    return ax.length - bx.length;
}


function init(){
  var height_multiplier = 2;

  // Initialize SVG drawing
  draw = SVG('drawing');
  SVG.on(window, 'resize', function() { draw.spof() });

  // Load test cases
  var test_case_names_callback = function( test_cases_names ) {
    test_cases_names = test_cases_names.sort(function(a,b){ return parseInt(a.substring(0,2))-parseInt(b.substring(0,2))});

    var test_case_barrier = function(){
      if ((test_cases_names.length/2) == Object.keys(test_cases).length){
        var names = Object.keys(test_cases);
        names = names.sort(function(a,b){ return parseInt(a.substring(0,2))-parseInt(b.substring(0,2))});

        for (var i in names){
          var test_case_name = names[i];

          var test_case = test_cases[test_case_name];
          var test_case_name = test_case.test;

          $("#initial_states").append(
            "<li class=\"mdl-menu__item\" onclick=\"handle_select('" +
            test_case_name +
            "')\">" +
            test_case_name +
            "</li>");
        }

        handle_select(names[0]);
      }
    }

    for (var i in test_cases_names) {
      var filename = test_cases_names[i];
      if (!(filename.match(/.*?[.]in/i))) continue;

      var test_case_callback = function( test_case ) {
        var first = Object.keys(test_cases).length == 0;
        var test_case_name = test_case.test;
        test_cases[test_case_name] = test_case;
        test_case_barrier();
      };
      invoke_rpc("/load_json", { "path": "cases/"+filename }, 0, test_case_callback);
    };
  };
  invoke_rpc("/ls", { "path": "cases/" }, 0, test_case_names_callback);
}

var simulation_flag;
function on_stop(){
  simulation_flag = false;
  simulate();
}

var scores;
function adjust_score(val) {
  if (typeof val === 'undefined'){
    scores = [0,0];
    $('#p1_score').text(scores[0]);
    $('#p2_score').text(scores[1]);
  }

  if (val > 0) {
    scores[0]++;
    $('#p1_score').text(scores[0]);
  } else if (val < 0) {
    scores[1]++;
    $('#p2_score').text(scores[1]);
  }
}

var initial_state = null;


// UI button handlers
function handle_select(test_case_name) {
  // test case is already loaded in memory, simply switch to it!
  $("#current_state").html(test_case_name);
  current_test_case = test_cases[test_case_name];
  initial_state = test_cases[test_case_name];
  on_restart();
}

// Game loop is tied to RPCs
var previous_time = new Date().getTime();

function simulate() {
  // force wait if game is running too fast
  var new_time = new Date().getTime();
  if ((new_time - previous_time) < 1000/frame_rate_cap){
    if (simulation_flag){
      window.setTimeout(simulate, (1000/frame_rate_cap)-(new_time-previous_time));
    }
    return;
  }
  previous_time = new Date().getTime();

  // Adjust paddle positions
  var p1_offset = (p1_input[0] & !p1_input[1])? -paddle_speed : (!p1_input[0] & p1_input[1])? paddle_speed : 0;
  paddles[0] += p1_offset;
  paddles[0] = Math.min(initial_state.width, Math.max(0, paddles[0]));

  var p2_offset = (p2_input[0] & !p2_input[1])? -paddle_speed : (!p2_input[0] & p2_input[1])? paddle_speed : 0;
  paddles[1] += p2_offset;
  paddles[1] = Math.min(initial_state.width, Math.max(0, paddles[1]));

  // Issue RPC to update and draw on success
  var args = {
    "time": step_time,
    "paddle_1_xpos": paddles[0],
    "paddle_2_xpos": paddles[1],
    "paddle_offset": initial_state.paddle_offset,
    "paddle_radius": initial_state.paddle_radius
  };
  invoke_rpc( "/step",
              args,
              1000,
              function(result){
                adjust_score(result);
                invoke_rpc (  "/draw",
                              args,
                              200,
                              function(result){
                                // render
                                render(result);
                                // check if it is time for the  next frame
                                simulate();
                              } );
              } );
}

// Input
var p1_input = [false, false];
var p2_input = [false, false];

$('html').keydown(function(e){
  if (e.which == 37) { p1_input[0] = true; } // left arrow
  if (e.which == 39) { p1_input[1] = true; }  // right arrow
  if (e.which == 65) { p2_input[0] = true; } // A
  if (e.which == 68) { p2_input[1] = true; }  //D
});

$('html').keyup(function(e){
  if (e.which == 37) { p1_input[0] = false; } // left arrow
  if (e.which == 39) { p1_input[1] = false; }  // right arrow
  if (e.which == 65) { p2_input[0] = false; } // A
  if (e.which == 68) { p2_input[1] = false; }  //D
});

function on_p1_input(offset){
  //window.console.log("P1: " + offset);
  p1_offset = offset;
}

function on_p2_input(offset){
  //window.console.log("P2: " + offset);
  p2_offset = offset;
}

