$(document).ready(function() {
  console.log('controller.js loaded successfully');

  // Check if Eel is available
  if (typeof eel !== 'undefined') {
    console.log('Eel is available in controller.js');
  } else {
    console.error('Eel not loaded in controller.js!');
  }

  // Display Speak Message
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    console.log('DisplayMessage called:', message);
    if (message && message.trim() !== '') {
      try {
        // Replace the hidden textillate <li>
        $('.siri-message .texts li').text(message);
        // Re-initialize textillate so it splits into chars again
        $('.siri-message').textillate('start');
      } catch (e) {
        console.error('Error in DisplayMessage:', e);
      }
    }
  }

  // Display hood
  eel.expose(ShowHood);
  function ShowHood() {
    console.log('ShowHood called');
    $('#Oval').attr('hidden', false);
    $('#SiriWave').attr('hidden', true);
  }

  eel.expose(senderText);
  function senderText(message) {
    console.log('senderText called:', message);
    if (message && message.trim() !== '') {
      var chatBox = document.getElementById('chat-canvas-body');
      if (chatBox) {
        chatBox.innerHTML += `<div class="row justify-content-end mb-4">
          <div class="width-size">
            <div class="sender_message">${escapeHtml(message)}</div>
          </div>
        </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }
  }

  eel.expose(receiverText);
  function receiverText(message) {
    console.log('receiverText called:', message);
    if (message && message.trim() !== '') {
      var chatBox = document.getElementById('chat-canvas-body');
      if (chatBox) {
        chatBox.innerHTML += `<div class="row justify-content-start mb-4">
          <div class="width-size">
            <div class="receiver_message">${escapeHtml(message)}</div>
          </div>
        </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }
  }

  // Hide Loader and display Face Auth animation
  eel.expose(hideLoader);
  function hideLoader() {
    console.log('hideLoader called');
    $('#Loader').attr('hidden', true);
    $('#FaceAuth').attr('hidden', false);
  }

  // Hide Face auth and display Face Auth success animation
  eel.expose(hideFaceAuth);
  function hideFaceAuth() {
    console.log('hideFaceAuth called');
    $('#FaceAuth').attr('hidden', true);
    $('#FaceAuthSuccess').attr('hidden', false);
  }

  // Hide success and display
  eel.expose(hideFaceAuthSuccess);
  function hideFaceAuthSuccess() {
    console.log('hideFaceAuthSuccess called');
    $('#FaceAuthSuccess').attr('hidden', true);
    $('#HelloGreet').attr('hidden', false);
  }

  // Hide Start Page and display blob
  eel.expose(hideStart);
  function hideStart() {
    console.log('hideStart called');
    $('#Start').attr('hidden', true);
    setTimeout(function() {
      $('#Oval').addClass('animate__animated animate__zoomIn');
      $('#Oval').attr('hidden', false);
    }, 1000);
  }

  // Helper function to escape HTML
  function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  console.log('controller.js initialization complete');
});