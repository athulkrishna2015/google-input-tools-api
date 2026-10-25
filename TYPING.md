# Typing Malayalam with Fcitx5 + m17n (ITRANS)

This guide covers the `m17n_ml_itrans` input method configured by this project.
It works fully offline once Fcitx5 + m17n are installed (see README).

## Switching
- Toggle input methods: `Ctrl+Space` (or `Super+Space`).
- Available: `keyboard-us` (English), `m17n_ml_itrans` (ITRANS), `m17n_ml_mozhi` (Mozhi).

## ITRANS key map (Malayalam)

### Vowels
| Type | Result |
|------|--------|
| a    | അ     |
| aa / A | ആ   |
| i    | ഇ     |
| ii / I | ഈ   |
| u    | ഉ     |
| uu / U | ഊ   |
| e    | എ     |
| ee / E | ഏ   |
| ai   | ഐ     |
| o    | ഒ     |
| oo / O | ഓ   |
| au   | ഔ     |
| R    | ഋ     |

### Consonants
| Type | Result | Type | Result |
|------|--------|------|--------|
| k    | ക     | K / kh | ഖ    |
| g    | ഗ     | G / gh | ഘ    |
| N    | ങ     | ch     | ച    |
| C / chh | ഛ  | j      | ജ    |
| J / jh | ഝ   | ~N     | ഞ    |
| T    | ട     | Th / Th | ഠ  |
| D    | ഡ     | Dh     | ഢ    |
| N    | ണ     | t      | ത    |
| th   | ഥ     | d      | ദ    |
| dh   | ധ     | n      | ന    |
| p    | പ     | ph / f | ഫ    |
| b    | ബ     | bh     | ഭ    |
| m    | മ     | y      | യ    |
| r    | ര     | l      | ല    |
| L    | ള     | v / w  | വ    |
| sh / S | ശ   | Sh / Sh | ഷ  |
| s    | സ     | h      | ഹ    |
| R    | റ     | z      | ഴ    |

### Specials
| Type | Result |
|------|--------|
| M    | ം (anusvara) |
| H    | ഃ (visarga) |
| ~    | ് (virama / chillu trigger) |
| OM   | ഓം    |

### Examples
| Type this          | Get this       |
|--------------------|----------------|
| malayaaLaM         | മലയാളം        |
| namaskaram         | നമസ്കാരം      |
| ente pere raman    | എന്റെ പേര് രാമൻ |
| sugham aano        | സുഖം ആണോ     |
| kerala             | കേരള          |
| indiayaa           | ഇന്ത്യ         |

### Tips
- Capitalization matters: `L` = ള, `M` = ം, `N` = ണ/ങ/ഞ.
- Double a vowel for the long form: `aa`, `ee`, `oo`, `ii`, `uu`.
- Press `Space` to commit a trailing consonant (virama).
- For chillu letters, type the consonant followed by `~` (e.g. `n~` → ൻ).

## Mozhi scheme
`m17n_ml_mozhi` is an alternative popular in Kerala. Switch with `Ctrl+Space`.
It uses a more phonetic, less strict mapping (e.g. `malayalam` may need `malayaLam`).
ITRANS is generally more predictable for exact spelling.
