'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {createPlayback, AUTO_MS, READ_MS, LEAVE_MS} = require('../src/cycle-player.js');
function setup() {
 let time = 0, id = 0, advances = 0, state;
 const timers = new Map();
 const player = createPlayback({now: () => time,
  setTimer: (fn, delay) => {timers.set(++id, {fn, at: time + delay}); return id;},
  clearTimer: id => timers.delete(id),
  onAdvance: () => advances++, onState: s => state = s});
 function tick(ms) {
  const end = time + ms;
  while (true) {
   const next = [...timers].sort((a,b) => a[1].at-b[1].at)[0];
   if (!next || next[1].at > end) break;
   time = next[1].at; timers.delete(next[0]); next[1].fn();
  }
  time = end;
 }
 return {player, tick, timers, get advances(){return advances}, get state(){return state}};
}
test('starts only when visible, advances at four seconds, and uses one timer', () => {
 const s=setup(); s.tick(100000); assert.equal(s.advances,0); assert.equal(s.timers.size,0);
 s.player.setPaused('offscreen',false); s.tick(AUTO_MS-1); assert.equal(s.advances,0);
 s.tick(1); assert.equal(s.advances,1); assert.equal(s.timers.size,1);
 s.tick(AUTO_MS*5); assert.equal(s.advances,6);
});
test('hover freezes the remaining dwell; leaving adds 1.5 seconds without restarting', () => {
 const s=setup(); s.player.setPaused('offscreen',false); s.tick(2000);
 s.player.setPaused('hover',true); assert.equal(s.player.snapshot().remaining,2000);
 s.tick(60000); assert.equal(s.advances,0); assert.equal(s.timers.size,0);
 s.player.setPaused('hover',false,LEAVE_MS); s.tick(LEAVE_MS); assert.equal(s.advances,0);
 s.tick(1999); assert.equal(s.advances,0); s.tick(1); assert.equal(s.advances,1);
});
test('a tap holds the selected content for 18 seconds and the next stage gets four', () => {
 const s=setup(); s.player.setPaused('offscreen',false); s.tick(3000); s.player.hold();
 s.tick(READ_MS-1); assert.equal(s.advances,0); s.tick(1); assert.equal(s.advances,1);
 s.tick(AUTO_MS); assert.equal(s.advances,2);
});
test('keyboard focus and hover can overlap without prematurely resuming', () => {
 const s=setup(); s.player.setPaused('offscreen',false);
 s.player.setPaused('keyboard',true); s.player.hold(); s.player.setPaused('hover',true);
 s.player.setPaused('hover',false,LEAVE_MS); s.tick(60000);
 assert.equal(s.advances,0); assert.equal(s.timers.size,0);
 s.player.setPaused('keyboard',false,LEAVE_MS); s.tick(LEAVE_MS+READ_MS);
 assert.equal(s.advances,1);
});
test('hidden tabs and offscreen sections have no timers and preserve progress', () => {
 const s=setup(); s.player.setPaused('offscreen',false); s.tick(2500);
 s.player.setPaused('hidden-tab',true); s.player.setPaused('offscreen',true);
 s.player.setPaused('hidden-tab',false); s.tick(60000); assert.equal(s.timers.size,0);
 s.player.setPaused('offscreen',false); s.tick(1499); assert.equal(s.advances,0);
 s.tick(1); assert.equal(s.advances,1);
});
test('reduced motion blocks autoplay even after manual interaction and visibility changes', () => {
 const s=setup(); s.player.setPaused('reduced-motion',true); s.player.setPaused('offscreen',false);
 s.player.hold(); s.tick(60000); assert.equal(s.advances,0); assert.equal(s.timers.size,0);
 s.player.setPaused('reduced-motion',false); s.tick(READ_MS); assert.equal(s.advances,1);
});
test('explicit pause persists until resumed, independently of hover', () => {
 const s=setup(); s.player.setPaused('offscreen',false); s.tick(1000);
 s.player.setPaused('user',true); s.player.setPaused('hover',true);
 s.player.setPaused('hover',false,LEAVE_MS); s.tick(60000); assert.equal(s.timers.size,0);
 s.player.setPaused('user',false); s.tick(LEAVE_MS+3000); assert.equal(s.advances,1);
});
test('reentering during the resume delay freezes it; disposal cancels pending work', () => {
 const s=setup(); s.player.setPaused('offscreen',false); s.tick(2000);
 s.player.setPaused('hover',true); s.player.setPaused('hover',false,LEAVE_MS); s.tick(500);
 s.player.setPaused('hover',true); s.tick(30000); assert.equal(s.advances,0);
 s.player.setPaused('hover',false,LEAVE_MS); s.tick(LEAVE_MS+1999); assert.equal(s.advances,0);
 s.player.destroy(); s.tick(60000); assert.equal(s.advances,0); assert.equal(s.timers.size,0);
 s.player.setPaused('offscreen',false); s.player.hold(); assert.equal(s.timers.size,0);
});
