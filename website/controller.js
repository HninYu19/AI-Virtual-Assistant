$(document).ready(function() {
  // Show Spoken Message
  eel.expose(show_message);
  function show_message(message) {
    $('.siri-message li:first').text(message);
    $('.siri-message').textillate('start');
  }

  // show hood
  eel.expose(show_hood);
  function show_hood() {
    $('#Oval').attr('hidden', false);
    $('#SiriWave').attr('hidden', true);
  }
});