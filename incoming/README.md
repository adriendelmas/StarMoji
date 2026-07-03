# Incoming — SVG drop box

Drop new emoji SVG files here, named with the **official Unicode emoji name**
(as listed in [emoji-test.txt](https://unicode.org/Public/17.0.0/emoji/emoji-test.txt)
or on [Emojipedia](https://emojipedia.org)), e.g.:

```
flushed face.svg
grinning face.svg
red heart.svg
```

A GitHub Action automatically renames each file to its Unicode codepoint(s)
and moves it to `sources/svg/<group>/<subgroup>/`, then updates the progress
table in the main README.

If a file stays here after a few minutes, its name wasn't recognized — check
the Action logs (Actions tab) for close-match suggestions.

*This file stays here on purpose so the folder always exists.*
