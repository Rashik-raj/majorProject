window.addEventListener('load', () =>{
    var canvas = document.querySelector("#canvas");
    const ctx =  canvas.getContext("2d");

    var drawing = false;
    function startPosition(){
        drawing = true;
      
    }

    function finishedPosition(){
        drawing = false;
        ctx.beginPath()
      
    }

    function draw(e) {
        if(!drawing) return;
        var pos = getMousePos(canvas, e);
        posx = pos.x;
        posy = pos.y;
        ctx.lineWidth = 2;
        ctx.fillStyle = "#000000";
        // ctx.fillRect(posx, posy, 4, 4);
        ctx.lineTo(posx, posy)
        ctx.stroke()
    }
    window.addEventListener('mousemove', draw, false);
    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', finishedPosition);
   
    
    function getMousePos(canvas, evt) {
        var rect = canvas.getBoundingClientRect();
        return {
            x: (evt.clientX - rect.left) / (rect.right - rect.left) * canvas.width,
            y: (evt.clientY - rect.top) / (rect.bottom - rect.top) * canvas.height
        };
    }

    var save_btn = document.querySelector('#save_button')
    var save = document.querySelector('#save')
    save_btn.addEventListener('click', function(e){
        const confirmation = confirm('Do you want to save?');
        if(confirmation == true){
            save.href = canvas.toDataURL();
            save.download = 'mypaint.jpeg';
        }
    }, false)

    var button = document.querySelector('#clear')
    button.addEventListener('click', function(e){
        ctx.clearRect(0, 0 , canvas.width, canvas.height);
    }, false)
})



$(document).ready(function(){
    $(".switch-toggle").click(function(){
        $("#canvasDiv").fadeToggle('fast');
        $("#uploadImage").fadeToggle('fast');
      });
});