import { initMotion } from './core/motion';
import { mountHero } from './hero/index';
import { mountPopups } from './sections/popups';
import { mountTiles } from './sections/tiles';
import { mountBeforeAfter } from './sections/beforeafter';
import { mountLazyForms } from './form/lazy';

initMotion();
mountHero();
mountPopups();
mountTiles();
mountBeforeAfter();
mountLazyForms();
