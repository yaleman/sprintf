
async function sendquery() {
    // grab the form value
    let formatstring = $('input#formatstring').first().val();
    $('#results').html("Loading...");

    // make the call
    let response = await fetch("/parse", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({ "formatstring": formatstring}),
        });
    // wait for the call
    let result = await response.json();
    $('#results').val(result.result);

    // update the url to match the current input
    let currentURL = new URL(window.location.href);
    currentURL.searchParams.delete('f');
    currentURL.searchParams.append('f',formatstring);
    history.pushState({
        id: 'sprintf',
        source: 'web'
    }, 'sprintf', currentURL.toString());
}

function copyFormatString() {
    let formatstring = $('input#formatstring').first().val();
    navigator.clipboard.writeText(formatstring);
    console.log("Copied "+formatstring+" to the clipboard");

}

// runs on page load
$().loaded(function(){
    $('#formatstring').on('keyup',sendquery);
    $('#copy').on('click', copyFormatString);
    sendquery();
})
