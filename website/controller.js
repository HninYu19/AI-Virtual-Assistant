$(document).ready(function() {
  console.log('controller.js loaded successfully');

  // Variable to track if we should stay in SiriWave
  window.stayInSiriWave = true;  // Default to stay in SiriWave

  // Check if Eel is available
  if (typeof eel !== 'undefined') {
    console.log('✓ Eel is available in controller.js');

    // Expose functions to Python
    eel.expose(DisplayMessage);
    eel.expose(ShowHood);
    eel.expose(ShowSiriWave);
    eel.expose(senderText);
    eel.expose(receiverText);
    eel.expose(hideLoader);
    eel.expose(hideFaceAuth);
    eel.expose(hideFaceAuthSuccess);
    eel.expose(hideStart);
    eel.expose(hide_siri_wave);
    eel.expose(show_message);
    eel.expose(show_hood);
    eel.expose(setStayInSiriWave);  // New function
    eel.expose(goToMainScreen);  // New function to manually go to main screen
  } else {
    console.error('✗ Eel not loaded in controller.js!');
  }

  // Set whether to stay in SiriWave mode
  function setStayInSiriWave(stay) {
    console.log('setStayInSiriWave called:', stay);
    window.stayInSiriWave = stay;
  }

  // Manually go to main screen
  function goToMainScreen() {
    console.log('goToMainScreen called - returning to main screen');
    window.stayInSiriWave = false;
    $('#SiriWave').attr('hidden', true);
    $('#Oval').attr('hidden', false);
    // Reset after going back
    setTimeout(() => {
      window.stayInSiriWave = true;
    }, 1000);
  }

  // Display Speak Message
  function DisplayMessage(message) {
    console.log('DisplayMessage called:', message);
    if (message && message.trim() !== '') {
      try {
        if ($('.siri-message .texts li').length > 0) {
          $('.siri-message .texts li').text(message);
          $('.siri-message').textillate('start');
        } else {
          $('.siri-message').text(message);
        }
      } catch (e) {
        console.error('Error in DisplayMessage:', e);
        $('.siri-message').text(message);
      }
    }
  }

  // Show message
  function show_message(message) {
    console.log('show_message called:', message);
    if (message && message.trim() !== '') {
      $('.siri-message').text(message);
      console.log('Message updated to:', message);
    }
  }

  // Show Oval
  function ShowHood() {
    console.log('ShowHood called - showing Oval');
    $('#SiriWave').attr('hidden', true);
    $('#Oval').attr('hidden', false);
  }

  // Show SiriWave
  function ShowSiriWave() {
    console.log('ShowSiriWave called - showing SiriWave');
    $('#Oval').attr('hidden', true);
    $('#SiriWave').attr('hidden', false);
    $('.siri-message').text('How can I help you?');
    console.log('SiriWave is now visible');
  }

  // Show hood
  function show_hood() {
    console.log('show_hood called - showing Oval');
    $('#SiriWave').attr('hidden', true);
    $('#Oval').attr('hidden', false);
  }

  // Hide SiriWave and show Oval - only if not staying in SiriWave
  function hide_siri_wave() {
    console.log(
        'hide_siri_wave called, stayInSiriWave:', window.stayInSiriWave);
    if (!window.stayInSiriWave) {
      $('#SiriWave').attr('hidden', true);
      $('#Oval').attr('hidden', false);
    } else {
      console.log('Staying in SiriWave mode');
      // Just clear the message but stay in SiriWave
      $('.siri-message').text('Ready for next command');
    }
  }

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

      if (!$('#SiriWave').attr('hidden')) {
        $('.siri-message').text(message);
      }
    }
  }

  function hideLoader() {
    console.log('hideLoader called');
    $('#Loader').attr('hidden', true);
    $('#FaceAuth').attr('hidden', false);
  }

  function hideFaceAuth() {
    console.log('hideFaceAuth called');
    $('#FaceAuth').attr('hidden', true);
    $('#FaceAuthSuccess').attr('hidden', false);
  }

  function hideFaceAuthSuccess() {
    console.log('hideFaceAuthSuccess called');
    $('#FaceAuthSuccess').attr('hidden', true);
    $('#HelloGreet').attr('hidden', false);
  }

  function hideStart() {
    console.log('hideStart called');
    $('#Start').attr('hidden', true);
    setTimeout(function() {
      $('#Oval').addClass('animate__animated animate__zoomIn');
      $('#Oval').attr('hidden', false);
    }, 1000);
  }

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  if (typeof eel !== 'undefined') {
    try {
      eel.init()()
          .then(function() {
            console.log('✓ eel.init() completed successfully');
          })
          .catch(function(error) {
            console.error('✗ eel.init() failed:', error);
          });
    } catch (err) {
      console.error('Error calling eel.init():', err);
    }
  }

  console.log('✓ controller.js initialization complete');
});