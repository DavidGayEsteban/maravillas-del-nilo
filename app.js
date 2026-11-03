// Mejora progresiva: lectura en voz alta del vocabulario árabe.
// La navegación por pestañas NO depende de este script (es CSS puro).
(function(){
  if(!('speechSynthesis' in window)) return;
  var arabicVoice = null;
  function pickVoice(){
    var voices = window.speechSynthesis.getVoices();
    arabicVoice = null;
    for (var i = 0; i < voices.length; i++) {
      var l = (voices[i].lang || '').toLowerCase();
      if (l.indexOf('ar-eg') === 0) { arabicVoice = voices[i]; break; }
      if (l.indexOf('ar') === 0 && !arabicVoice) arabicVoice = voices[i];
    }
  }
  pickVoice();
  window.speechSynthesis.onvoiceschanged = pickVoice;
  window.speakArabic = function(text, btn){
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = arabicVoice ? arabicVoice.lang : 'ar-EG';
    if(arabicVoice) u.voice = arabicVoice;
    u.rate = 0.85;
    if(btn){
      btn.classList.add('playing');
      u.onend = function(){ btn.classList.remove('playing'); };
      u.onerror = function(){ btn.classList.remove('playing'); };
    }
    window.speechSynthesis.speak(u);
  };
  // Al cambiar de pestaña, volver arriba
  var radios = document.querySelectorAll('.tab-radio');
  for (var r = 0; r < radios.length; r++) {
    radios[r].addEventListener('change', function(){ window.scrollTo(0, 0); });
  }
})();
