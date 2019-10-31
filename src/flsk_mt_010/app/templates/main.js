function p000(){
	jsPanel.create(
		{
			closeOnEscape:true,
			theme:"primary",
			headerTitle:"test",
			position:"center-top 0 58",
			contentSize:"420 240",
			content:"",
			callback:function(panel){
				$(document).ready(
					function(){
						$.post(
							'/xas',
							JSON.stringify(
							{
								"action":"action_fractal",
								"params":{
									"width":128,
									"height":128,
									"mode":"J",
									"x_min":-2,
									"x_max":2,
									"y_min":-2,
									"y_max":2,
									"max_iterations":128,
									"color_multiplier":1,
									"c_im":-0.618,
									"c_re":0,
									"d":2,
								}
							}
	/*
		//other examples
	J 256 256 -2 2 -2 2 128 20 -0.618 0 2
	J 256 256 -2 2 -2 2 128 1 -0.4 0.6 2
	J 256 256 -2 2 -2 2 128 20 -0.4 0.6 3
	J 256 256 -2 2 -2 2 128 1 -0.8 0.156 2
	M 256 256 -2.5 1.5 -2 2 128 20 2
	M 256 256 -2 2 -2 2 128 20 3
	M 256 256 -2 2 -2 2 128 20 4
	M 256 256 -2 2 -2 2 128 20 6
	*/
						),
						function(d){
							var data=d.data;
							for(var row=0;row<data.length;row++){
								for(var col=0;col<data[row].length;col++){
									/*
									if(
										data[row][col]>128
									){
										data[row][col]=0;
										//data[row][col]=data[row][col]%24;
									}else{
										if(
											data[row][col]>96
										){
											data[row][col]=18;
										}else{
											data[row][col]=15;
										}
									}
									*/
									data[row][col]%=24;
								}
							}
							/*
							*/
							var level=data;
							const config = {
								type: Phaser.AUTO, // Which renderer to use
								width: 800, // Canvas width in pixels
								height: 600, // Canvas height in pixels
								parent: panel.content,//"game-container", // ID of the DOM element to add the canvas to
								scene: {
									preload: preload,
									create: create,
									update: update
								},
							};
							const game = new Phaser.Game(config);
							panel.game=game;
							function preload() {
								  // Runs once, loads up assets like images and audio
								this.load.image("mario-tiles", "assets/spritesheets/mario.png");
							}
							var level=data;
							var tiles=null;
							var map=null;
							var layer=null;
							var camera;
							function create() {
								// When loading from an array, make sure to specify the tileWidth and tileHeight
								map = this.make.tilemap({ data: level, tileWidth: 16, tileHeight: 16 });
								tiles = map.addTilesetImage("mario-tiles");
								layer = map.createStaticLayer(0, tiles, 0, 0);
								// Phaser supports multiple cameras, but you can access the default camera like this:
								camera = this.cameras.main;
								// Set up the arrows to control the camera
								const cursors = this.input.keyboard.createCursorKeys();
								controls = new Phaser.Cameras.Controls.FixedKeyControl({
									camera: camera,
									left: cursors.left,
									right: cursors.right,
									up: cursors.up,
									down: cursors.down,
									speed: 0.5
								});
								//Constrain the camera so that it isn't allowed to move outside the width/height of tilemap
								camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
								this.cameras.main.removeBounds()
							}
							var syncing=false;
							function update(time, delta) {
								controls.update(delta);
							}
						},
						'json'
					);
				}
			)	
		},
		onbeforeclose:function(panel){
			panel.game.destroy();
			return true;
		}

	}
	);
};
function p001(){
	jsPanel.create(
		{
			closeOnEscape:true,
			theme:"primary",
			headerTitle:"test",
			position:"center-top 0 58",
			contentSize:"420 240",
			content:"",
			callback:function(panel){


				$(document).ready(
					function(){
						$.post(
							'/xas',
							JSON.stringify({
								"action":"action_perlin",
								"params":{
									"width":512,
									"height":64,
									"seed":Math.floor(8*Math.random()),
									"gridsize":24//32
								}
							}),
							function(d){
								var data=d.data;
								for(var row=0;row<data.length;row++){
									for(var col=0;col<data[row].length;col++){
										if(
											data[row][col]>128
										){
											data[row][col]=0;
											//data[row][col]=data[row][col]%24;
										}else{
											if(
												data[row][col]>96
											){
												data[row][col]=18;
											}else{
												data[row][col]=15;
											}
										}
									}
								}
								/*
								*/
								var level=data;
								const config = {
									type: Phaser.AUTO, // Which renderer to use
									width: 800, // Canvas width in pixels
									height: 600, // Canvas height in pixels
									parent: panel.content,//"game-container", // ID of the DOM element to add the canvas to
									scene: {
										preload: preload,
										create: create,
										update: update
									},
								};
								const game = new Phaser.Game(config);
								panel.game=game;
								function preload() {
									  // Runs once, loads up assets like images and audio
									this.load.image("mario-tiles", "assets/spritesheets/mario.png");
								}
								var level=data;
								var tiles=null;
								var map=null;
								var layer=null;
								var camera;
								function create() {
									// When loading from an array, make sure to specify the tileWidth and tileHeight
									map = this.make.tilemap({ data: level, tileWidth: 16, tileHeight: 16 });
									tiles = map.addTilesetImage("mario-tiles");
									layer = map.createStaticLayer(0, tiles, 0, 0);


					// Phaser supports multiple cameras, but you can access the default camera like this:
					camera = this.cameras.main;
					// Set up the arrows to control the camera
					const cursors = this.input.keyboard.createCursorKeys();
					controls = new Phaser.Cameras.Controls.FixedKeyControl({
						camera: camera,
						left: cursors.left,
						right: cursors.right,
						up: cursors.up,
						down: cursors.down,
						speed: 0.5
					});
					//Constrain the camera so that it isn't allowed to move outside the width/height of tilemap
					camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

					this.cameras.main.removeBounds()





								}
								var syncing=false;
								function update(time, delta) {
									controls.update(delta);
								}
							},
							'json'
						);
					}
				)


			},
			onbeforeclose:function(panel){
				panel.game.destroy();
				return true;
			}
		}
	);
}
function p002(){
	jsPanel.create(
		{
			closeOnEscape:true,
			theme:"primary",
			headerTitle:"test",
			position:"center-top 0 58",
			contentSize:"420 240",
			content:"",
			callback:function(panel){
				$(document).ready(
					function(){
						$.post(
							'/xas',
							JSON.stringify({
								"action":"action_sine",
								"params":{
									"width":512,
									"height":48
								}
							}),
							function(d){
								var data=d.data;
								/*
								for(var row=0;row<data.length;row++){
									for(var col=0;col<data[row].length;col++){
										if(
											data[row][col]>128
										){
											data[row][col]=0;
											//data[row][col]=data[row][col]%24;
										}else{
											if(
												data[row][col]>96
											){
												data[row][col]=18;
											}else{
												data[row][col]=15;
											}
										}
									}
								}
								*/
								var level=data;
								const config = {
									type: Phaser.AUTO, // Which renderer to use
									width: 800, // Canvas width in pixels
									height: 600, // Canvas height in pixels
									parent: panel.content,//"game-container", // ID of the DOM element to add the canvas to
									scene: {
										preload: preload,
										create: create,
										update: update
									},
								};
								const game = new Phaser.Game(config);
								panel.game=game;
								function preload() {
									  // Runs once, loads up assets like images and audio
									this.load.image("mario-tiles", "assets/spritesheets/mario.png");
								}
								var level=data;
								var tiles=null;
								var map=null;
								var layer=null;
								var camera;
								function create() {
									// When loading from an array, make sure to specify the tileWidth and tileHeight
									map = this.make.tilemap({ data: level, tileWidth: 16, tileHeight: 16 });
									tiles = map.addTilesetImage("mario-tiles");
									layer = map.createStaticLayer(0, tiles, 0, 0);


					// Phaser supports multiple cameras, but you can access the default camera like this:
					camera = this.cameras.main;
					// Set up the arrows to control the camera
					const cursors = this.input.keyboard.createCursorKeys();
					controls = new Phaser.Cameras.Controls.FixedKeyControl({
						camera: camera,
						left: cursors.left,
						right: cursors.right,
						up: cursors.up,
						down: cursors.down,
						speed: 0.5
					});
					//Constrain the camera so that it isn't allowed to move outside the width/height of tilemap
					camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

					this.cameras.main.removeBounds()





								}
								var syncing=false;
								function update(time, delta) {
									controls.update(delta);
								}
							},
							'json'
						);
					}
				)
			},
			onbeforeclose:function(panel){
				panel.game.destroy();
				return true;
			}
		}
	);
}
var session=null;
function createSession(){
    $(document).ready(
      function(){
	$.post(
	  '/xas',
	  JSON.stringify(
	    {
	      "action":"get_session_data",
	      "params":{
	      }
	    }
	  ),
	  function(d){
		session=d;
		$.toast('Session Created ['+d.token+']')
		console.log(d);
	  },
	  'json'
	);
      }
    );
}
function removeSession(){
    $(document).ready(
      function(){
	$.post(
	  '/xas',
	  JSON.stringify(
	    {
	      "action":"remove_session",
		"data":{}
	    }
	  ),
	  function(d){
		  if(d.data){
			  $.toast(d.data)
		  }else if(d.error){
			  $.toast(d.error)
		  }else{
			  $.toast('error');
		  }
		console.log(d);
	  },
	  'json'
	);
      }
    );
}
function terminal(){
	$(function() {
		//$('#terminal');
		jsPanel.create(
			{
				closeOnEscape:true,
				theme:"dark",
				headerTitle:"Terminal",
				position:"center-top 0 58",
				contentSize:"420 240",
				callback:function(panel){
					//style
					panel.term=$(panel).find('.jsPanel-content').terminal(
function(command,term){
	console.log(command);
	if(command=="login"){
		term.pause();
		$.post(
		  '/xas',
		  JSON.stringify(
		    {
		      "action":"get_session_data",
		      "params":{
		      }
		    }
		  ),
		  'json'
		).then(
			function(response){
				term.resume();
				term.echo(JSON.stringify(response));
			}
		);
	}else if(command=="logout"){
		term.pause();
		$.post(
		  '/xas',
		  JSON.stringify(
		    {
		      "action":"remove_session",
		      "params":{
		      }
		    }
		  ),
		  'json'
		).then(
			function(response){
				term.resume();
				term.echo(JSON.stringify(response));
			}
		);
	}else if(command.startsWith("ls ")){
		var arg=command.substring(3);
		term.pause();
		$.post(
		  '/xas',
		  JSON.stringify(
		    {
		      "action":"readdir",
		      "params":{
			      "path":arg
		      }
		    }
		  ),
		  'json'
		).then(
			function(response){
				term.resume();
				term.echo(JSON.stringify(response));
			}
		);
	}else if(command=="exit"){
		//term.destroy();
		panel.close();
	}else if(command.startsWith("js ")){
		alert('a');
		eval(command.substring(3));
	}else if(command=="fractal"){
		term.pause();
		$.post(
		  '/xas',
		  JSON.stringify(
			{"action":"action_fractal","params":{"width":8,"height":8,"mode":"J","x_min":-2,"x_max":2,"y_min":-2,"y_max":2,"max_iterations":128,"color_multiplier":1,"c_im":-0.618,"c_re":0,"d":2}}
		  ),
		  'json'
		).then(
			function(response){
				term.resume();
				term.echo(response);
			}
		);
	}else{
		return "Invalid command";
	}
},
{
	greetings:"Mongoose OS",
	prompt: 'mg> '
}
					);
					//style
					$(panel).find('.jsPanel-content').css("background","#000000");
					$(panel).find('.jsPanel-content').css("width","100%");
				},
				onbeforeclose:function(panel){
					panel.term.destroy();
					return true;
				}
			}
		)


	});
}
//-----------------------------------------------------------------------------
//jstree example
//-----------------------------------------------------------------------------
function treeajax(path){
	$.post(
	  '/xas',
	  JSON.stringify(
	    {
	      "action":"action_readdir",
	      "params":{
		      "path":path
	      }
	    }
	  ),
	  'json'
	).then(
		function(response){
			if(response.error==null){
				jsPanel.create(
					{
						closeOnEscape:true,
						theme:"dark",
						headerTitle:"JsTree",
						position:"center-top 0 58",
						contentSize:"420 240",
						callback:function(panel){
							var data=response;
							panel.tree=$(panel)
								.find('.jsPanel-content')
								.jstree(
									{
										'core':{
											"themes": {
												"name": "default-dark",
												"dots": true,
												"icons": true
											},
											'data' : data
										}
									}
								);
							$(panel).find('.jsPanel-content').css("background","#444444");
							$(panel).find('.jsPanel-content').css("width","100%");
						},
						onbeforeclose:function(panel){
							//panel.term.destroy();
							return true;
						}
					}
				);
			}else{
				$.toast(JSON.stringify(response));
			}
		}
	)
}
/*
// example lazyloading ajax
$('#TreeDiv')
.jstree(
	{
		core: {
			data: {
				url:function(node){
					return node.id==='#'?'/UserAccount/AccountGroupPermissions'
					: '/UserAccount/AccountPermissions/' + node.id
				},
				type: 'POST'
			}
		},
		plugins : ["checkbox"]
	}
);

 */
