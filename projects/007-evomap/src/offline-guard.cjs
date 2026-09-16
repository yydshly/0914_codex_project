'use strict';
// Experiment guard, not a general security sandbox. No CLI or daemon is loaded.
const deny = () => { throw new Error('OFFLINE_RESEARCH_NETWORK_BLOCKED'); };
for (const name of ['http', 'https']) {
  const mod = require(name);
  mod.request = deny;
  mod.get = deny;
}
const net = require('net');
net.connect = deny;
net.createConnection = deny;
net.Socket.prototype.connect = deny;
require('tls').connect = deny;
require('dgram').createSocket = deny;
globalThis.fetch = deny;
globalThis.WebSocket = deny;
