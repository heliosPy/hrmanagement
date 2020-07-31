function display()
{
    var id = document.getElementById("id_op_code").value;

    var req = new XMLHttpRequest();


    req.onreadystatechange = show;
    req.open("GET", "http://127.0.0.1:8000/manager/check/?opid="+id,true);
    req.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
    req.send()


    function show() {
        if (req.readyState==4 && req.status == 200){
            var response = req.responseText;
            if(response=="No"){
                alert("The Opertunity Code already Taken")
            }
        }

    }
}