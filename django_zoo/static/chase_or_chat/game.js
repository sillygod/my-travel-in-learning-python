(function($){

    $.fn.gameProc = function(){
        // extend the jquery library's function

        $(this).attr('tabindex', '0');
        // set this element to be able being captured by tab
        $(this).focus();

        Canvas($(this));


    };



    function Point(x, y){
        this.x = x;
        this.y = y;
    }

    function createPts(w, h, wlength, hlength){
        var lst = [];

        for(var j=0; j<h; j++){
            for(var i=0; i<w; i++){
                lst.push({'x': i*wlength, 'y': j*hlength})
            }
        }

        return lst;
    }


    function Timer(settings) {
        // create a timer for a game loop..
        // it seems that using a infinite loop will cause a
        // crack down or no response

        this.callback = settings.callback;
        this.timer = null;

        this.fps = settings.fps || 30;
        this.timeInit = null;

    }


    Timer.prototype = {

        run: function()
        {
            // store the this, due to the lost of this you want,
            // when you call this function by setTimeout
            var $this = this;

            this.callback();
            
            // In my opinion, using interval is better than settimeout
            // due to the cancel timer..
            // you need to check the timer id carefully to cancel it
            // by settimeout
            this.timer = setInterval(this.callback, 1000/this.fps);
            
        },

        start: function()
        {
            if(this.timer === null)
            {
                //performance.now
                this.timeInit = performance.now();
                this.run();
            }
        },

        stop: function()
        {
            clearTimeout(this.timer);
            this.timer = null;
        }
    };


    function Canvas(canvas)
    {
        // canvas is a jQuery object which select the dom canvas
        var domCanvas = canvas[0]; //get the dom object
        var jCanvas = canvas;

        //console.log(jCanvas.attr('width')+' '+jCanvas.attr('height'));
        var backBuffer = new BackBuffer(domCanvas, jCanvas.attr('width'), jCanvas.attr('height'));

        var bg = new Sprite('./bg.png');
        var skill = new animateSprite(backBuffer);
        var character = new animateSprite(backBuffer);


        character.setframes('./Evil.png', 'Evil');
        skill.setframes('./Special1.png', 'Special1');
        skill.setWidthandHeight({'width':192, 'height': 192});


        var resLoader = new ResourceLoader();

        resLoader.push(bg);
        resLoader.push(skill);


        var gameloop = new Timer({
          callback: function(){
                bg.draw(backBuffer.getDC());
                skill.draw();
                backBuffer.present();

          }
        });

        resLoader.init(gameloop);


        jCanvas.on("keydown", function(event){
            event.preventDefault(); //prevent other events
            console.log(event.type+' '+event.which);

            if(event.which == 13){
                skill.play();
            }

        });







        //now, consider should it have a gameloop here
        //in javascript, it has a asynchronous loop already, hasn't it?
        //maybe, it need a loop for drawing, but how about control?
    }





    function getMousePos(canvas, event){
    // calculate the relative pos to the canvas
    // the event will return  global pos
    // rect get the pos of canvas of the viewport

        var rect = canvas.getBoundingClientRect();
        var root = document.documentElement;


        console.log(event.clientY+' '+rect.top+' '+root.scrollTop);
        var mouseX = event.clientX - rect.left;
        var mouseY = event.clientY - rect.top;

        return {x: mouseX, y: mouseY};
    }


    function BackBuffer(Canvas, width, height){
        // be used for double buffer

        var backCanvas = document.createElement('canvas');
        backCanvas.setAttribute('width', width);
        backCanvas.setAttribute('height', height);
        this.backHdc = backCanvas.getContext('2d');
        this.presentHdc = Canvas.getContext('2d');


        BackBuffer.prototype.getDC = function(){
            return this.backHdc;
        };

        BackBuffer.prototype.present = function(){
            this.presentHdc.drawImage(backCanvas, 0, 0); // maybe practical
        };
    }


    function ResourceLoader(){
        // handle the loading of resource like picture
        // I found it needs some time to dynamically load pic if
        // you wirte something like this -- ( instance of Image ) img.src = /path/;
        // it will not show the pic if you call draw method in canvas immediately
        // so I decide to create a resouce handler.
        //
        // process:
        //   set a timeout to check the list of resources whether is loaded or not.
        //
        //   every value should has the same interface!!
        //   currently, use the dock typing to achieve this function

        //

        var deffered = $.Deferred();

        this.resList = [];
        this.isLoaded = [];

    }
    
    ResourceLoader.prototype.push = function(value){
        // will push resource state (deferred object)
        this.resList.push(value);
        this.isLoaded.push(value.deferred);
    };


    ResourceLoader.prototype.init = function(process){
        
        var $this = this;

        var resLoadloop = new Timer({
            callback: function(){
                for(var i=0; i<$this.resList.length; i++){
                    var deferred = $this.resList[i].isLoaded();
                    console.log(deferred.state());
                }
            }
        });
        
        
        $.when.apply($, $this.isLoaded).progress(function(){
            console.log('still in loading resource..run check again');
        }).done(function(){
            resLoadloop.stop();
            process.start();
        });

        resLoadloop.start();
        
        
    };


    function Sprite(src){

        this.img = new Image();
        this.x = 0;
        this.y = 0;
        this.width = 0;
        this.height = 0;
        this.deferred = $.Deferred();

        if(src != 'undefined'){
            this.load(src); //due to this.load defined at runtime... so
        }
    }

    Sprite.prototype.load = function(src){
        // initially, we set the display's height and width are the
        // same as the picture's
        this.img.src = src;
        this.width = this.img.width;
        this.height = this.img.height;
    };


    Sprite.prototype.setWidthandHeight= function(value){
        this.width = value.width;
        this.height = value.height;
    };


    Sprite.prototype.isLoaded = function(){
        
        if(this.img.complete){
            //check the img is loaded or not
            this.deferred.resolve(this.img.src+' is loaded');
        }else{
            this.deferred.notify('in process');
        }

        return this.deferred;
    };


    Sprite.prototype.draw = function(backBufferDC, sx, sy, x, y){
        // draw the content to the back buffer
        // img.complete
        // maybe, we can set a timer to trigger this...until it show the pic
        sx = sx || 0;
        sy = sy || 0;
        x  = x || 0;
        y = y || 0;

        backBufferDC.drawImage(this.img, sx, sy, this.width, this.height, x, y, this.width, this.height);
    };



    function animateSprite(backBuffer)
    {
        // load a sprite batching
        this.backBuffer = backBuffer;

        this.batch = new Sprite();
        this.frames = [];
        this.fps = 30;

        this.count = 0;
        this.deferred = $.Deferred();
        this.jsonLoaded = false;

    }

    animateSprite.prototype.setWidthandHeight = function(value){
        this.batch.setWidthandHeight(value);
    };


    animateSprite.prototype.isLoaded = function(){
        
        var $this = this;
        
        $.when(this.batch.isLoaded()).done(function(){
            
            if($this.jsonLoaded){
                $this.deferred.resolve('loaded');
            }else{
                $this.deferred.notify('process');
            }
        });
        return $this.deferred;
    };


    animateSprite.prototype.setframes = function(src, name){
        // load batch file and the points (x, y) of different frame
        // ex.
        //     this.setframe('ch.png', [{x: 10, y: 20}])
        var $this = this;
        this.batch.load(src);

        //$.each.apply(this.frames, function(value){
        //    this.frames.push(value);
        //}, points);
        $.getJSON("./data.json", function(data){
            
            $.each(data[name], function(index, element){
                $this.frames.push(element);
            });
            
        }).done(function(){
            $this.jsonLoaded = true;
        });



    };


    animateSprite.prototype.draw = function(){
        // need to think a way of python unpack argument..
        var sx = this.frames[this.count].x;
        var sy = this.frames[this.count].y;

        this.batch.draw(this.backBuffer.getDC(), sx, sy, 50, 50);
    };


    animateSprite.prototype.play = function(){

        var $this = this;

        console.log(this.count);

        if(this.count < this.frames.length){
            this.count++;
            setTimeout(function(){ $this.play();}, 1000/this.fps);
            //set timeout with this...
        }
        else{
                this.count = 0;
                console.log('count is '+this.count);
        }

    };


}(jQuery));
