import { mountCharacters } from './home/characters';
import { mountPlayer } from './home/player';
import { mountHero } from './hero/index';
import { mountSteps } from './home/steps';
import { mountSticky } from './home/sticky';
import { mountTiles } from './sections/tiles';
import { mountLazyForms } from './form/lazy';
import { track } from './core/analytics';

const open = mountPlayer();
mountHero(open);
mountSteps();
mountSticky();
mountTiles();
mountLazyForms();
void mountCharacters();

const h1 = document.getElementById('hero-h1');
if (h1?.dataset['variant']) track('utm_headline_variant', { v: h1.dataset['variant'] });
