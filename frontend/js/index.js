// JS to show name of photo uploaded
const imageUploadBtn = document.getElementById("imageUpload");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");

customBtn.addEventListener("click", function () {
    imageUploadBtn.click();
});

imageUploadBtn.addEventListener("change", function () {
    var fileName = document.getElementById("imageUpload").value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile == "jpg" || extFile == "jpeg" || extFile == "png") {
        customTxt.innerHTML = imageUploadBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    } else {
        customTxt.innerHTML = "No file chosen";
    }
});

//Loader animation while waiting for result
function showSpinner() {
    var spinner = $('#loader');
    spinner.show();
}
function hideSpinner() {
    var spinner = $('#loader');
    spinner.hide();
}


// JS to submit photo
function reqListener() {
    console.log(this.responseText);
}

function submitPhoto(e) {

    // JS to validate the photo file
    var fileName = document.getElementById("imageUpload").value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();

    language = document.querySelector('select[name="languages"]').value;
    // const path_uuid = info_path + "?uuid=" + this.responseText + "?language=" + language;
    // console.log(path_uuid);

    if (extFile == "jpg" || extFile == "jpeg" || extFile == "png") {
        //TO DO
        showSpinner();
        //Send data to RMQ
        let xhr = new XMLHttpRequest();
        let formData = new FormData();
        let photo = e.files[0];

        formData.append("file", photo);

        xhr.onreadystatechange = state => { console.log(xhr.status); } // err handling
        xhr.addEventListener("load", reqListener);
        xhr.open("POST", "/theia/api/v1.0/img_path", true);
        xhr.setRequestHeader("language", language);
        xhr.send(formData);
    } else {
        alert("Invalid image format: Images must be either .jpg or .png");
    }
}

// JS to validate the image URL
var checkValidation = function () {
    var valid = true;
    valid &= checkEmpty('pasteURL', 'error_pasteURL') & checkValidURL('pasteURL', 'error_correctURLImage');

    if (valid) {
        submitURL();
    } else {
        return false;
    }
}

var checkEmpty = function (idValue, idError) {
    var inputText = document.getElementById(idValue).value;

    if (inputText.trim() === '') {
        //URL empty
        document.getElementById(idError).innerHTML = 'URL cannot be empty';
        document.getElementById(idError).style.display = 'block';
        document.getElementById(idError).className = 'alert alert-danger';
        return false;
    } else {
        //URL not empty
        document.getElementById(idError).innerHTML = '';
        document.getElementById(idError).style.display = 'none';
        return true;
    }
}

var checkValidURL = function (idValue, idError) {
    var inputText = document.getElementById(idValue).value;
    var regexURL = /(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|jpeg|png)/ig;

    if (regexURL.test(inputText)) {
        //Valid
        document.getElementById(idError).innerHTML = '';
        document.getElementById(idError).style.display = 'none';
        return true;
    } else {
        //Invalid
        document.getElementById(idError).innerHTML = 'URL need to be an image link';
        document.getElementById(idError).style.display = 'block';
        document.getElementById(idError).className = 'alert alert-danger';
        return false;
    }
}

document.getElementById('btnSubmit').onclick = checkValidation;

// JS to submit image URL
function reqListener() {
    console.log(this.responseText);

    info_path = "/theia/api/v1.0/get_info";
    const path_uuid = info_path + "?uuid=" + this.responseText;
    // language = document.querySelector('select[name="languages"]').value;
    // const path_uuid = info_path + "?uuid=" + this.responseText + "?language=" + language;
    console.log(path_uuid);

    const fetchResult = () => {
        axios({
            url: `${path_uuid}`,
            method: "GET",
            headers: {'Content-Type': 'application/json'},
            timeout: 10000,
        })
        .then((res) => {
                console.log(res);

                uuid = res.data.uuid;
                img_file = res.data.img_file;
                label_list = res.data.label_list;
                nat_sentence = res.data.nat_sentence;
                audio_file_location = res.data.audio_file_location;

                const renderResult = () => {
                    let htmlContent = "";
                    htmlContent =
                        `<center style="padding: 5rem 0;">
                            <div class="container">
                                <h2 style="color:#191970;">RESULTS</h2>
                                <img src="${img_file}" alt="${uuid}" class="container" style="width: 90vw; display:block;">
                                <br>
                                <p>${nat_sentence}</p> 
                                <br>
                                <audio controls><source src="${audio_file_location}"></audio>
                            </div>
                        </center>;`
                    console.log(htmlContent);
                    document.getElementById('showResult').innerHTML = htmlContent;
                    }
                renderResult();
                hideSpinner();
            })
            .catch((err) => {
                console.log(err);

                hideSpinner();
                alert("Sorry something went wrong. Please try again.");
            });
        };

    
    

    fetchResult();
}


function submitURL() {
    language = document.querySelector('select[name="languages"]').value;

    //Prevent the form from submitting and refreshing page on submit
    var form = document.getElementById("myForm");
    function handleForm(event) { event.preventDefault(); }
    form.addEventListener('submit', handleForm);
    showSpinner();

    //Send data to RMQ
    const img_url = document.querySelector('#pasteURL').value;

    const xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open('POST', '/theia/api/v1.0/img_url', true);
    xhr.setRequestHeader('Content-Type', 'plain/text');
    xhr.setRequestHeader("language", language);
    xhr.send(img_url);
}
    



    