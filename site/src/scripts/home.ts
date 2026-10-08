import { initMotion } from './core/motion';
import { mountHero } from './hero/index';
import { mountTiles } from './sections/tiles';
import { mountLazyForms } from './form/lazy';
import { mountStory } from './story/index';

initMotion();
mountHero();
mountTiles();
mountLazyForms();
void mountStory();
