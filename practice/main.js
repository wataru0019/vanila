const content = document.getElementById('content');
const loading = document.getElementById('loading');
// document.addEventListener('readystatechange', function(){
//     if(document.readyState === 'loading'){
//         console.log('loading');
//         alert('loading');
//         setTimeout(function(){
//             content.innerHTML = 'Content';
//         }, 2000);
//     } else if(document.readyState === 'complete'){
//         console.log('complete');
//         loading.classList.add('hidden');
//     }})
document.addEventListener("readystatechange", () => {
    console.log(`現在の readyState は: ${document.readyState}`);
});