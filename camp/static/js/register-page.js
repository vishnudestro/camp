function test() {
  const checkbox = document.getElementById("website");
  if(checkbox.checked == true){
    document.getElementById("ip-1").style = "display: block"
  }
    else{
        document.getElementById("ip-1").style = "display: none"
    }
}
function test1(){
    var checkbox = document.getElementById("event")
    if(checkbox.checked == true){
        document.getElementById("ip-2").style = "display: block"
    }
    else{
        document.getElementById("ip-2").style = "display: none"
    }
}
function test2(){
    var checkbox = document.getElementById("product")
    if(checkbox.checked == true){
        document.getElementById("ip-3").style = "display: block"
    }
    else{
        document.getElementById("ip-3").style = "display: none"
    }
}
function test3(){
    var checkbox = document.getElementById("business")
    if(checkbox.checked == true){
        document.getElementById("ip-4").style = "display: block"
    }
    else{
        document.getElementById("ip-4").style = "display: none"
    }
}

function changeDiv() {
    document.getElementById("password-div").style.display = "block";
    document.getElementById("login-button").style.display = "block";
    document.getElementById("change-button").style.display = "none";
}

function validate(){
    var companyName = document.forms["regform"]["company_name"];
    var personName = document.forms["regform"]["person_name"];
    var emailId = document.forms["regform"]["email"];
    if(companyName.value == ""){
        companyName.focus();
        document.getElementById("company-name").classList.toggle("invalid");
        document.getElementById("error-message").style = "display:block";
        return false;
    }
    if(personName.value == ""){
        personName.focus();
        document.getElementById("error-message").style = "display:block";
        document.getElementById("person-name").classList.toggle("invalid");
        return false;
    }
    return true;
}

