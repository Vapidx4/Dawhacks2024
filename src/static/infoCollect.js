// Assuming you have a JSON object called jsonResponse

// Accessing values by keys
var isHealthy = jsonResponse["isHealthy"];
var isPlant = jsonResponse["isPlant"];
var name = jsonResponse["classification"]["name"];
var nameProb = jsonResponse["classification"]["probability"];
var similarImg = jsonResponse["similarImages"]["similarImage"];
var similarImgProb = jsonResponse["similarImages"]["probability"];
var disease = jsonResponse["diseases"]["disease"];
var diseaseProb = jsonResponse["diseases"]["probability"];



// document.getElementById('selectBtn').addEventListener('click', function () {
//     let input = document.createElement('input');
//     input.type = 'file';
//     input.accept = 'image/*'; // Accept only image files
//     input.onchange = function (event) {
//         let files = event.target.files;
//         if (files.length > 0) {
//             let selectedImage = files[0];
//             console.log('Selected image:', selectedImage);
//             // Getting the file location of the chosen image
//             const reader = new FileReader();
//             reader.onload = function (event) {
//                 const imageLocation = event.target.result;
//             }
//         reader.readAsDataURL(selectedImage);
//         document.getElementById('output').innerHTML = 'Image Location: ${imageLocation}';
//         }
//     };
//     input.click();
// });