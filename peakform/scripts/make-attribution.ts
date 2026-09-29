// Writes MEDIA_ATTRIBUTION.md from the media records so the two never disagree.
import { writeFileSync } from 'node:fs';
import { MEDIA } from '../src/content/media';
import { LIBRARY } from '../src/content/library';
import { RECIPES } from '../src/content/recipes';

const name = (id: string) => LIBRARY.find((e) => e.id === id)?.name ?? RECIPES.find((r) => r.id === id)?.name ?? id;
const rows = MEDIA.map((m) => `| ${name(m.targetId)} | [${m.title.replace(/\|/g, '/')}](${m.url}) | ${m.channel} | ${m.verifiedOn} | ${m.reviewStatus} |`);
const withVideo = new Set(MEDIA.filter((m) => m.targetType === 'exercise').map((m) => m.targetId));
const without = LIBRARY.filter((e) => !withVideo.has(e.id)).map((e) => e.name);
const md = `# Media attribution

## Original artwork

All visual assets in PeakForm were drawn for this project as original SVG code:

- Front and back body map with separately addressable muscle regions: \`src/svg/BodyMap.tsx\`
- Exercise keyframe figures and the pose renderer: \`src/svg/pose.ts\`, \`src/svg/Figures.tsx\`, with pose data in \`src/content/exercises/*.ts\`
- Volleyball, sprint, and pool drill diagrams: \`src/svg/pose.ts\`
- Estimate by Eye portion icons: \`src/svg/PortionIcons.tsx\`
- Interface icons: \`src/ui/icons.tsx\`
- App icon: \`public/icons/icon.svg\` and \`public/icons/icon-maskable.svg\`

They are not traced from or based on third party images, and they are released with the app.

## Linked videos

PeakForm links to these videos and can embed them with YouTube's official player from youtube-nocookie.com, only after a tap. Nothing is downloaded or rehosted. If a video disappears, the written steps and original keyframes remain.

Every video was matched by title and channel from search results, because YouTube could not be opened from the build environment. None was watched frame by frame. In the app, the user can mark each one as matching or not matching the exercise.

| For | Video | Channel | Checked | Status |
| --- | --- | --- | --- | --- |
${rows.join('\n')}

Exercises without a vetted video use the written steps and original keyframes only: ${without.join(', ')}.

## Food data

Built in food values are rounded approximations of common reference data. Optional barcode lookups use Open Food Facts, a community database under the Open Database License (ODbL).

## Social media

The two TikTok links supplied by the user could not be opened from the build environment. Nothing from them is used. See \`RESEARCH.md\`.
`;
writeFileSync('MEDIA_ATTRIBUTION.md', md);
console.log(`MEDIA_ATTRIBUTION.md written with ${MEDIA.length} videos; ${without.length} exercises without video.`);
