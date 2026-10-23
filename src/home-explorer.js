/* Progressive enhancement: every example remains readable without JavaScript. */
(() => {
  document.querySelectorAll('[data-explorer]').forEach(root => {
    const choices = [...root.querySelectorAll('[data-choice]')];
    const panels = choices.map(choice => root.querySelector('#' + choice.dataset.choice));
    if (panels.some(panel => !panel)) return;
    const select = index => {
      choices.forEach((choice, i) => {
        choice.setAttribute('aria-current', String(i === index));
        choice.setAttribute('aria-controls', panels[i].id);
        panels[i].hidden = i !== index;
      });
    };
    root.classList.add('is-enhanced');
    const initial = panels.findIndex(panel => '#' + panel.id === location.hash);
    select(initial < 0 ? 0 : initial);
    choices.forEach((choice, i) => {
      choice.addEventListener('click', event => {
        event.preventDefault();
        select(i);
      });
      choice.addEventListener('keydown', event => {
        const next = {ArrowDown: (i + 1) % choices.length, ArrowRight: (i + 1) % choices.length,
          ArrowUp: (i + choices.length - 1) % choices.length, ArrowLeft: (i + choices.length - 1) % choices.length,
          Home: 0, End: choices.length - 1}[event.key];
        if (next === undefined) return;
        event.preventDefault(); select(next); choices[next].focus();
      });
    });
    // Links and history can still address a specific example directly.
    window.addEventListener('hashchange', () => {
      const index = panels.findIndex(panel => '#' + panel.id === location.hash);
      if (index >= 0) select(index);
    });
  });
})();
