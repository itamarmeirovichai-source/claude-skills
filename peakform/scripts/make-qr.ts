// QR code for the install address. The address contains no personal data.
import QRCode from 'qrcode';
import { writeFileSync } from 'node:fs';
const url = process.argv[2] ?? 'https://itamarmeirovichai-source.github.io/claude-skills/peakform/';
writeFileSync('docs/install-qr.svg', await QRCode.toString(url, { type: 'svg', margin: 2, errorCorrectionLevel: 'M' }));
await QRCode.toFile('docs/install-qr.png', url, { margin: 2, width: 512, errorCorrectionLevel: 'M' });
console.log(`QR code for ${url} written to docs/install-qr.svg and docs/install-qr.png`);
