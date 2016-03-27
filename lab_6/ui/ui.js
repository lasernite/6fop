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

// Render logic
function draw_bag(x,y,color,orient){
  if (orient == 0){
    draw_rect().size(2.9, 0.9).radius(0.25,0.25).fill(color).move(x+0.05,y+0.05);
    draw_image('bag_fg.svg').size(3,1).move(x,y);
  } else {
    draw_rect().size(0.9, 2.9).radius(0.25,0.25).fill(color).move(x+0.05,y+0.05);
    draw_image('bag_fg.svg').size(3,1).rotate(90,x+0.5,y+0.5).move(x,y);
  }
}

function draw_rock(x,y){
  var rock_id = 1+(image_cache.length + 1)%5;
  draw_image("rock" + rock_id + ".png").move(x+0.1,y+0.1).size(0.8,0.8);
}

// [{"anchor": (x,y), "orientation": 0}, ...]
function render(state, solution) {
  clear_primitives();

  if (state == null) return;

  var width = state.tent_size[0];
  var height = state.tent_size[1];

  draw.viewbox(0, 0, width, height);
  draw.height = draw.width*height/width;

  // Draw grid
  for (var x=0; x<=width; x++){
    draw_line(x,0, x,height).stroke({ width: 0.025, color: '#9E9E9E' });
  }

  for (var y=0; y<=height; y++){
    draw_line(0,y, width,y).stroke({ width: 0.025, color: '#9E9E9E' });
  }

  if (solution != false){
    for (var i in solution){
      var bag = solution[i];
      draw_bag(bag.anchor[0], bag.anchor[1], random_color(), bag.orientation);
    }
  } else {
    draw_rect().fill("#F44336").move(0,0).size(width,height).opacity(0.25);
  }

  // Draw result if it is available
  /*
  if (solution != null) {
    // If no solution exists
    shade everything red?
    CONSTRUCT A MEESSAGE
    draw.rect(totWidth,totHeight).opacity(0.5).center(0.5*totWidth,0.5*totHeight).fill("#F44336");

    // Draw sleeping bags
    FOR EACH BAG
      IS THE BAG FULLY IN THE TENT?
      IS THE BAG PARTIALLY IN TENT?
      RENDER BAG

    // Construct message
    IF EVERYBODY IS FULLY IN THE TENT
    IF NO PACKING EXISTS
    IF N BAGS ARE PARTIALLY OUT OF THE TENT AND M ARE NOT IN THE TENT AT ALL
  }
  */

  // Place grid items
  for (var i in state.rocks){
    var rock = state.rocks[i];
    draw_rock(rock[0], rock[1]);
  }

  // Hide remaining cached primitives
  render_primitives();
}

// Color library
function random_color() {
    var colors = [
      "#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#2196F3",
      "#03A9F4", "#00BCD4", "#009688", "#4CAF50", "#8BC34A", "#CDDC39",
      "#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#795548", "#9E9E9E",
      "#607D8B"];
    return colors[~~(Math.random() * colors.length)];
}

// Render back-end library
var draw;
var rectangle_cache = [];
var rectangle_counter = 0;
var line_cache = [];
var line_counter = 0;
var image_cache = [];

function clear_primitives() {
  rectangle_counter = 0;
  line_counter = 0;

  for (var i in image_cache) {
    image_cache[i].remove();
  }
  image_cache = [];
}

function render_primitives() {
  while (rectangle_counter < rectangle_cache.length) {
    rectangle_cache[rectangle_counter].hide();
    rectangle_counter++;
  }
  while (line_counter < line_cache.length) {
    line_cache[line_counter].hide();
    line_counter++;
  }
}

function draw_rect() {
  if (rectangle_cache.length < (rectangle_counter+1)) {
    rectangle_cache.push(draw.rect(1,1));
  }
  rectangle_counter ++;
  var r = rectangle_cache[rectangle_counter-1];
  r.show().opacity(1);
  return r;
}

function draw_image(image) {
  var i = draw.image("/resources/images/"+image, 100, 100);
  image_cache.push(i);
  return i;
}

function draw_line(x0, y0, x1, y1) {
  if (line_cache.length < (line_counter+1)) {
    line_cache.push(draw.line(0,0,1,1));
  }
  line_counter ++;
  var l = line_cache[line_counter-1];
  l.plot(x0,y0, x1,y1);
  l.show();
  return l;
}

// UI button handlers
function handle_select(test_case_name) {
  // test case is already loaded in memory, simply switch to it!
  $("#current_test").html(test_case_name);
  current_test_case = test_cases[test_case_name];
  $("#lab_message").html("");
  render(current_test_case, null);
}

function handle_solve() {
  // RPC to server.py to
  var solve_callback = function( solution ) {
    // print cost of best path
    if (solution == false) {
      $("#lab_message").html("Your code found no solution.");
    } else {
      $("#lab_message").html("The tent is packed!");
    }

    // Render the solution
    render(current_test_case, solution);
  };
  invoke_rpc("/run_test", current_test_case, 5000, solve_callback);
}

// Initialization code (called when the UI is loaded)
function init() {
  draw = SVG('drawing');
  SVG.on(window, 'resize', function() { draw.spof() });

  // Load list of test cases
  var test_case_names_callback = function( test_cases_names ) {
    for (var i in test_cases_names) {
      var filename = test_cases_names[i];
      if (!(filename.match(/.*?[.]in/i))) continue;

      var test_case_callback = function( test_case ) {
        var first = Object.keys(test_cases).length == 0;
        var test_case_name = test_case.test;
        test_cases[test_case_name] = test_case;

        $("#test_cases").append(
          "<li class=\"mdl-menu__item\" onclick=\"handle_select('" +
          test_case_name +
          "')\">" +
          test_case_name +
          "</li>");

        // is it first? select it!
        if (first) handle_select(test_case.test);
      };
      invoke_rpc("/load_json", { "path": "cases/"+filename }, 0, test_case_callback);
    };
  };
  invoke_rpc("/ls", { "path": "cases/" }, 0, test_case_names_callback);
}

