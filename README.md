## Status
![Status](https://img.shields.io/badge/status-work%20in%20progress-orange)

🚧 **StarMoji is in active early development.** Glyph coverage is currently partial, 
the visual style is still being refined, and both the source file structure and 
the build pipeline may change without notice. It's not yet ready for production use.

Watch or star the repo to follow progress — feel free to open an issue if you'd 
like to contribute or suggest which emoji to prioritize next.

# StarMoji
StarMoji is an original, from-scratch emoji font in a glossy, 
three-dimensional style. It's built for people who like that polished, 
rounded look but want it outside of a single vendor's walled garden — 
on Android, Linux, or the web — without relying on unofficial, 
copyright-infringing font swaps.

Every glyph is drawn independently, not traced or derived from any 
existing commercial set, and released under the SIL Open Font License. 
The goal is full Unicode 17 emoji coverage, including skin tone and 
gender variant sequences.


## Design & Source Files

All artwork for StarMoji is created in [Affinity Designer](https://affinity.serif.com/), 
a free, vector-first design tool. Beyond the final exported font files, this repository 
also publishes the underlying **source assets** — base face shapes, shadow and highlight 
layers, and other reusable building blocks — as native Affinity (`.afdesign`) and SVG files.

Sharing these base components, not just the finished glyphs, means anyone can build new 
emoji on a consistent visual foundation, fork the style, or contribute variants without 
having to reverse-engineer the shading, gradients, and proportions from scratch.
