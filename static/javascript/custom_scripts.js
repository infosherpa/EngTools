function formLoader() {
    const url = "api/form/";
    console.log('hello console')
    fetch(url)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        const formContainer = document.querySelector(".form-container");
        formContainer.innerHTML = data.form;
      });
}

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
const csrftoken = getCookie('csrftoken');


function postForm(){

    $('#button-id-advance').on('click', function(e){

        e.preventDefault();
        var form_id = '#geo_form';
        console.log(form_id);

        $.ajax({
            type : "POST",
            url: 'api/form/post/',
            headers: {
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            data: $(form_id).serialize(),
            success: function(data){
                if (!(data['success'])){
                    $(form_id)[0].reset();
                } else {
                    $(form_id).find('.success-message').show();
                }
            },
            error: function(){
                $(form_id).find('.error-message').show();
            }
        });
    });
};


$(document).on('submit','.geoform',function(){
            // catch the form's submit event
                // create an AJAX call
                console.log('js activated');
                var geo_form_var = '#geo_form';
                $.ajax({
                    headers: {
                    'X-CSRFToken': csrftoken,
                    },
                    data: $(geo_form_var).serialize(), // get the form data
                    type: $(geo_form_var).attr('method'), // GET or POST
                    url: 'api/form/post/',
                    // on success
                    success: function (response) {
                        console.log('hello console')
                        response => { return response.json();}
                        if (!(response['success'])) {
                            console.log('Form Data Unsuccessful')
                            $(geo_form_var).replaceWith(response['form_html']);
                        }
                        else {
                            alert("Data successfully posted");
                            const formContainer = document.querySelector(".form-container");
                            formContainer.innerHTML = response.form;
                        }

                    },
                    // on error
                    error: function (response) {
                        // alert the error if any error occured
                        response => { return response.json();}
                        alert(response.responseJSON.errors);
                        console.log(response.responseJSON.errors)
                    }
                });
                return false;
            })


$(document).on('click','.formadvance',function(e){
            // catch the form's submit event
                // create an AJAX call
                e.preventDefault();
                console.log('js activated');
                var form = '.tunform';
                $.ajax({
                    headers: {
                    'X-CSRFToken': csrftoken,
                    },
                    data: $(form).serialize(), // get the form data
                    type: $(form).attr('method'), // GET or POST
                    url: 'api/form/post/',
                    // on success
                    success: function (response) {
                        console.log('hello console')
                        response => { return response.json();}
                        if (!(response['success'])) {
                            console.log('Form Data Unsuccessful')
                            $(geo_form_var).replaceWith(response['form_html']);
                        }
                        else {
                            alert("Data successfully posted");
                            const formContainer = document.querySelector(".form-container");
                            formContainer.innerHTML = response.form;
                        }

                    },
                    // on error
                    error: function (response) {
                        // alert the error if any error occured
                        response => { return response.json();}
                        alert(response.responseJSON.errors);
                        console.log(response.responseJSON.errors)
                    }
                });
                return false;
            })


function dirFunc(){
    if(document.getElementById('id_load_pattern_description').value=='LL_RS'){
        document.getElementById('id_load_direction').value="Gravity";
        document.getElementById('id_load_location').value="RS";
        document.getElementById("id_force_start_depth").value = "";
        document.getElementById("id_force_end_depth").value = "";
        document.getElementById("id_force_start_depth").readOnly = true;
        document.getElementById("id_force_end_depth").readOnly = true;
    }
    else if(document.getElementById('id_load_pattern_description').value=='LL_CS'){
        document.getElementById('id_load_direction').value="Gravity";
        document.getElementById('id_load_location').value="CS";
        document.getElementById("id_force_start_depth").value = "";
        document.getElementById("id_force_end_depth").value = "";
        document.getElementById("id_force_start_depth").readOnly = true;
        document.getElementById("id_force_end_depth").readOnly = true;
    }
    else if(document.getElementById('id_load_pattern_description').value=='H_L'){
        document.getElementById('id_load_direction').value="X";
        document.getElementById('id_load_location').value="LW";
        document.getElementById("id_force_start_depth").readOnly = false;
        document.getElementById("id_force_end_depth").readOnly = false;
    }
    else if(document.getElementById('id_load_pattern_description').value=='R_L'){
        document.getElementById('id_load_direction').value="X";
        document.getElementById('id_load_location').value="RW";
        document.getElementById("id_force_start_depth").readOnly = false;
        document.getElementById("id_force_end_depth").readOnly = false;
    }
}


function bugPrompt(){
    prompt ("This is a prompt box", "Hello world");
}

function openForm() {
  document.getElementById("RequestForm").style.display = "none";
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

function submitBugform(e){
    console.log('js activated');
    e = e || window.event;
    e.preventDefault();
                var form = '.form-popup';
                console.log(form)
                $.ajax({
                    headers: {
                    'X-CSRFToken': csrftoken,
                    },
                    data: $(form).serialize(), // get the form data
                    type: "POST", // GET or POST
                    url: '/tun/bugreport/',
                    // on success
                    success: function (response) {
                        response => { return response.json();}
                        alert("Bug Report Sent");
                    },
                    // on error
                    error: function (response) {
                        // alert the error if any error occured
                        response => { return response.json();}
                        alert(response.responseJSON.errors);
                        console.log(response.responseJSON.errors)
                    }
                });
                closeForm()
                return false;
}

function submitFeaturesform(e){
    console.log('js activated');
    console.log(e)
    e = e || window.event;
    e.preventDefault();
                var form = '.form-popup';
                console.log(form)
                $.ajax({
                    headers: {
                    'X-CSRFToken': csrftoken,
                    },
                    data: $(form).serialize(), // get the form data
                    type: "POST", // GET or POST
                    url: '/tun/bugreport/',
                    // on success
                    success: function (response) {
                        response => { return response.json();}
                        alert("Bug Report Sent");
                    },
                    // on error
                    error: function (response) {
                        // alert the error if any error occured
                        response => { return response.json();}
                        alert(response.responseJSON.errors);
                        console.log(response.responseJSON.errors)
                    }
                });
                closeForm()
                return false;
}


function openFeatForm() {
  document.getElementById("myForm").style.display = "none";
  document.getElementById("RequestForm").style.display = "block";
}

function closeFeatForm() {
  document.getElementById("RequestForm").style.display = "none";
}

function formAdv() {
  if (document.getElementById("conc_col").style.display == "none") {
    document.getElementById("basic_frame").style.display = "none";
    document.getElementById("conc_col").style.display = "block";
    document.getElementById("formcontrolbut").value="Back To Essential Geometry";
  }
  else {
   document.getElementById("basic_frame").style.display = "block";
   document.getElementById("conc_col").style.display = "none";
   document.getElementById("formcontrolbut").value="Concourse/Column Inputs";
  }
}

function formtoBasic() {
  document.getElementById("basic_frame").style.display = "none";
  document.getElementById("conc_col").style.display = "block";
}

function concourseControl() {
    document.getElementById("id_concourse_slab_vertical_location").readOnly = false;
    document.getElementById("id_concourse_haunch_depth").readOnly = false;
    document.getElementById("id_concourse_haunch_width").readOnly = false;
    document.getElementById("id_concourse_haunch_depth").value = 0;
    document.getElementById("id_concourse_haunch_width").value = 0;
    if (document.getElementById("id_column_bays").value > 1) {
      document.getElementById("id_column_capital_height").readOnly = false;
      document.getElementById("id_column_capital_width").readOnly = false;
    }
    if (document.getElementById("id_concourse_slab_thickness").value == 0 || null) {
      document.getElementById("id_column_capital_height").value = null;
      document.getElementById("id_column_capital_width").value = null;
      document.getElementById("id_concourse_slab_vertical_location").value = null;
      document.getElementById("id_column_capital_height").value = null;
      document.getElementById("id_column_capital_width").value = null;

      document.getElementById("id_concourse_haunch_depth").readOnly = true;
      document.getElementById("id_concourse_haunch_width").readOnly = true;
      document.getElementById("id_concourse_slab_vertical_location").readOnly = true;
      document.getElementById("id_column_capital_height").readOnly = true;
      document.getElementById("id_column_capital_width").readOnly = true;
    }
}

function columnControl() {
    document.getElementById("id_column_width").readOnly = false;
    document.getElementById("id_column_capital_roof_slab_width").readOnly = false;
    document.getElementById("id_column_capital_roof_slab_height").readOnly = false;
    if (document.getElementById("id_concourse_slab_vertical_location").readOnly == false) {
      document.getElementById("id_column_capital_height").readOnly = false;
      document.getElementById("id_column_capital_width").readOnly = false;
    }
    if (document.getElementById("id_column_bays").value == 1) {
      document.getElementById("id_column_capital_roof_slab_width").value = null;
      document.getElementById("id_column_capital_roof_slab_height").value = null;
      document.getElementById("id_column_width").value = null;
      document.getElementById("id_column_capital_height").value = null;
      document.getElementById("id_column_capital_width").value = null;

      document.getElementById("id_column_capital_roof_slab_width").readOnly = true;
      document.getElementById("id_column_capital_roof_slab_height").readOnly = true;
      document.getElementById("id_column_capital_height").readOnly = true;
      document.getElementById("id_column_capital_width").readOnly = true;
      document.getElementById("id_column_width").readOnly = true;
    }
}


window.addEventListener("load", formLoad)

function formLoad() {
    console.log('load event')
    if (document.getElementById("id_column_bays").value > 1) {
      document.getElementById("id_column_capital_roof_slab_width").readOnly = false;
      document.getElementById("id_column_capital_roof_slab_height").readOnly = false;
      document.getElementById("id_column_width").readOnly = false;
      if (document.getElementById("id_concourse_slab_thickness").value > 0) {
        document.getElementById("id_column_capital_height").readOnly = false;
        document.getElementById("id_column_capital_width").readOnly = false;
      }
    }
    if (document.getElementById("id_concourse_slab_thickness").value > 0) {
      document.getElementById("id_concourse_slab_vertical_location").readOnly = false;
      document.getElementById("id_concourse_haunch_depth").readOnly = false;
      document.getElementById("id_concourse_haunch_width").readOnly = false;
      if (document.getElementById("id_column_bays").value > 1) {
        document.getElementById("id_column_capital_height").readOnly = false;
        document.getElementById("id_column_capital_width").readOnly = false;
      }
    }
}