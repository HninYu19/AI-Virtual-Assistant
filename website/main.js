$(document).ready(function() {
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
});