function checkPassword(){
    var password = document.forms["regform"]["password"]
    var confirmPassword = document.forms["regform"]["confirmpassword"]
    if(password.value != confirmPassword.value){
        document.getElementById("errormsg").style = "display:block"
        return false
    }
    return true;
}
function showTeamCard(){
    document.getElementById("team-card").style = "display: block"
}
function showProjectCard(){
    document.getElementById("project-card").style = "display: block"
}
function routePage(company_id){
    window.location = "http://localhost:2000/user_details/"+ company_id
}
function showTeamOptions(id){
    document.getElementById(id).style.left = "0"
}
function hideTeamOptions(id){
    document.getElementById(id).style.left = "230px"
}  
function showProjectOptions(id){
    document.getElementById(id).style.left = "0"
}
function hideProjectOptions(id){
    document.getElementById(id).style.left = "230px"
}
function teamRename(id, name){
    document.getElementById('i-'+id).value = name
    document.getElementById('i-'+id).focus()
    document.getElementById('r-'+id).style.left = "0"
} 
function hideteamRename(id){
    document.getElementById('r-'+id).style.left = "250px"
    document.getElementById(id).style.left = "230px"
}
function showtodoOptions(){
    document.getElementById("todo-options-div").style.right = "0"
}
function hidetodoOptions(){
    document.getElementById("todo-options-div").style.right = "-280px"
}
function showtodotitleEdit(title, inputid){
    document.getElementById("todotitle").style.display = "none"
    document.getElementById(inputid).value = title
    document.getElementById("todo-options-div").style.right = "-280px"
    document.getElementById("todotitleEdit").style.display = "block"
}
function hidetodotitleEdit(){
    document.getElementById("todotitle").style.display = "block"
    document.getElementById("todotitleEdit").style.display = "none"
}
function addtodoTitle(id){
    var data = {
        title: $("#list-title").val(),
        ref_id : id,
        description : null
    }
    if(data.title == ""){
        $("#todo-title-error").css("display", "block")
        return false
    }
    else{
        $.ajax({
            url: "/api/add_todo",
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response){
                $('#to-do-card').append(todoCard_template(response))
                $('.input-card-body').css('display','none')
                $("#list-title").val("")
            }
        })
    }
}
var due ={
    start: '',
    end:''
}
var todoDue = {
    start: '',
    end:''
}
var inviteData = {
    people_id :"",
}
var static_data = []
var assigned_to = []
var notified_to = []
var todo_assigned_to = []
var todo_notified_to = []
var chat_members = []
//update array
var assigned_data = []
var notify_data = []
//end of update array
// update string
var assigned_remove = ''
var notify_remove = ''
//end of update string
var checkname = ""
var current_user_id = $(".current_user").attr("id")
function addListItems(val){
    var data = {
        description: $("#description").val(),
        assigned_to: assigned_to,
        notify_to: notified_to,
        due: due
    }
    if(data.description == ""){
        $("#form-error-msg").css("display", "block")
        return false
    }
    else{
        $.ajax({
            url:`/api/`+val+`/todo_list`,
            method:'POST',
            dataType: 'json',
            async: true,
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response){    
                $("#listContainer").append(lists_template(response));
                $("#list-form-card").css("display","none")
                $("#showFormCard").css("display", "block")
                $("#form-error-msg").css("display", "none")
                $("#description").val("")
                $("#assigned").val("")
                $("#notify").val("")
                document.getElementById("no-date").checked = false
                document.getElementById("specific-radio").checked = false
                $(".specific-label").css("display", "block");
                $(".specific-input-field").css("display", "none");
                $("#specific-date").val("")
                document.getElementById("multiple-radio").checked = false
                $(".multiple-label").css("display", "block");
                $(".multiple-input-field").css("display", "none");
                $("#start-date").val("")
                $("#end-date").val("")
            }
        })
    }
}
function addInvitePeople(val){
    var data = {
        id:val,
        people_id: inviteData.people_id
    }
    if(checkname == ""){
        return false
    }
    else{
        $.ajax({
            url:`/api/invite_user`,
            method:'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response){  
                $("#invitesection").append((invite_template(response)))
                $(".invite-card-body").css("display", "none")
                $("#invite-name").val("")
            }
        })
    }
}
function addComment(val, id){
    var md = window.markdownit();
    var result = md.render(easyMDE.value());
    if(easyMDE.value() == ""){
        return false
    }
    else{
        var data = {
            created_by: val,
            comment: result,
            ref_id: id
        }
        $.ajax({
            url: "/api/comments",
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response){
                $("#comment-container").append(comment_template(response))
                easyMDE.value("")
            }
        })
    }
}
function addPeopleTOChat(company_id, current_user_id){
    chat_members.push(current_user_id)
    chat_members.sort()
    var data = {
       members: chat_members,
       company_id : company_id
    }
    if($("#chat-room").val() == ""){
        return false
    }
    else{
        $.ajax({
            url: "/api/chatroom",
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response){
                window.location = response.url
                messageTest(response)
            }
        })
    }
}
function deleteTeamCard(id){
    $.ajax({
        url: "/api/delete?card_id=" + encodeURIComponent(id),
        method: 'GET', 
        success: function(response){
            var id = 'team-'+ response.card_id
           document.getElementById(id).remove()
        }
    });
}
function deleteProjectCard(id){
    $.ajax({
        url: "/api/delete?card_id=" + encodeURIComponent(id),
        method: 'GET', 
        success: function(response){
            var id = 'project-'+ response.card_id
           document.getElementById(id).remove()
        }
    });
}
function deletetodoCard(id){
    $.ajax({
        url: "/api/delete?todo_id=" + encodeURIComponent(id),
        method: 'GET', 
        success: function(response){
            window.location = "/todo/"+ response.ref_id
        }
    });
}
function singleTodoDelete(id){
    $.ajax({
        url: "/api/delete?task_id=" + encodeURIComponent(id),
        method: 'GET', 
        success: function(response){
            window.location = "/todo/todo_list/"+ response.todo_id
        }
    });
}
function updateTeamName(id, input_id){
    var name = document.getElementById(input_id).value
    var data = {
        name: name,
        _id : id
    }
    $.ajax({
        url: "/api/rename",
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response){
            document.getElementById('teamname-'+response._id).innerHTML = response.name
            document.getElementById('r-'+response._id).style.left = "250px"
            document.getElementById(response._id).style.left = "230px"
        }
    })
}
function updateProjectName(id, input_id){
    var name = document.getElementById(input_id).value
    var data = {
        name: name,
        _id : id
    }
    $.ajax({
        url: "/api/rename",
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response){
            document.getElementById('projectname-'+response._id).innerHTML = response.name
            document.getElementById('r-'+response._id).style.left = "250px"
            document.getElementById(response._id).style.left = "230px"
        }
    })
}
function updatetodoname(id, inputid){
    var name = document.getElementById(inputid).value
    data={
        name: name,
        _id:id
    }
    $.ajax({
        url: "/api/rename",
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response){
            document.getElementById("todotitle").innerHTML = response.name
            document.getElementById("todotitle").style.display = "block"
            document.getElementById("todotitleEdit").style.display = "none"
        }
    })
}
function updateSingleTodo(id){
    var final_assigned = todo_assigned_to.concat(assigned_data)
    var final_notify = todo_notified_to.concat(notify_data)
    data = {
        _id: id,
        description: $("#tododescription").val(),
        assigned_to: final_assigned,
        notify_to: final_notify,
        due: todoDue
    }
    $.ajax({
        url: "/api/edit_task",
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response){
            window.location = "http://localhost:2000/todo/todoset/" + response.task_id
        }
    })
}
$(document).ready(function() {
    $('#showlist').click(function(){
        $('.input-card-body').css('display','block')
    })
    $("#show-invite-list").click(function(){
        $(".invite-card-body").css("display", "block")
    })
    $("#hide-invite").click(function(){
        $(".invite-card-body").css("display", "none")
    })
    $('#hidelist').click(function(){
        $("#todo-title-error").css("display", "none")
        $('.input-card-body').css('display','none')
    })

    $("#showlist").click(function() {
        $(".input-card-body").css("display", "block");
    });
    $("#hidelist").click(function() {
        $(".input-card-body").css("display", "none");
    });
    $("#showFormCard").click(function(){
        $("#list-form-card").css("display", "block")
        $("#showFormCard").css("display", "none")
    })
    $("#hideFormCard").click(function(){
        $("#list-form-card").css("display", "none")
        $("#showFormCard").css("display", "block")
        $("#form-error-msg").css("display", "none")
    })
    $(this).click(function(){
        if($("#multiple-radio").is(":checked")){
            $(".multiple-label").css("display", "none");
            $(".multiple-input-field").css("display", "block");
            $(".specific-label").css("display", "block");
            $(".specific-input-field").css("display", "none");
            var start = $("#start-date").val()
            var end = $("#end-date").val()
            addDueDate(start, end)
        }
        if($("#specific-radio").is(":checked")){
            $(".multiple-label").css("display", "block");
            $(".multiple-input-field").css("display", "none");
            $(".specific-label").css("display", "none");
            $(".specific-input-field").css("display", "block");
            var start = null
            var end = $('#specific-date').val()
            addDueDate(start, end)
        }
        if($("#no-date").is(":checked")){
            $(".multiple-label").css("display", "block");
            $(".multiple-input-field").css("display", "none");
            $(".specific-label").css("display", "block");
            $(".specific-input-field").css("display", "none");
            var start = null
            var end = null
            addDueDate(start, end)
        }
    })
    // single todo due 
    $(this).click(function(){
        if($("#no-due").is(":checked")){
            $("#specificdate").css("display", "block")
            $("#specific-input").css("display", "none")
            $("#multipledays").css("display", "block")
            $("#multiple-input").css("display", "none")
            var start = null
            var end = null
            addTodoDueDate(start, end)
        }
        if($("#specific-date").is(":checked")){
            $("#specificdate").css("display", "none")
            $("#specific-input").css("display", "block")
            $("#multipledays").css("display", "block")
            $("#multiple-input").css("display", "none")
            var start = null
            var end = $('#specific-input').val()
            addTodoDueDate(start, end)
        }
        if($("#multiple-days").is(":checked")){
            $("#specificdate").css("display", "block")
            $("#specific-input").css("display", "none")
            $("#multipledays").css("display", "none")
            $("#multiple-input").css("display", "block")
            var start = $("#multiple-start").val()
            var end = $("#multiple-end").val()
            addTodoDueDate(start, end)
        }
    })
    //end of single todo due
    // adding team
    $("#save-team").click(function(){
        var val = $("#team-name").val()
        if(val == ""){
            $("#team-name").css({"border-color":"red", "box-shadow":"0 0 4px red"})
            return false
        }
        else{
            $.ajax({
                url: "/api/team?team_name=" + encodeURIComponent(val),
                method: 'GET',  
                success: function(response){
                    $("#teamList").append(teamCard_template(response))
                    $("#team-name").val("")
                    $("#team-name").css({"border-color":"#a4d2ff", "box-shadow":"0 0 6px rgba(27,106,201,0.5)"})
                    $("#team-card").css("display", "none");
                }
            });
        }
    })
    $("#cancel-save-team").click(function(){
        $("#team-name").css({"border-color":"#a4d2ff", "box-shadow":"0 0 6px rgba(27,106,201,0.5)"})
        $("#team-card").css("display", "none");
    })
    //end of adding team

    // adding project
    $("#save-project").click(function(){
        var val = $("#project-name").val()
        if(val == ""){
            $("#project-name").css({"border-color":"red", "box-shadow":"0 0 4px red"})
            return false
        }
        else{
            $.ajax({
                url: "/api/project?project_name=" + encodeURIComponent(val),
                method: 'GET',
                success: function(response) {
                    $("#projectList").append(projectCard_template(response))
                    $("#project-name").val("")
                    $("#project-name").css({"border-color":"#a4d2ff", "box-shadow":"0 0 6px rgba(27,106,201,0.5)"})
                    $('#project-card').css("display", "none")
                }
            });
        }
    })
    $("#cancel-save-project").click(function(){
        $("#project-name").css({"border-color":"#a4d2ff", "box-shadow":"0 0 6px rgba(27,106,201,0.5)"})
        $("#project-card").css("display", "none");
    })
    //end of adding project

    $("#start-date").on("change", function(){
        var limit = $("#start-date").val()
        $("#end-date").attr("min", limit)
    })
    //show chatSelection
    $("#ping").click(function(){
        $("#ping-selection").css("display", "block")
    })
    //socket.io
    var socket;
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    socket.on('status', function(data) {
        console.log("connected")
    });
    socket.on('message', function(data) {
        var time = moment.utc(data.created_at).format("hh:mma")
        if(data.created_by.user_id == current_user_id){
            $('#message_container').append(currentbubble_template(data, time))
        }
        else{
            $('#message_container').append(bubble_template(data, time))
        }
    });
    $('.message').keypress(function(event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == '13') {
            message = $('.message').val();
            chatroom_id = $(".message").attr("id");
            created_by = $(".current_user").attr("id")

            if(message == ''){
                return false
            }
            else{
                var data = {
                    message:message,
                    chatroom_id:chatroom_id,
                    created_by:created_by,
                }
                $.ajax({
                    url: "/api/message",
                    method: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response){

                    }
                })
                $('.message').val('');
            }   
        }
    });
    //end of socket.io
});
function addDueDate(start, end){
    due.start = String(start)
    due.end = String(end)
}
function addTodoDueDate(start, end){
    todoDue.start = String(start)
    todoDue.end = String(end)
}
function teamCard_template(data){
    return `<div id='team-`+data.team_id+`' class="col-sm-4 col-md-4">
                <div class="card" style="width: auto;position: relative;overflow: hidden;border-radius: 8px;">
                    <div class="card-body">
                        <div style="display:flex;justify-content:space-between">
                            <h5 class="card-title">
                                <a id='teamname-`+data.team_id+`' style="color: #283c46" href='`+data.url+`'>`+data.name+`</a>
                            </h5>
                            <img onclick="showTeamOptions('`+data.team_id+`')" style="cursor:pointer" src="/static/images/horizontal.svg">
                        </div>
                        <p class="card-text">Company-wide announcements and stuff everyone needs to know.</p>
                    </div>
                    <div id="`+data.team_id+`" class="card-body" style="position:absolute; left: 250px;width: 100%;height: 118px;background-color: white;transition: 0.3s;padding: 0">
                        <div style="display: flex;justify-content: space-between;margin-bottom: 8px;padding: 1.25rem 1.25rem 0 1.25rem">
                            <h5 class="card-title">
                                <a style="color: #283c46">`+data.name+`</a>
                            </h5>
                            <img onclick="hideTeamOptions('`+data.team_id+`')" style="cursor:pointer" src="/static/images/close.svg">
                        </div>
                        <div onclick="teamRename('`+data.team_id+`', '`+data.name+`')" class="team-option-hover" style="display:flex;padding: 4px 20px;">
                            <img style="margin-right: 8px;" src="/static/images/rename.svg">
                            <p style="color:#070707;font-size:12px;margin: 0;padding:2px">Rename this team</p>
                        </div>
                        <div onclick="deleteTeamCard('`+data.team_id+`')" class="team-option-hover" style="display:flex;padding: 4px 20px;">
                            <img style="margin-right: 8px;" src="/static/images/delete.svg">
                            <p style="color:#283c46;font-size:12px; margin: 0;padding: 2px;">Delete it...</p>
                        </div>
                    </div>
                    <div id="r-`+data.team_id+`" class="card-body" style="position:absolute;left:250px;width: 100%;height: 118px;background-color: white;transition: 0.3s;padding: 0">
                        <div style="display: flex;justify-content: space-between;padding: 1.25rem 1.25rem 0 1.25rem">
                            <input id="i-`+data.team_id+`" class="renameInput" type="text" placeholder="Name this team">
                        </div>
                        <div style="display:flex;padding: 4px 20px;">
                            <button onclick="updateTeamName('`+data.team_id+`','i-`+data.team_id+`')" type="button" style="background-color: #596568;border-radius: 24px;border: 1px solid #596568;color:white;font-size:12px;padding: 6px 12px;margin-right: 4px;">Save</button>
                            <button onclick="hideteamRename('`+data.team_id+`')" type="button" style="background-color: #fff;border-radius: 24px;outline:0;border: 1px solid #596568;color:#596568;font-size:12px;padding: 6px 12px;">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>`
}
function projectCard_template(data){
    return `<div id='project-`+data.team_id+`' class="col-sm-4 col-md-4">
                <div class="card" style="width: auto;position: relative;overflow: hidden;border-radius: 8px;">
                    <div class="card-body">
                        <div style="display:flex;justify-content:space-between">
                            <h5 class="card-title">
                                <a id="projectname-`+data.team_id+`" style="color: #283c46" href='`+data.url+`'>`+data.name+`</a>
                            </h5>
                            <img onclick="showTeamOptions('`+data.team_id+`')" style="cursor:pointer" src="/static/images/horizontal.svg">
                        </div>
                        <p class="card-text">Company-wide announcements and stuff everyone needs to know.</p>
                    </div>
                    <div id="`+data.team_id+`" class="card-body" style="position:absolute; left: 250px;width: 100%;height: 118px;background-color: white;transition: 0.3s;padding: 0">
                        <div style="display: flex;justify-content: space-between;margin-bottom: 8px;padding: 1.25rem 1.25rem 0 1.25rem">
                            <h5 class="card-title">
                                <a style="color: #283c46">`+data.name+`</a>
                            </h5>
                            <img onclick="hideTeamOptions('`+data.team_id+`')" style="cursor:pointer" src="/static/images/close.svg">
                        </div>
                        <div onclick="teamRename('`+data.team_id+`', '`+data.name+`')" class="team-option-hover" style="display:flex;padding: 4px 20px;">
                            <img style="margin-right: 8px;" src="/static/images/rename.svg">
                            <p style="color:#070707;font-size:12px;margin: 0;padding:2px">Rename this project</p>
                        </div>
                        <div onclick="deleteProjectCard('`+data.team_id+`')" class="team-option-hover" style="display:flex;padding: 4px 20px;">
                            <img style="margin-right: 8px;" src="/static/images/delete.svg">
                            <p style="color:#283c46;font-size:12px; margin: 0;padding: 2px;">Delete it...</p>
                        </div>
                    </div>
                    <div id="r-`+data.team_id+`" class="card-body" style="position:absolute;left:250px;width: 100%;height: 118px;background-color: white;transition: 0.3s;padding: 0">
                        <div style="display: flex;justify-content: space-between;padding: 1.25rem 1.25rem 0 1.25rem">
                            <input id="i-`+data.team_id+`" class="renameInput" type="text" placeholder="Name this project">
                        </div>
                        <div style="display:flex;padding: 4px 20px;">
                            <button onclick="updateProjectName('`+data.team_id+`','i-`+data.team_id+`')" type="button" style="background-color: #596568;border-radius: 24px;border: 1px solid #596568;color:white;font-size:12px;padding: 6px 12px;margin-right: 4px;">Save</button>
                            <button onclick="hideteamRename('`+data.team_id+`')" type="button" style="background-color: #fff;border-radius: 24px;outline:0;border: 1px solid #596568;color:#596568;font-size:12px;padding: 6px 12px;">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>`
}
function todoCard_template(data){
    return `<div class="col-sm -4 col-md-4">
                <div class="card" style="width: auto;">
                    <div class="card-body">
                        <h5 class="card-title">
                            <a style="color: #596568" href="`+data.url+`">
                                `+data.title+`
                            </a>
                        </h5>
                    </div>
                </div>
            </div>`
}
function lists_template(data){
    return `<div class="row" style="margin:0">
                <label class="todo-container">
                    <a href="http://localhost:2000/todo/todoset/` +data.task_details.task_id+`">
                        `+data.task_details.description+`
                    </a>
                    <input type="checkbox">
                    <span class="todo-checkmark"></span>
                </label>
            </div>
    `
}
function invite_template(val){
    return `<div class="col-sm-6 col-md-6" style="padding:0">
                <div class="card invite-card-styles" style="width: auto;margin:4px;height: 130px;">
                    <div class="card-body">
                        <h5 style="color:#283c46;font-weight: bold;font-size: 22px;">`+val.person_name+`</h5>
                        <h5 style="color:#2e3c46;font-size:18px">`+val.email+`</h5>
                        <h5 style="color:#2e3c46;font-size:18px">`+val.job_title+`</h5>
                    </div>
                </div>
            </div>
    `
}
function comment_template(val){
    // var md = window.markdownit();
    // var result = md.render(val.comment);
    return `<div class="card" style="width: auto;background: #faf8f7;border-radius: 20px ;padding: 15px 20px;margin: 20px 0;border:none">
                <div class="card-body" style="padding:0 !important">
                    <h6 class="card-text" style="color:#283c46;font-weight:bold;font-size: 15px;">
                        `+ val.created_by +`
                        <span style="font-weight: normal"> `+ val.job_title+`</span>
                    </h6>
                    <p class="card-text">`+ val.comment +`</p>
                </div>
            </div>`
}
function currentbubble_template(val, time){
    return `<div class="bubble-main-div">
                <div class="currentbubble-sub-div">
                    <div class="currentbubble-content">
                        <span>`+time+`</span>`+val.created_by.person_name+`
                        <div style="font-size:16px;font-weight:normal">
                            `+val.message+`
                        </div>
                    </div>
                </div> 
            </div>`
}
function bubble_template(val, time){
    return `<div class="bubble-main-div">
                <div class="bubble-sub-div">
                    <div class="bubble-content">`
                    + val.created_by.person_name+`<span>`+time+`</span>
                        <div style="font-size:16px;font-weight:normal">
                            `+val.message+`
                        </div>
                    </div>
                </div>
            </div>`
}


