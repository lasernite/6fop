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

// matrix accessors
function get_element(maze, x, y) {
  return maze.maze[y][x];
}

function is_valid(solution, x, y) {
  var valid = true;

  // is x,y inside the maze?
  valid &= ((x>=0) && (x<solution.width));
  valid &= ((y>=0) && (y<solution.height));

  // is there a path from x,y to the solution?

  if (valid) {
    valid &= (get_element(solution, x, y) != "X");
  }

  return valid;
}

// Convert value matrix to one path
function find_max_path(solution, start_x, start_y, goal_x, goal_y) {
  var path = [];
  if (get_element(solution, goal_x, goal_y) != "X") {
    var x = goal_x;
    var y = goal_y;

    while ((x != start_x) || (y != start_y)) {
      path.push([x,y]);

      // is there a valid path to the left?
      var left_valid = is_valid(solution, x-1, y);
      var up_valid = is_valid(solution, x, y-1);
      if (left_valid && up_valid) {
        var left = get_element(solution, x-1, y);
        var up = get_element(solution, x, y-1);
        if (left > up) {
          x = x-1;
        } else {
          y = y-1;
        }
      } else if (left_valid) {
        x = x-1;
      } else if (up_valid) {
        y = y-1;
      } else {
        return []; // this solution is crazy wrong
      }
    }

    path.push([start_x,start_y]);
    path.reverse();
  }
  return path;
}

// Render logic
function render(state, solution) {
  clear_primitives();

  if (state == null) return;

  draw.viewbox(0, 0, state.m.width, state.m.height);
  draw.height = draw.width*state.m.height/state.m.width;

  // Draw grid
  for (var x=0; x<=state.m.width; x++){
    draw_line(x,0, x,state.m.height).stroke({ width: 0.025, color: '#000' });
  }

  for (var y=0; y<=state.m.height; y++){
    draw_line(0,y, state.m.width,y).stroke({ width: 0.025, color: '#000' });
  }

  // Draw start and goal
  draw_rect().move(state.start_x, state.start_y).size(1,1).fill({color: '#03A9F4', opacity: 0.5 });
  draw_rect().move(state.goal_x, state.goal_y).size(1,1).fill({color: '#03A9F4', opacity: 0.5 });

  var path = [];

  // Draw result if it is available
  if (solution != null) {
    // Find the max value
    var max_value = 0;
    for (var x=0; x<state.m.width; x++){
      for (var y=0; y<state.m.height; y++){
        var cell = get_element(solution, x, y);
        if (cell != "X") max_value = Math.max(max_value, cell);
      }
    }

    // Draw overlay
    for (var x=0; x<state.m.width; x++){
      for (var y=0; y<state.m.height; y++){
        var cell = get_element(solution, x, y);
        if (cell == "X") {
          draw_rect().move(x+0.1,y+0.1).size(0.8,0.8).fill({color: '#E91E63', opacity: 0.5 });
        } else {
          var value = (cell / max_value)*0.75;
          draw_rect().move(x+0.1,y+0.1).size(0.8,0.8).fill({color: '#4CAF50', opacity: value });
        }
      }
    }

    // Draw path
    path = find_max_path(solution, state.start_x, state.start_y, state.goal_x, state.goal_y);
    for (var i=1; i<path.length; i++) {
      draw_line(path[i-1][0]+0.5,path[i-1][1]+0.5, path[i][0]+0.5,path[i][1]+0.5).stroke({ width: 0.1, color: '#03A9F4', opacity: 1 });
    }
  }

  // Place grid items
  for (var x=0; x<state.m.width; x++){
    for (var y=0; y<state.m.height; y++){
      var cell = get_element(state.m, x, y);
      if (cell == 1) { // wall
        draw_rect().move(x,y).size(1,1).fill({color: '#000', opacity: 0.5 });
      } else if (cell == "c") { // coin
        draw_image("coin").move(x+0.1,y+0.1).size(0.8,0.8);
      } else if (cell == "b") { // bomb
        draw_image("bomb").move(x+0.1,y+0.1).size(0.8,0.8);
      }
    }
  }

  // Draw path
  for (var i=1; i<path.length; i++) {
    draw_line(path[i-1][0]+0.5,path[i-1][1]+0.5, path[i][0]+0.5,path[i][1]+0.5).stroke({ width: 0.1, color: '#03A9F4', opacity: 1 });
  }

  // Hide remaining cached primitives
  render_primitives();
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
  r.show();
  return r;
}

function draw_image(image) {
  var i = draw.image("/resources/"+image+".svg", 100, 100);
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
  current_test_case = test_cases[test_case_name].inputs;
  render(current_test_case, null);
}

function handle_solve() {
  // RPC to server.py to
  var solve_callback = function( solution ) {
    // print cost of best path
    var coins = get_element(solution, current_test_case.goal_x, current_test_case.goal_y);
    if (coins == "X") {
      $("#best_coins").html("Your code found no path.");
    } else {
      $("#best_coins").html("Your code suggests the best path collects " + coins + " coins!");
    }

    // Render the solution
    render(current_test_case, solution);
  };
  invoke_rpc("/run_test", { function: "solve_maze", inputs: current_test_case }, 5000, solve_callback);
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

