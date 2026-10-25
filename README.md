# manglish-typing-api

Manglish (Latin-script Malayalam) → Malayalam conversion, extracted from the
network traffic of [https://www.manglish.app/](https://www.manglish.app/).

The site itself does not host a conversion model. Every keystroke is sent to
Google's (undocumented) Input Tools endpoint:

```
GET https://inputtools.google.com/request
    ?text=<manglish>&itc=ml-t-i0-und&num=5&cp=0&cs=1&ie=utf-8&oe=utf-8
```

- `itc=ml-t-i0-und` selects Malayalam transliteration.
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

The first candidate is the best guess. Other Indic languages use their own
`itc` codes: `hi-t-i0-und` (Hindi), `ta-t-i0-und` (Tamil), `kn-t-i0-und`
(Kannada), etc.

## Install / use

No dependencies beyond Python 3.8+.

```sh
./manglish "ente pere raman aanu"          # -> എന്റെ പേര് രാമൻ ആണ്
./manglish -a "namaskaram"                 # all 5 candidates
./manglish --json "njan"                   # raw response
echo "sugham aano" | ./manglish
./manglish -i input.txt -o output.txt
```

As a library:

```python
from manglish import convert
c = convert("ente pere raman aanu")
print(c.top)          # എന്റെ പേര് രാമൻ ആണ്
print(c.candidates)   # all candidates
```

## HTTP API

```sh
./server.py            # listens on 0.0.0.0:8080
curl "http://localhost:8080/convert?text=ente%20pere%20raman%20aanu"
curl -X POST http://localhost:8080/convert -d '{"text":"namaskaram","num":3}'
```

## Notes

- No API key, no account. It is someone else's free web tool being driven over
  an undocumented endpoint — expect it to break if Google changes it.
- Be a decent client: don't hammer it.
- Extracted via passive browser observation (Chrome DevTools) of
  manglish.app; no source of the site was modified.
