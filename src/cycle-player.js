/* The six stages advance together with their explanation. CRM is manual context. */
(function (global) {
 'use strict';
 const AUTO_MS = 4000, READ_MS = 18000, LEAVE_MS = 1500;

 // One cancellable timer, with the unspent reading time preserved on every pause.
 function createPlayback({now = () => performance.now(), setTimer = setTimeout,
   clearTimer = clearTimeout, onAdvance, onState = () => {}}) {
  const reasons = new Set(['offscreen']);
  let timer = null, kind = '', deadline = 0, remaining = AUTO_MS;
  let duration = AUTO_MS, delay = 0, destroyed = false;
  function snapshot() {
   const left = timer !== null && kind === 'advance' ? Math.max(0, deadline - now()) : remaining;
   return {remaining: left, duration, running: timer !== null && kind === 'advance',
    waiting: timer !== null && kind === 'resume', reasons: [...reasons]};
  }
  function freeze() {
   if (timer === null) return;
   if (kind === 'advance') remaining = Math.max(0, deadline - now());
   else delay = Math.max(0, deadline - now());
   clearTimer(timer); timer = null; kind = '';
  }
  function run() {
   if (destroyed) return;
   if (!reasons.size && timer === null) {
    kind = delay > 0 ? 'resume' : 'advance';
    const wait = delay > 0 ? delay : remaining;
    deadline = now() + wait;
    timer = setTimer(() => {
     const wasDelay = kind === 'resume'; timer = null; kind = '';
     if (wasDelay) delay = 0;
     else {remaining = duration = AUTO_MS; onAdvance();}
     run();
    }, wait);
   }
   onState(snapshot());
  }
  return {
   snapshot,
   setPaused(reason, paused, resumeDelay = 0) {
    if (destroyed || reasons.has(reason) === paused) return;
    freeze();
    if (paused) reasons.add(reason);
    else {reasons.delete(reason); delay = Math.max(delay, resumeDelay);}
    run();
   },
   hold() {
    if (destroyed) return;
    freeze(); remaining = duration = READ_MS; run();
   },
   destroy() {freeze(); destroyed = true;}
  };
 }

 function mount(cycle) {
  const buttons = [...cycle.querySelectorAll('[data-cycle-step]')];
  const stages = buttons.filter(b => b.classList.contains('cycle-node'));
  const wheel = cycle.querySelector('.cycle-wheel');
  const details = cycle.querySelector('.cycle-details');
  const zones = [cycle.querySelector('.cycle-visual'), details];
  const panels = buttons.map(b => document.getElementById(b.getAttribute('aria-controls')));
  const paths = [...cycle.querySelectorAll('[data-cycle-flow]')];
  const toggle = cycle.querySelector('[data-cycle-playback-toggle]');
  const hint = cycle.querySelector('[data-cycle-static-hint]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const abort = new AbortController();
  const listen = (target, type, fn) => target.addEventListener(type, fn, {signal: abort.signal});
  let selected = buttons.find(b => b.getAttribute('aria-selected') === 'true') || stages[0];
  let lastStage = Math.max(0, stages.indexOf(selected));
  let keyboard = false, userPaused = false, animation = null, measureFrame = null;
  let disposed = false, lastWidth = -1;
  const inside = node => node instanceof Node && zones.some(zone => zone.contains(node));

  function select(button, automatic = false) {
   const previousStage = lastStage;
   selected = button;
   if (stages.includes(button)) lastStage = stages.indexOf(button);
   for (let i = 0; i < buttons.length; i++) {
    const active = buttons[i] === button;
    buttons[i].setAttribute('aria-selected', String(active));
    buttons[i].tabIndex = active ? 0 : -1;
    panels[i].hidden = !active;
   }
   cycle.dataset.activeStep = button.dataset.cycleStep;
   cycle.dataset.loopReturn = String(automatic && previousStage === stages.length - 1 && lastStage === 0);
  }
  function render(state) {
   if (animation) {animation.cancel(); animation = null;}
   cycle.dataset.cyclePlayback = state.running ? 'running' : state.waiting ? 'waiting' : 'paused';
   toggle.textContent = userPaused ? window.NintecI18n.t("Reprendre recorregut") : window.NintecI18n.t("Pausar recorregut");
   toggle.setAttribute('aria-pressed', String(userPaused));
   const activeIndex = stages.indexOf(selected);
   for (const path of paths) {
    const active = Number(path.dataset.cycleFlow) === activeIndex && !motion.matches;
    path.dataset.flowActive = String(active);
    if (!active) continue;
    const offset = 100 * state.remaining / state.duration;
    path.style.strokeDashoffset = String(offset);
    if (state.running && path.animate) {
     animation = path.animate([{strokeDashoffset: offset}, {strokeDashoffset: 0}],
      {duration: state.remaining, easing: 'linear', fill: 'forwards'});
    }
   }
  }
  const player = createPlayback({onAdvance: () => select(stages[(lastStage + 1) % stages.length], true), onState: render});
  select(selected);

  for (const button of buttons) {
   listen(button, 'click', () => {select(button); player.hold();});
   listen(button, 'keydown', event => {
    const current = buttons.indexOf(button); let next;
    if (['ArrowRight', 'ArrowDown'].includes(event.key)) next = (current + 1) % buttons.length;
    if (['ArrowLeft', 'ArrowUp'].includes(event.key)) next = (current + buttons.length - 1) % buttons.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = buttons.length - 1;
    if (next !== undefined) {
     event.preventDefault(); player.setPaused('keyboard', true);
     select(buttons[next]); player.hold(); buttons[next].focus({preventScroll: true});
    }
   });
  }
  zones.forEach((zone, i) => {
   if (matchMedia('(hover: hover)').matches && zone.matches(':hover')) player.setPaused('hover-' + i, true);
   listen(zone, 'pointerenter', event => {
    if (event.pointerType === 'mouse') player.setPaused('hover-' + i, true);
   });
   listen(zone, 'pointerleave', event => {
    if (event.pointerType === 'mouse') player.setPaused('hover-' + i, false, LEAVE_MS);
   });
   listen(zone, 'pointerdown', () => player.hold());
   listen(zone, 'focusin', event => {
    if (keyboard || event.target.matches(':focus-visible')) player.setPaused('keyboard', true);
   });
   listen(zone, 'focusout', event => {
    if (!inside(event.relatedTarget)) player.setPaused('keyboard', false, LEAVE_MS);
   });
  });
  listen(document, 'keydown', () => {
   keyboard = true;
   if (inside(document.activeElement)) player.setPaused('keyboard', true);
  });
  listen(document, 'pointerdown', () => {
   keyboard = false; player.setPaused('keyboard', false, LEAVE_MS);
  });
  listen(toggle, 'click', () => {
   userPaused = !userPaused; player.setPaused('user', userPaused);
  });

  // Observe the wheel and reading surface separately, including on narrow screens.
  const visible = new Set();
  const observer = new IntersectionObserver(entries => {
   for (const entry of entries) {
    if (entry.isIntersecting && entry.intersectionRatio >= .35) visible.add(entry.target);
    else visible.delete(entry.target);
   }
   player.setPaused('offscreen', !visible.size);
  }, {threshold: [0, .35]});
  observer.observe(wheel); observer.observe(details);
  function preference() {
   cycle.classList.toggle('cycle-reduced', motion.matches);
   toggle.hidden = motion.matches; hint.hidden = !motion.matches;
   player.setPaused('reduced-motion', motion.matches);
  }
  listen(motion, 'change', preference); preference();
  function visibility() {player.setPaused('hidden-tab', document.hidden);}
  listen(document, 'visibilitychange', visibility); visibility(); render(player.snapshot());

  // Reserve the tallest explanation at this width, so autoplay never moves the page.
  function measure() {
   if (disposed || !cycle.isConnected) return;
   measureFrame = null;
   let height = 0;
   const width = details.clientWidth;
   for (const panel of panels) {
    const copy = panel.cloneNode(true);
    copy.hidden = false; copy.removeAttribute('id'); copy.removeAttribute('role');
    copy.removeAttribute('aria-labelledby'); copy.removeAttribute('tabindex');
    copy.setAttribute('aria-hidden', 'true'); copy.inert = true;
    copy.classList.add('cycle-measure'); copy.style.width = width + 'px';
    copy.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
    details.append(copy); height = Math.max(height, copy.getBoundingClientRect().height); copy.remove();
   }
   details.style.setProperty('--cycle-panel-height', Math.ceil(height) + 'px');
  }
  const resize = new ResizeObserver(entries => {
   const width = entries[0].contentRect.width;
   if (Math.abs(width - lastWidth) < .5) return;
   lastWidth = width;
   if (measureFrame !== null) cancelAnimationFrame(measureFrame);
   measureFrame = requestAnimationFrame(measure);
  });
  resize.observe(details); measure();
  cycle.classList.add('cycle-ready');
  // No timers, observers, animations or listeners survive a removed component.
  const removal = new MutationObserver(() => {if (!cycle.isConnected) cleanup();});
  removal.observe(document.body, {childList: true, subtree: true});
  function cleanup() {
   if (disposed) return;
   disposed = true; player.destroy(); abort.abort(); observer.disconnect(); resize.disconnect(); removal.disconnect();
   if (animation) animation.cancel();
   if (measureFrame !== null) cancelAnimationFrame(measureFrame);
   cycle.classList.remove('cycle-ready'); toggle.hidden = true; hint.hidden = false;
   instances.delete(cycle);
  }
  listen(window, 'pagehide', cleanup);
  return cleanup;
 }
 const instances = new Map();
 if (typeof module !== 'undefined' && module.exports) module.exports = {createPlayback, AUTO_MS, READ_MS, LEAVE_MS};
 else {
  function init() {
   document.querySelectorAll('[data-cycle]').forEach(cycle => {
    if (!instances.has(cycle)) instances.set(cycle, mount(cycle));
   });
  }
  init(); window.addEventListener('pageshow', init);
 }
})(globalThis);