// Today's date
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0!
var yyyy = today.getFullYear();
if(dd<10){
    dd='0'+dd
} 
if(mm<10){
    mm='0'+mm
} 

today = yyyy+'-'+mm+'-'+dd;
$("#specific-date").attr("min", today)
$("#start-date").attr("min", today)
// Today's date end


// flexdatalist-assign
$('#assigned.flexdatalist').on( "select:flexdatalist", function(event,set){
    assigned_to.push(set.value)
})
// flexdatalist end

// flexdatalist-notify
$('#notify.flexdatalist').on("select:flexdatalist", function(event, set){
    notified_to.push(set.value)
})
$('#invite-name.flexdatalist').on( "select:flexdatalist", function(event,set){
    checkname = set.label
    inviteData.people_id = set.value;
})

// flexdata chatroom
$("#chat-room").on("select:flexdatalist", function(event, set){
    $("#ping-button").css("display","block")
    chat_members.push(set.value)
})
$("#chat-room").on("after:flexdatalist.remove", function(event, set){
    $("#ping-button").css("display","none")
})
var easyMDE = new EasyMDE({element: $('#my-text-area')[0], toolbar: ["bold", "italic", "strikethrough", "link", "heading", "quote", "code", "unordered-list", "ordered-list"]});

$("#singleassigned").on("select:flexdatalist", function(event, set){
    todo_assigned_to.push(set.value)
})
$("#singlenotify").on("select:flexdatalist", function(event, set){
    todo_notified_to.push(set.value)
})
$("#singleassigned").on('change:flexdatalist', function(event, set, options){
    for(i=0;i < set.length;i++){
        for(j=0;j < set[i].value.length; j++){
            assigned_remove = set[i].value[j]
        }
    }
    assigned_data = assigned_data.filter(function(item) {
        return item !== assigned_remove
    })
})
$("#singlenotify").on('change:flexdatalist', function(event, set, options){
    for(i=0;i < set.length;i++){
        for(j=0;j < set[i].value.length; j++){
            notify_remove = set[i].value[j]
        }
    }
    notify_data = notify_data.filter(function(item) {
        return item !== notify_remove
    })
})

