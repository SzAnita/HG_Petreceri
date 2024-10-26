let i = 1
$(document).on("click", ".add_task", function (event) {
    let task_name = $("#task"+i+"_name").val();
    let task_desc  = $("task"+i+"_desc").val();
    let task_person = $("#task"+i+"_person").val();
    let party_id = $("#party_id").val()
    $.ajax({
        method: "POST",
        headers: {'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val()},
        url: "{% url 'add_tasks' %}",
        data: {
            'party_id': party_id,
            'task_name': task_name,
            'task_desc': task_desc,
            'task_person': task_person,
        }, success: function (data) {
            i = i+1;
            let task_name_next = "<label for='task"+i+"_name'>Name of the task<br><input type='text' name='task"+i+"_name' id='task"+i+"_name'></label>"
            let task_desc_next = "<label for='task"+i+"_desc'>Description of the task<br><input type='text' name='task"+i+"_desc' id='task"+i+"_desc'></label>"
            let task_person_next = "<label for='task"+i+"_person'>Person responsible for task<br><input type='text' name='task"+i+"_person' id='task"+i+"_person'></label>"
            $(".add-task").before()
        }
    })
})