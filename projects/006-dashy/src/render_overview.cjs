// Use a caller-specified sharp installation; keep project dependencies isolated.
const path = require('node:path');
const sharp = require(process.env.SHARP_MODULE || 'sharp');
const assets = path.resolve(__dirname, '../assets');
sharp(path.join(assets, 'dashy-capability-overview.svg'))
  .png()
  .toFile(path.join(assets, 'dashy-capability-overview.png'))
  .then(info => console.log(JSON.stringify(info)))
  .catch(error => { console.error(error); process.exitCode=1; });
