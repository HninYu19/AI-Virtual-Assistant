$(document).ready(function() {
  // Start face authentication when page loads
  setTimeout(function() {
    startFaceAuthentication();
  }, 1000);

  function startFaceAuthentication() {
    console.log('Starting face authentication...');

    // Show loader, hide others
    $('#Loader').attr('hidden', false);
    $('#FaceAuth').attr('hidden', true);
    $('#FaceAuthSuccess').attr('hidden', true);
    $('#HelloGreet').attr('hidden', true);

    // Call Python authentication function
    eel.start_authentication()(function(result) {
      console.log('Authentication result:', result);

      if (result.success) {
        // Authentication successful - show success animations
        console.log('Authentication successful!');

        // Hide loader, show face auth animation
        $('#Loader').attr('hidden', true);
        $('#FaceAuth').attr('hidden', false);

        setTimeout(function() {
          // Hide face auth, show success animation
          $('#FaceAuth').attr('hidden', true);
          $('#FaceAuthSuccess').attr('hidden', false);
        }, 2000);

        setTimeout(function() {
          // Hide success, show greeting
          $('#FaceAuthSuccess').attr('hidden', true);
          $('#HelloGreet').attr('hidden', false);
        }, 3000);

        setTimeout(function() {
          // Hide start page and show main interface
          $('#Start').attr('hidden', true);
          $('#Oval').attr('hidden', false);
          $('#Oval').addClass('animate__animated animate__zoomIn');
        }, 5000);

        // Close camera after authentication
        eel.close_camera();

      } else {
        // Authentication failed
        console.log('Authentication failed!');
        alert('Face Authentication Failed! Please try again.');

        // Reset and try again
        setTimeout(function() {
          startFaceAuthentication();
        }, 2000);
      }
    });
  }

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

  // Siri Wave Configuration
  var siriWave = new SiriWave({
    container: document.getElementById('siri-container'),
    width: 800,
    height: 200,
    style: 'ios9',
    amplitude: '1',
    speed: '0.3',
    autostart: true,
  });

  // Siri message animation
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

  // mic click
  $('#MicBtn').click(function() {
    eel.play_sound();
    $('#Oval').attr('hidden', true);
    $('#SiriWave').attr('hidden', false);
    eel.all_commands()()
  });

  function doc_keyUp(e) {
    if (e.key == 'j' && e.metaKey) {
      eel.play_sound();
      $('#Oval').attr('hidden', true);
      $('#SiriWave').attr('hidden', false);
      eel.all_commands()();
    }
  }
  document.addEventListener('keyup', doc_keyUp, false);

  function PlayAssistant(message) {
    if (message != '') {
      $('#Oval').attr('hidden', true);
      $('#SiriWave').attr('hidden', false);
      eel.all_commands(message);
      $('#chatbox').val('');
      $('#MicBtn').attr('hidden', false);
      $('#ChatBtn').attr('hidden', true);
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
});