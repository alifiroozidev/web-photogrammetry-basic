// Wait until the content of the DOM has loaded and parsed. This does
// not wait on stylesheets, images, or subframes
window.addEventListener('DOMContentLoaded', () => {

    // Find the container and form
    const container = document.querySelector('.uk-container');
    const form = document.querySelector('form');
    const stdout = document.querySelector('code');

    // Start a websocket connection. This websocket connection allows us to
    // ping the backend and start an actual meshroom process. This process
    // also streams the process' stdout over the connection
    const websocket = new WebSocket('ws://127.0.0.1:5678');

    // Listen to incoming messages, which we want to stream the stdout element
    websocket.onmessage = (event) => {

        // Get the text from the blob
        event.data.text().then((text) => {

            // And update the stdout
            stdout.textContent = stdout.textContent + text;
        });
    };

    // Fetch the default configuration of meshroom from the API
    fetch('/config').then((res) => {

        // Fetch the text and load it into the form
        res.text().then((text) => {

            // Set the text on the form field that holds the json configuration
            form.querySelector('textarea').textContent = text;
        });
    });

    // Listen until the user submits the form
    form.addEventListener('submit', (event) => {

        // Prevent the default behavior as we don't want the browser
        // redirect the user
        event.preventDefault();

        // Create form data from the form
        const formdata = new FormData(form);
        form.classList.remove('uk-form-danger');

        // Show a loading animation
        const overlay = container.appendChild(document.createElement('div'));
        overlay.classList.add('uk-overlay', 'uk-position-center');
        const loader = overlay.appendChild(document.createElement('div'));
        loader.setAttribute('uk-spinner', true);

        // List of promises that are required to run meshroom
        const promises = [
            fetch('/upload', {
                method: 'POST',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                body: formdata
            }),
            fetch('/config', {
                method: 'POST',
                mode: 'cors',
                credentials: 'same-origin',
                body: formdata
            })
        ];

        // Make a post request to upload the images
        Promise.all(promises).then(() => {

            // Remove the loader
            overlay.remove();

            // Inform the user
            UIkit.notification({
                message: 'Meshroom has started',
                status: 'success',
                pos: 'bottom-right',
                timeout: 3000
            });

            // Refresh the view to show the progress of the meshroom progress
            websocket.send(JSON.stringify({ type: 'run' }));
        }).catch((err) => {

            console.log(err);
            // Remove the loader
            overlay.remove();

            // Something went wrong, so we need to inform the user
            form.classList.add('uk-form-danger');
            UIkit.notification({
                message: 'Files could not be uploaded',
                status: 'danger',
                pos: 'bottom-right',
                timeout: 3000
            });
        });
    });
});