//-----------------------------------------------------------------------------
//data tables example
//-----------------------------------------------------------------------------
function dtajax(w,h){
	$.post(
		'/xas',
		JSON.stringify(
			{
				"action":"action_dttest",
				"params":{
					"width":w,
					"height":h
				}
			}
		),
		'json'
	).then(
		function(response){
			if(response.error==null){
				jsPanel.create(
					{
						closeOnEscape:true,
						theme:"dark",
						headerTitle:"DataTables Example",
						position:"center-top 0 58",
						contentSize:"420 240",
						callback:function(panel){
							$(panel)
							.find('.jsPanel-content')
							.html(
								'<table id="example" class="table table-striped table-bordered" cellspacing="0" width="100%"></table>'
							);
							$(panel)
							.find('#example')
							.DataTable(
								{
									data: response.data,
									columns: response.columns
								}
							);
						},
						onbeforeclose:function(panel){
							return true;
						}
					}
				)
			}else{
				$.toast(JSON.stringify(response));
			}

		}
	);
}
//-----------------------------------------------------------------------------
//ace editor
//-----------------------------------------------------------------------------
function edit(path){
	if(path==null){
		  $.toast("No path specified")
	}else{
		$.post(
		  '/xas',
		  JSON.stringify(
		    {
			"action":"_fread",
			"params":{
				"path":path,
				"size":1024
			}
		    }
		  ),
		  function(d){
			if(d.data){
				jsPanel.create(
					{
						closeOnEscape:true,
						theme:"primary",
						headerTitle:"Editor",
						position:"center-top 0 0",
						contentSize:"100% 200px",
						callback:function(panel){
							var content=$(panel)
							.find('.jsPanel-content')
							.html("<div></div>")
							var editor=ace.edit(
								content[0]
							);
							editor
							.setTheme(
								"ace/theme/light"
							);
							editor
							.getSession()
							//.setMode(
							//	"ace/mode/javascript"
							//);
							editor.setValue(
				  				d.data
							);
							editor.focus();
						},
						onbeforeclose:function(panel){
							//panel.term.destroy();
							return true;
						}
					}
				);

			}else if(d.error){
				  $.toast(d.error)
			}else{
				  $.toast(JSON.stringify(d));
			}
			console.log(d);
		  },
		  'json'
		);
	}
}
//-----------------------------------------------------------------------------
//babylonjs
//-----------------------------------------------------------------------------
function bab(){
	jsPanel.create(
		{
			closeOnEscape:true,
			theme:"dark",
			headerTitle:"Babylon",
			position:"center-top 10 10",
			contentSize:"480px 320px",
			callback:function(panel){
				$(panel)
				.find('.jsPanel-content')
				.html('<canvas class="renderCanvas" id="renderCanvas"></canvas>');
				//var canvas = document.getElementById("renderCanvas");
				var canvas=$(panel)
					.find('.jsPanel-content')
					.find('#renderCanvas')[0];
				var engine = new BABYLON.Engine(canvas, true);
				var createScene = function () {
					// This creates a basic Babylon Scene object (non-mesh)
					var scene = new BABYLON.Scene(engine);
					// This creates and positions a free camera (non-mesh)
					var camera = new BABYLON.FreeCamera("camera1", new BABYLON.Vector3(0, 5, -10), scene);
					// This targets the camera to scene origin
					camera.setTarget(BABYLON.Vector3.Zero());
					// This attaches the camera to the canvas
					camera.attachControl(canvas, true);
					// This creates a light, aiming 0,1,0 - to the sky (non-mesh)
					var light = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(0, 1, 0), scene);
					// Default intensity is 1. Let's dim the light a small amount
					light.intensity = 0.7;
					// Our built-in 'sphere' shape. Params: name, subdivs, size, scene
					// lod tex
					var myMaterial=new BABYLON.StandardMaterial('myMaterial',scene);
					var tex=new BABYLON.Texture('/test',scene);
					myMaterial.diffuseTexture=tex;
					myMaterial.specularTexture=tex;
					myMaterial.emissiveTexture=tex;
					myMaterial.ambientTexture=tex;
					var sphere = BABYLON.Mesh.CreateSphere("sphere1", 16, 2, scene);
					sphere.material=myMaterial;//set mat
					// Move the sphere upward 1/2 its height
					sphere.position.y = 1;
					// Our built-in 'ground' shape. Params: name, width, depth, subdivs, scene
					//var ground = BABYLON.Mesh.CreateGround("ground1", 6, 6, 2, scene);
					scene.clearColor=new BABYLON.Color3(0,0,0);
					$.toast('Scene created');
					return scene;
				};
				var scene = createScene()
				panel.scene=scene;
				engine.runRenderLoop(
					function () {
						if(scene){
							scene.render();
						}
					}
				);
				// Resize
				window.addEventListener(
					"resize",
					function(){
						engine.resize();
					}
				);
				canvas.addEventListener(
					"resize",
					function(){
						engine.resize();
					}
				);
			},
			onbeforeclose:function(panel){
				panel.scene.dispose();
				$.toast('Scene destroyed');
				return true;
			}
		}
	);

}
//------------------------------------------------------------------------------
String.prototype.strip = function(char) {
	return this.replace(new RegExp("^" + char + "*"), '').
	replace(new RegExp(char + "*$"), '');
}
$.extend_if_has = function(desc, source, array) {
	for (var i=array.length;i--;) {
		if (typeof source[array[i]] != 'undefined') {
			desc[array[i]] = source[array[i]];
		}
	}
	return desc;
};
//------------------------------------------------------------------------------
//quake style terminal
//------------------------------------------------------------------------------
$(document).ready(
	function(){
$.fn.tilda=
	$.proxy(
	function(_eval, options){
		if ($('body').data('tilda')) {
		    return $('body').data('tilda').terminal;
		}
		this.addClass('tilda');
		options = options || {};
		_eval=function(command,term){
			if(command=="login"){
				term.pause();
				$.post(
				  '/xas',
				  JSON.stringify(
				    {
				      "action":"get_session_data",
				      "params":{
				      }
				    }
				  ),
				  'json'
				).then(
					function(response){
						term.resume();
						term.echo(JSON.stringify(response));
					}
				);
			}else if(command=="logout"){
				term.pause();
				$.post(
				  '/xas',
				  JSON.stringify(
				    {
				      "action":"remove_session",
				      "params":{
				      }
				    }
				  ),
				  'json'
				).then(
					function(response){
						term.resume();
						term.echo(JSON.stringify(response));
					}
				);
			}else if(command.startsWith("ls ")){
				var arg=command.substring(3);
				term.pause();
				$.post(
				  '/xas',
				  JSON.stringify(
				    {
				      "action":"action_readdir",
				      "params":{
					      "path":arg
				      }
				    }
				  ),
				  'json'
				).then(
					function(response){
						term.resume();
						term.echo(JSON.stringify(response));
					}
				);
			}else if(command.startsWith("ex ")){
				var action=command.substring(3);
				var params={};
				if(
					action.indexOf(" ")>0
				){
					params=JSON.parse(
						action.substring(
							action.indexOf(
								" "
							)+1
						)
					);
					action=
					 action.substring(
						0,
						action.indexOf(
							" "
						)
					);
				}
				term.pause();
				$.post(
				  '/xas',
				  JSON.stringify(
				    {
				      "action":action,
				      "params":params
				    }
				  ),
				  'json'
				).then(
					function(response){
						term.resume();
						term.echo(JSON.stringify(response));
					}
				);
			}else if(command=="exit"){
				//term.destroy();
				panel.close();
			}else if(command.startsWith("js ")){
				eval(command.substring(3));
			}else if(command=="fractal"){
				term.pause();
				$.post(
				  '/xas',
				  JSON.stringify(
					{"action":"action_fractal","params":{"width":8,"height":8,"mode":"J","x_min":-2,"x_max":2,"y_min":-2,"y_max":2,"max_iterations":128,"color_multiplier":1,"c_im":-0.618,"c_re":0,"d":2}}
				  ),
				  'json'
				).then(
					function(response){
						term.resume();
						term.echo(response);
					}
				);
			}else{
				return "Invalid command";
			}
		};
		var settings = {
		    prompt: 'tilda> ',
		    name: 'tilda',
		    height: 300,
		    opacity: '50%',
		    enabled: false,
		    greetings: 'Quake like console',
		    keypress: function(e) {
			if (e.which == 96) {
			    return false;
			}
		    }
		};
		if (options) {
		    $.extend(settings, options);
		}
		this.append('<div class="td"></div>');
		var self = this;
		//self.terminal = this.find('.td').terminal(_eval, settings);
		self.terminal = this.find('.td').terminal(_eval,settings);
		var focus = false;
		$(document.documentElement).keypress(function(e) {
		    if (e.which == 96) {
			self.slideToggle('fast');
			self.terminal.focus(focus = !focus);
			self.terminal.attr({
			    scrollTop: self.terminal.attr("scrollHeight")
			});
		    }
		});
		$('body').data('tilda', this);
		this.hide();
		return self;
    },//this
);
//--------------------------------------------------------------------------
$('#tilda').tilda(
	function(command, terminal){
		//terminal.echo('you type command "' + command + '"');
	}
);
	}
);
//--------------------------------------------------------------------------------

