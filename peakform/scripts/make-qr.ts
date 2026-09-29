// QR code for your private install address. The address is kept out of the repository, so
// the code is written to private/, which is gitignored. The app's About screen also shows it.
// Usage: npx tsx scripts/make-qr.ts https://<your-project>.pages.dev/
import QRCode from 'qrcode';
import { mkdirSync, writeFileSync } from 'node:fs';
const url = process.argv[2];
if (!url || !/^https:\/\//.test(url)) {
  console.error('Give your private https address, for example https://peakform-abcd.pages.dev/');
  process.exit(1);
}
mkdirSync('private', { recursive: true });
writeFileSync('private/install-qr.svg', await QRCode.toString(url, { type: 'svg', margin: 2, errorCorrectionLevel: 'M' }));
await QRCode.toFile('private/install-qr.png', url, { margin: 2, width: 512, errorCorrectionLevel: 'M' });
console.log('QR code written to private/install-qr.svg and private/install-qr.png');
