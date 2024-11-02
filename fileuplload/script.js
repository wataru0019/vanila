document.addEventListener('DOMContentLoaded', function(){
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const preview = document.getElementById('preview');

    dropZone.addEventListener('dragover', function(e){
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', function(e){
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', function(e){
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if(files.length > 0){
            fileInput.files = files;
            preview.textContent = files[0].name;
        }
        console.log(files[0].name)
    });

    uploadForm.addEventListener('submit', async function(e){
        e.preventDefault();
        const formData = new FormData(uploadForm);
        try {
            const response = await fetch(uploadForm.action, {
                method: 'POST',
                body: formData
            });
            if(!response.ok){
                throw new Error('Network response was not ok');
            }
            const result = await response.json();
            console.log(result);
            alert("ファイルがアップロードされました")
        } catch (error) {
            console.log(error);
        }
    })
})