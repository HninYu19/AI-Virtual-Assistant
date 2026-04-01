$(document).ready(function() {
  console.log('controller.js loaded successfully');

  // Variable to track if we should stay in SiriWave
  window.stayInSiriWave = true;

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
    eel.expose(setStayInSiriWave);
    eel.expose(goToMainScreen);
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

  // Display Speak Message with wrapping
  function DisplayMessage(message) {
    console.log('DisplayMessage called:', message);
    if (message && message.trim() !== '') {
      try {
        // Format message with line breaks for better display
        var formattedMessage = formatMessageForDisplay(message);

        if ($('.siri-message .texts li').length > 0) {
          $('.siri-message .texts li').html(formattedMessage);
          $('.siri-message').textillate('start');
        } else {
          $('.siri-message').html(formattedMessage);
        }

        // Auto-adjust font size for long messages
        adjustFontSize($('.siri-message'), message.length);

      } catch (e) {
        console.error('Error in DisplayMessage:', e);
        $('.siri-message').html(escapeHtml(message));
      }
    }
  }

  // Format message with line breaks
  function formatMessageForDisplay(message, maxLineLength = 50) {
    if (!message) return '';

    // Split into words
    var words = message.split(' ');
    var lines = [];
    var currentLine = '';

    for (var i = 0; i < words.length; i++) {
      if ((currentLine + words[i]).length > maxLineLength) {
        lines.push(currentLine.trim());
        currentLine = words[i] + ' ';
      } else {
        currentLine += words[i] + ' ';
      }
    }

    if (currentLine.trim()) {
      lines.push(currentLine.trim());
    }

    return lines.join('<br>');
  }

  // Adjust font size based on message length
  function adjustFontSize(element, messageLength) {
    if (messageLength > 200) {
      element.css('font-size', '16px');
    } else if (messageLength > 100) {
      element.css('font-size', '18px');
    } else {
      element.css('font-size', '24px');
    }
  }

  // Show message with improved formatting
  function show_message(message) {
    console.log('show_message called:', message);
    if (message && message.trim() !== '') {
      var formattedMessage = formatMessageForDisplay(message);
      $('.siri-message').html(formattedMessage);
      adjustFontSize($('.siri-message'), message.length);
      console.log('Message updated to:', formattedMessage);
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
    $('.siri-message').html('How can I help you?');
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
      $('.siri-message').html('Ready for next command');
    }
  }

  // Enhanced sender text with better formatting
  function senderText(message) {
    console.log('senderText called:', message);
    if (message && message.trim() !== '') {
      var chatBox = document.getElementById('chat-canvas-body');
      if (chatBox) {
        var formattedMessage = formatMessageForDisplay(message, 40);
        chatBox.innerHTML += `<div class="row justify-content-end mb-4">
          <div class="width-size">
            <div class="sender_message" style="white-space: pre-wrap; word-wrap: break-word;">${
            escapeHtml(formattedMessage)}</div>
          </div>
        </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }
  }

  // Enhanced receiver text with better formatting and scrolling
  function receiverText(message) {
    console.log('receiverText called:', message);
    if (message && message.trim() !== '') {
      var chatBox = document.getElementById('chat-canvas-body');
      if (chatBox) {
        var formattedMessage = formatMessageForDisplay(message, 40);
        chatBox.innerHTML += `<div class="row justify-content-start mb-4">
          <div class="width-size">
            <div class="receiver_message" style="white-space: pre-wrap; word-wrap: break-word; max-width: 100%;">${
            escapeHtml(formattedMessage)}</div>
          </div>
        </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }

      if (!$('#SiriWave').attr('hidden')) {
        var siriFormattedMessage = formatMessageForDisplay(message, 50);
        $('.siri-message').html(siriFormattedMessage);
        adjustFontSize($('.siri-message'), message.length);

        // Auto-scroll siri message if needed
        if ($('.siri-message').height() > 100) {
          $('.siri-message')
              .css('overflow-y', 'auto')
              .css('max-height', '150px');
        }
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

// Pagination variables
var currentResponseChunk = 0;
var responseChunks = [];

function receiverText(message) {
  console.log('receiverText called:', message);
  if (message && message.trim() !== '') {
    var chatBox = document.getElementById('chat-canvas-body');
    if (chatBox) {
      var formattedMessage = formatMessageForDisplay(message, 40);

      // Check if this is a paginated message
      var isPaginated = message.includes('Say \'continue\' to read more') ||
          message.includes('More available');

      chatBox.innerHTML += `<div class="row justify-content-start mb-4">
                <div class="width-size">
                    <div class="receiver_message" style="white-space: pre-wrap; word-wrap: break-word; max-width: 100%;">
                        ${escapeHtml(formattedMessage)}
                        ${
          isPaginated ?
              '<br><br><button class="continue-reading-btn" onclick="requestMore()">Continue Reading ▶</button>' :
              ''}
                    </div>
                </div>
            </div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (!$('#SiriWave').attr('hidden')) {
      var siriFormattedMessage = formatMessageForDisplay(message, 50);
      $('.siri-message').html(siriFormattedMessage);
      adjustFontSize($('.siri-message'), message.length);

      // Auto-scroll siri message if needed
      if ($('.siri-message').height() > 100) {
        $('.siri-message').css('overflow-y', 'auto').css('max-height', '150px');
      }
    }
  }
}

// Function to request more content
function requestMore() {
  console.log('Requesting more content...');
  if (typeof eel !== 'undefined') {
    eel.all_commands('continue')()
        .then(function(result) {
          console.log('Continue command sent');
        })
        .catch(function(error) {
          console.error('Error sending continue command:', error);
        });
  }
}

// Global function for button click
window.requestMore = requestMore;