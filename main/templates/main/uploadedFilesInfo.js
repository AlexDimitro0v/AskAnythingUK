{% load static %}

let totalSize = 0;
let numOfFiles;
// Array of all selected files
let selectedFiles = [];

function updateNumOfFiles() {
  $("#fileCount").text(numOfFiles == 1 ? "1 file" : numOfFiles + " files");
}

$("input[name=feedbackfiles]").change(function() {
  $('#allFiles').empty();
  selectedFiles = Array.from(document.getElementById("file-upload").files);
  numOfFiles = selectedFiles.length;
  totalSize = 0;

  for (var i = 0; i < numOfFiles; ++i) {
      totalSize += selectedFiles[i].size;
      let fileName = $(this).get(0).files[i].name;
      let extension = fileName.split("").reverse().join("").split(".")[0].split("").reverse().join("").substring(0,4).toUpperCase();
      $('#allFiles').append("<div title='Click to remove file' id='container"+i+"' class='file-container noselect'><img  style='width: 40px' src='{% static 'img/fileicon.png' %}'/><span class='file-extension'>"+extension+"</span><p class='file-p'>"+ fileName.substring(0,20) +"</p></div>");

      // Remove file on click
      $('#container'+i).click(function(e) {
        let i = $(this).attr('id').substring(9,$(this).attr('id').length);
        totalSize -= selectedFiles[i].size;

        selectedFiles[i] = null;
        $("#fileSize").text(formatBytes(totalSize));

        numOfFiles -=1;
        updateNumOfFiles();
        $(this).remove();
      });
  }

  $("#fileSize").text(formatBytes(totalSize));
  updateNumOfFiles();
});
