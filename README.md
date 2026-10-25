# google-input-tools-api

Transliteration for 27 languages via the (undocumented) Google Input Tools endpoint
that [https://www.manglish.app/](https://www.manglish.app/) drives in the browser.

The site itself does not host a conversion model. Every keystroke is sent to:

```
GET https://inputtools.google.com/request
    ?text=<latin>&itc=<code>&num=5&cp=0&cs=1&ie=utf-8&oe=utf-8
```

- `itc` selects the language/script (e.g. `ml-t-i0-und` for Malayalam, `pinyin` for Chinese).
- `num` = how many candidates to return.
- `cp` = cursor position inside `text`.
- `cs` = commit-segment flag (0/1).
- `ie`/`oe` = input/output encoding (`utf-8`).

Response:

```json
["SUCCESS", [["namaskaram",
  ["നമസ്കാരം", "നമസ്‌കാരം", "നമസ്ക്കാരം", "..."],
  [], {"candidate_type": [0,0,0,0,0]}]]]
```

The first candidate is the best guess.

## Supported languages

amharic, arabic, assamese, bengali, belarusian, bulgarian, chinese, greek,
gujarati, hebrew, hindi, kannada, malayalam, marathi, nepali, odia, persian,
punjabi, russian, sanskrit, serbian, sinhala, tamil, telugu, tigrinya,
ukrainian, urdu.

## Install / use

No dependencies beyond Python 3.8+.

```sh
./inputtools "ente pere raman aanu"          # -> എന്റെ പേര് രാമൻ ആണ്
./inputtools --lang hindi "namaste"
./inputtools --lang tamil "vanakkam"
./inputtools -a "namaskaram"                 # all candidates
./inputtools --json "njan"                   # raw response
echo "sugham aano" | ./inputtools
./inputtools -i input.txt -o output.txt
```

Backward-compatible `manglish` wrapper is also provided.

As a library:

```python
from inputtools import convert
c = convert("ente pere raman aanu", itc="ml-t-i0-und")
print(c.top)          # എന്റെ പേര് രാമൻ ആണ്
print(c.candidates)   # all candidates
```

## HTTP API

```sh
./server.py            # listens on 0.0.0.0:8080
curl "http://localhost:8080/convert?text=ente%20pere%20raman%20aanu&lang=malayalam"
curl -X POST http://localhost:8080/convert -d '{"text":"namaste","lang":"hindi"}'
```

## Notes

- No API key, no account. It is someone else's free web tool being driven over
  an undocumented endpoint — expect it to break if Google changes it.
- Be a decent client: don't hammer it.
- Extracted via passive browser observation (Chrome DevTools) of
  manglish.app; no source of the site was modified.
