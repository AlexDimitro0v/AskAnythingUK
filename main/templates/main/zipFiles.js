let zip = new JSZip();
// Add all uploaded files to ZIP
function addFileToZip(n) {
    if(n >= nonNullSelectedFiles.length) {
       zip.generateAsync({type:"blob"}).then(function(content) {
           let files = new File([content], "feedbackFiles.zip");
           let formData = new FormData(document.querySelector('#'+fileFormName));
           formData.append('fileZip', files);
           formData.delete('feedbackfiles');

           let xhr = new XMLHttpRequest();
           const Toast = Swal.mixin({
              toast: true,
              position: 'bottom-end',
              showConfirmButton: false,
              timer: 1500,
              timerProgressBar: true,
              onOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
              }
           })

           Toast.fire({
              icon: 'success',
              title: 'Your request has been processed'
           })
           xhr.onreadystatechange = function() {
               if(xhr.readyState == 4 && xhr.status == 200) {
               window.setTimeout(function(){
                   window.location.href = "/dashboard/";
               }, 10);
               }
           }
           xhr.open('POST', postAction, true);
           xhr.send(formData);
     });
   }
   else {
     let fileReader = new FileReader();
     fileReader.onload = function() {
         zip.file(nonNullSelectedFiles[n].name, this.result);
         addFileToZip(n + 1);
     };
     fileReader.readAsArrayBuffer(nonNullSelectedFiles[n]);
   }
}
addFileToZip(0);
