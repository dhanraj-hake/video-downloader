
function downloadVideo(url,name) {
    console.log(`/proxy/?url=${(url)}`)
    fetch(`/proxy/`,{
        method: 'POST',
        body : JSON.stringify({url:url})
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const fileName = name+ '.mp4'; 
            saveAs(blob, fileName);
        })
        .catch(error => {
            console.error('Download failed:', error);
        });
}