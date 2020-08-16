$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var infoModal = $('.info-modal')
    // infoModal.on('show.bs.modal', function(event){
    //     console.log(event)
    // })
    infoModal.on('hidden.bs.modal', function(event){
        window.location.reload()
    })
    // Enroll Modal
    var enrollModal = $('#enroll-modal')
    var enrollBtn = $('.enroll-btn')
    enrollBtn.click(function(){
        enrollModal.modal('show')
    })
    var enrollForm = $('#enroll-form')
    enrollForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var httpMethod = thisForm.attr('method')
        var formEndpoint = thisForm.attr('action')
        var formData = thisForm.serialize();
        $.ajax({
            url: formEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                console.log(data)
                enrollModal.modal('hide')
                infoModal.find('.modal-body').text('Gratulacje')
                
                infoModal.modal('show')
                // close modal
                // fetch course content
                // remove enroll button
                // show conrim
            },
            error: function(errorData){
                console.log(errorData)
                enrollModal.find('#course_access_key').addClass("is-invalid")
                enrollModal.find('.invalid-feedback').text(errorData.responseJSON.message)
            }
        })
    })
    

    // fetchSubjects();
    var loginForm = $('.login-form')
    loginForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var httpMethod = thisForm.attr('method')
        var formEndpoint = thisForm.attr('action')
        var formData = thisForm.serialize();
        //pokazać ładowanie
        $('#username').prop('disabled', true)
        $('#password').prop('disabled', true)
        $.ajax({
            url: formEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                console.log(data)
                loginForm[0].reset();
                if (data.full_name){
                    $('.user-name-display').text(data.full_name)
                } else {
                    $('.user-name-display').text(data.username)
                }
                
                $('.navbar-user-control').css('display', 'unset')
                $('.navbar-login-button').css('display', 'none')
                $('.subjects').css('display', 'unset')
                if(data.teacher){
                    $('.content-manage').css('display','unset')
                }
                
                //fetchSubjects();
                $('#exampleModal').modal('hide')
                //zakończyć ładowanie
                },
            error: function(errorData){
                $('#username').addClass('is-invalid').prop('disabled', false)
                $('#password').addClass('is-invalid').prop('disabled', false)
                $('#passwordHelpBlock').html(errorData.responseJSON.message).css('display', '')
                $('.login-help-info').css('display', '')
                console.log("error")
                console.log(errorData)
                },
            })
        })
    function fetchSubjects() {
        subjects = [{ name: 'Algebra z Geometrią Analityczną II 2020', 'id': 4}, { name: 'Algebra z Geometrią Analityczną II 2020', 'id': 4}]
        var subjectsList = $('.subjects > div > .subjects-list')
        subjectsList.html('')
        subjects.forEach((obj) => {
            subjectsList.append(`<a class="dropdown-item" href="#">${obj.name}</a>`)
        })
        
        subjectsList.html('<a class="dropdown-item" href="#">Algebra z Geometrią Analityczną II 2020</a><a class="dropdown-item" href="#">Algebra z Geometrią Analityczną II 2020</a>')
    }
    var loginFormSubmitButton = $('.login-form-submit')
    loginFormSubmitButton.click(function(){
        loginForm.submit();
    })

    // add content modal
    var addContentModal = $('.module-add-text-modal')
    var moduleAddTextButton = $('.module-add-text')
    moduleAddTextButton.click(function(event){
        addContentModal.modal('show', data={'ta': 'nom'})
        addContentModal.find('.add-content-form').find('#id_module_id').val(event.originalEvent.target.dataset.id)
    })
    addContentModal.on('show.bs.modal', function(event){
        var thisModal = $(this)
        thisModal.find('.add-content-form').find('#id_content_id').val(null)
    })
    var addContentForm = addContentModal.find('.add-content-form')
    addContentForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var httpMethod = thisForm.attr('method')
        var formEndpoint = thisForm.attr('action')
        // var formData = thisForm.serialize();
        var fd = new FormData(this);
        // if (thisForm.attr('data-type') === 'image'){
        //     var files = thisForm.find('#id_file')[0].files[0];
        // }
                    

        $.ajax({
            url: formEndpoint,
            method: httpMethod,
            data: fd,
            enctype: 'multipart/form-data',
            contentType: false,
            cache: false,
            processData:false,
            success: function(data){
                infoModal.find('.modal-body').text(data.message)
                addContentModal.modal('hide')
                infoModal.modal('show')
            },
            error: function(errorData){
                console.log(errorData)
            }
        })
    })
    var contentSubmitBtn = $('.add-content-modal-submit-btn')
    contentSubmitBtn.click(function(event){
        var activeContentFormDiv = addContentModal.find('.tab-pane.fade.show.active')
        var activeContentForm = activeContentFormDiv.find('form')
        activeContentForm.submit();
    })


    var addModuleModal = $('.module-add-module-modal')
    var addModuleButton = $('.course-add-module-button')
    addModuleButton.click(function(event){
        addModuleModal.modal('show')
        addModuleModal.find(".add-module-form").trigger("reset");
    })
    var addModuleSubmitButton = $('.add-module-modal-submit-btn')
    var addModuleForm = $('.add-module-form')
    addModuleSubmitButton.click(function(event){
        addModuleForm.submit()
    })

    addModuleForm.submit(function(event){
        event.preventDefault()
        var thisForm = $(this)
        var httpMethod = thisForm.attr('method')
        var formEndpoint = thisForm.attr('action')
        console.log("to chociaż działa?")
        $.ajax({
            url: formEndpoint,
            method: httpMethod,
            data: thisForm.serialize(),
            // headers: {'ContentType':'application/json'},
            success: function(data){
                console.log(data)
                addModuleModal.modal('hide')
                infoModal.find('.modal-body').text(data.message)
                infoModal.modal('show')
            },
            error: function(errorData){
                console.log(error)
                addModuleModal.modal('hide')
                infoModal.find('.modal-body').text(errorData.message)
                infoModal.modal('show')
            }
        })
    })

    var moduleDescEditBtn = $('.module-desc-edit')
    moduleDescEditBtn.click(function(event){
        addModuleModal.modal('show')
        // addModuleForm.find('#id_module_id').val(event.originalEvent.target.dataset.id)
        var moduleEditId = event.originalEvent.target.dataset.id
        var moduleEditEndpoint = event.originalEvent.target.dataset.endpoint
        addModuleForm.attr('action', moduleEditEndpoint)
        addModuleForm.find("input[name='title']").val(event.originalEvent.target.dataset.moduletitle)
        addModuleForm.find("textarea[name='description']").val(event.originalEvent.target.dataset.moduledesc)
        var checked = event.target.dataset.visible === "True" ? true: false;
        addModuleForm.find("input[name='visible']").attr("checked", checked)
        console.log(moduleEditId, moduleEditEndpoint)
    })
    var moduleDeleteBtn = $('.module-delete')
    var moduleDeleteModal = $('.module-delete-modal')
    var moduleDeleteSubmitBtn = $('.delete-module-modal-submit-btn')
    var moduleDeleteTitleSpan = $('.delete-module-title')
    moduleDeleteBtn.click(function(event){
        event.preventDefault()
        moduleDeleteModal.modal('show')
        console.log(moduleDeleteSubmitBtn[0].dataset)
        moduleDeleteSubmitBtn[0].dataset.endpoint = event.originalEvent.target.dataset.endpoint
        moduleDeleteTitleSpan[0].textContent = event.originalEvent.target.dataset.moduletitle
        console.log("DELETE:", event.originalEvent.target.dataset.id)
    })
    moduleDeleteSubmitBtn.click(function(event){
        var endpoint = event.originalEvent.target.dataset.endpoint
        console.log("Legancko")
        $.ajax({
            method: 'POST',
            url: endpoint,
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            success: function(data){
                moduleDeleteModal.modal('hide')
                infoModal.find('.modal-body').text(data.message)
                infoModal.modal('show')
            },
            error: function(errorData){
                moduleDeleteModal.modal('hide')
                infoModal.find('.modal-body').text(errorData.message)
                infoModal.modal('show')
            }
        })
    })
    var courseDeleteBtn = $('.course-delete-btn')
    var courseDeleteModal = $('.course-delete-modal')
    var courseDeleteModalSubmitBtn = $('.delete-course-modal-submit-btn')
    var courseDeleteTitleSpan = $('.course-delete-title')
    courseDeleteBtn.click(function(event){
        event.preventDefault()
        var url = event.originalEvent.target.attributes.href.value
        courseDeleteModal.modal('show')
        console.log(url)
        courseDeleteModalSubmitBtn[0].dataset.endpoint = url
        console.log(courseDeleteTitleSpan)
        courseDeleteTitleSpan[0].textContent = event.originalEvent.target.dataset.title
        console.log(courseDeleteModalSubmitBtn[0].dataset.endpoint)
    })
    courseDeleteModalSubmitBtn.click(function(event){
        var endpoint = event.originalEvent.target.dataset.endpoint
        console.log(endpoint)
        $.ajax({
            method: 'POST',
            url: endpoint,
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            success: function(data){
                courseDeleteModal.modal('hide')
                infoModal.find('.modal-body').text(data.message)
                infoModal.modal('show')
            },
            error: function(errorData){
                courseDeleteModal.modal('hide')
                infoModal.find('.modal-body').text(errorData.message)
                infoModal.modal('show')
            }
        })
    })
    var contentDeleteBtn = $('.content-delete')
    contentDeleteBtn.click(function(event){
        event.preventDefault()
        moduleDeleteModal.modal('show')
        console.log(moduleDeleteSubmitBtn[0].dataset)
        moduleDeleteSubmitBtn[0].dataset.endpoint = event.originalEvent.target.dataset.endpoint
        moduleDeleteTitleSpan[0].textContent = event.originalEvent.target.dataset.contenttitle
        console.log("DELETE:", event.originalEvent.target.dataset.id)
    })
    // moduleDeleteSubmitBtn.click(function(event){
    //     var endpoint = event.originalEvent.target.dataset.endpoint
    //     console.log("Legancko")
    //     $.ajax({
    //         method: 'POST',
    //         url: endpoint,
    //         headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
    //         success: function(data){
    //             moduleDeleteModal.modal('hide')
    //             infoModal.find('.modal-body').text(data.message)
    //             infoModal.modal('show')
    //         },
    //         error: function(errorData){
    //             moduleDeleteModal.modal('hide')
    //             infoModal.find('.modal-body').text(errorData.message)
    //             infoModal.modal('show')
    //         }
    //     })
    // })

    var contentShowHideBtn = $('.content-hide')
    contentShowHideBtn.click(function(event){
        var endpoint = event.originalEvent.target.dataset.endpoint
        $.ajax({
            method: 'POST',
            url: endpoint,
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            success: function(data){
                infoModal.find('.modal-body').text(data.message)
                infoModal.modal('show')
            },
            error: function(errorData){
                infoModal.find('.modal-body').text(errorData.message)
                infoModal.modal('show')
            }
        })
    })
    
    var moduleShowHideBtn = $('.module-hide')
    moduleShowHideBtn.click(function(event){
        var endpoint = event.originalEvent.target.dataset.endpoint
        $.ajax({
            method: 'POST',
            url: endpoint,
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            success: function(data){
                infoModal.find('.modal-body').text(data.message)
                infoModal.modal('show')
            },
            error: function(errorData){
                infoModal.find('.modal-body').text(errorData.message)
                infoModal.modal('show')
            }
        })
    })

    var contentEditButton = $('.content-edit')
    contentEditButton.click(function(event){
        var data = {
            id: event.target.dataset.id,
            title: event.target.dataset.title,
            type: event.target.dataset.type,
            text: event.target.dataset.text,
            file: event.target.dataset.file,
            visible: event.target.dataset.visible,
            edit: true
        }
        addContentModal.modal('show', data=data)
        addContentModal.find('.add-content-form').find('#id_module_id').val(null)
    })
    addContentModal.on('show.bs.modal', function(event){
        var thisModal = $(this)
        if (event.relatedTarget.edit){
            console.log("EDYCJAAAA")
            switch (event.relatedTarget.type.substring(10)) {
            case 'text':
                thisModal.find('.add-content-form').find('#id_content').val(event.relatedTarget.text)
                thisModal.find('#list-tab').find('#list-text-list').tab('show')
                break;
            case 'image':
                thisModal.find('#list-tab').find('#list-image-list').tab('show')
                break;
            case 'file':
                thisModal.find('#list-tab').find('#list-file-list').tab('show')
                break;
            case 'video':
                // thisModal.find('.add-content-form').find('#id_file').val(event.relatedTarget.file)
                thisModal.find('#list-tab').find('#list-video-list').tab('show')
                break;
            default:
                break;
        }
        thisModal.find('.add-content-form').find('#id_content_id').val(event.relatedTarget.id)
        thisModal.find('.add-content-form').find('#id_title').val(event.relatedTarget.title)
        var visible = event.relatedTarget.visible === "False" ? false : true;
        thisModal.find('.add-content-form').find('#id_visible').attr('checked', visible)
        } else {
            thisModal.find('.add-content-form').trigger('reset');
        }            
    })
    var moveContentUp = $('.move-content')
        moveContentUp.click(function(event){
            var data = JSON.stringify({
                id: event.target.dataset.id,
                direction: event.target.dataset.direc
            });
            var endpoint = event.target.dataset.endpoint
            $.ajax({
                method: 'POST',
                url: endpoint,
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
                data: data,
                success: function(data){
                    infoModal.find('.modal-body').text(data.message)
                    infoModal.modal('show')
                },
                error: function(errorData){
                    infoModal.find('.modal-body').text(errorData.message)
                    infoModal.modal('show')
                }
            })
        })
    
})