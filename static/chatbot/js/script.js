// Handle form submission
let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$("#chatform").on('submit', function(e) {
    e.preventDefault();
    let message = $("#query_sent").val();

    // Append the user's message to the chatbox immediately after 'Submit' is clicked
    $("#chatbox").append('<div class="user-message"><span>' + message + '</span><i class="fas fa-user fa-lg"></i></div>');
    $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);

    $.ajax({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: '/get-response/',
        data: {'query_sent': message},
        type: 'POST',
        success: function(response) {
            // Append the bot's response to the chatbox
            $("#chatbox").append('<div class="bot-message"><i class="fas fa-robot fa-lg"></i><span>' + response.Response + '</span></div>');
            // Scroll to the bottom of the chatbox
            $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
        }
    });
    // Clear the input field and reset the form
    $("#query_sent").val('');
    $("#chatform")[0].reset();
});
// Add an event listener to the 'New Chat' button
$(".new-chat-button").on('click', function() {
    // Clear the chatbox
    $("#chatbox").empty();
    // Add the initial bot message to the new chat
    $("#chatbox").append('<div class="bot-message"><i class="fas fa-robot fa-lg"></i><span>Hey! How can i help you?</span></div>');
});

