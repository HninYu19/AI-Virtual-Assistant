$(document).ready(function() {
  console.log('main.js loaded - DOM ready');

  // Variable to track SiriWave mode
  window.stayInSiriWave = true;

  // Check if required plugins exist
  if (typeof $.fn.textillate === 'undefined') {
    console.error('textillate plugin not loaded!');
  } else {
    console.log('textillate plugin loaded');
  }

  // Check if eel is available
  if (typeof eel !== 'undefined') {
    console.log('✓ Eel is available in main.js');
  } else {
    console.error('✗ Eel is NOT available in main.js!');
  }

  // Test Eel connection
  if (typeof eel !== 'undefined' && eel.test_connection) {
    eel.test_connection()()
        .then(response => {
          console.log('✓ Eel connection test successful:', response);
        })
        .catch(error => {
          console.error('✗ Eel connection test failed:', error);
        });
  }

  // Initialize textillate
  if (typeof $.fn.textillate !== 'undefined') {
    try {
      $('.text').textillate({
        loop: true,
        sync: true,
        in: {
          effect: 'bounceIn',
        },
        out: {
          effect: 'bounceOut',
        },
      });

      $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
          effect: 'fadeInUp',
          sync: true,
        },
        out: {
          effect: 'fadeOutUp',
          sync: true,
        },
      });
      console.log('Textillate initialized');
    } catch (e) {
      console.error('Textillate initialization error:', e);
    }
  }

  // Siri Wave Configuration
  var siriWave = null;
  try {
    siriWave = new SiriWave({
      container: document.getElementById('siri-container'),
      width: 800,
      height: 200,
      style: 'ios9',
      amplitude: '1',
      speed: '0.3',
      autostart: true,
    });
    console.log('✓ SiriWave initialized');
  } catch (e) {
    console.error('SiriWave initialization error:', e);
  }

  // MIC BUTTON CLICK HANDLER
  $('#MicBtn').click(function(e) {
    console.log('🔴 Mic button clicked!');
    e.preventDefault();

    if (typeof eel === 'undefined') {
      console.error('Cannot process click - eel not available!');
      return;
    }

    // Play sound
    try {
      console.log('Calling play_sound...');
      eel.play_sound();
    } catch (err) {
      console.error('Error calling play_sound:', err);
    }

    // Show SiriWave and stay there
    console.log('Showing SiriWave, hiding Oval');
    $('#Oval').attr('hidden', true);
    $('#SiriWave').attr('hidden', false);
    window.stayInSiriWave = true;
    $('.siri-message').text('Listening...');

    // Restart SiriWave animation
    if (siriWave) {
      siriWave.start();
      console.log('SiriWave animation restarted');
    }

    // Call the command handler
    console.log('Calling eel.all_commands()...');
    try {
      eel.all_commands()()
          .then(function(result) {
            console.log('all_commands completed:', result);
            // Don't hide SiriWave - stay for next command
            $('.siri-message').text('Ready for next command');
          })
          .catch(function(error) {
            console.error('all_commands error:', error);
            $('.siri-message').text('Error occurred. Try again.');
          });
    } catch (err) {
      console.error('Error calling all_commands:', err);
      $('.siri-message').text('Error occurred');
    }
  });

  // Keyboard shortcut (Win+J)
  function doc_keyUp(e) {
    console.log('Key pressed:', e.key, 'MetaKey:', e.metaKey);
    if (e.key == 'j' && e.metaKey) {
      console.log('🔴 Hotkey detected: Win+J');
      e.preventDefault();
      if (typeof eel !== 'undefined') {
        eel.play_sound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        window.stayInSiriWave = true;
        $('.siri-message').text('Listening...');
        eel.all_commands()();
      }
    }
  }
  document.addEventListener('keyup', doc_keyUp, false);

  // Play Assistant function for text input
  function PlayAssistant(message) {
    console.log('PlayAssistant called with message:', message);
    if (message != '' && typeof eel !== 'undefined') {
      // Show SiriWave and stay there
      $('#Oval').attr('hidden', true);
      $('#SiriWave').attr('hidden', false);
      window.stayInSiriWave = true;
      $('.siri-message').text(`Processing: ${message}`);

      // Call the command
      eel.all_commands(message);

      // Clear input and reset buttons
      $('#chatbox').val('');
      $('#MicBtn').attr('hidden', false);
      $('#SendBtn').attr('hidden', true);
    }
  }

  function ShowHideButtons(message) {
    if (message.length == 0) {
      $('#MicBtn').attr('hidden', false);
      $('#SendBtn').attr('hidden', true);
    } else {
      $('#MicBtn').attr('hidden', true);
      $('#SendBtn').attr('hidden', false);
    }
  }

  $('#chatbox').keyup(function() {
    let message = $('#chatbox').val();
    ShowHideButtons(message);
  });

  $('#SendBtn').click(function() {
    let message = $('#chatbox').val();
    PlayAssistant(message);
  });

  $('#chatbox').keypress(function(e) {
    key = e.which;
    if (key == 13) {
      let message = $('#chatbox').val();
      PlayAssistant(message);
    }
  });

  console.log('✓ main.js initialization complete');
});