//functions for the edit todo page
// var easyMDE = new EasyMDE({element: $('#editpage-text-area')[0], toolbar: ["bold", "italic", "strikethrough", "link", "heading", "quote", "code", "unordered-list", "ordered-list"]});

function showDiscussionDiv(){
    document.getElementById("discussion-div").style.display = "block"
    document.getElementById("discussion-input").style.display = "none"
}
function showtodoOptions(){
    document.getElementById("todo-options-div").style.right = "0"
}
function hidetodoOptions(){
    document.getElementById("todo-options-div").style.right = "-280px"
}
function editSingleTodo(){
    document.getElementById("single-todo-edit").style.display = "block"
    document.getElementById("single-todo-display").style.display = "none"
    document.getElementById("todo-options-div").style.right = "-280px"
}
function canceltodoedit(){
    document.getElementById("single-todo-edit").style.display = "none"
    document.getElementById("single-todo-display").style.display = "block"
}
$('.flexdatalists').flexdatalist({
    selectionRequired: true,
    valueProperty: 'name',
    minLength: 1
});
$('.flexdatalistss').flexdatalist({
    minLength: 1,
    valueProperty: 'name',
    selectionRequired: true,
});
$('.flex_static').flexdatalist({
    selectionRequired: true,
    valueProperty: 'name',
    minLength: 1,
});
