# IFDSM question bank

1,502 single-best-answer practice questions covering all 78 learning outcomes of the ten IFDSM dental sleep medicine examination competencies. It runs entirely in the browser — no server, no account — and installs on iPhone and iPad as a home-screen app that works offline.

## What's in this folder

| Path | What it is |
|---|---|
| `index.html` | The app itself. Questions are built into this one file. |
| `manifest.webmanifest`, `sw.js`, `icons/` | Let the app install to the home screen and work offline. |
| `data/questions.json`, `data/questions.csv` | The full question bank as data (the CSV opens in Excel or Numbers). |
| `source/` | The editable question files and the script that rebuilds `index.html`. |
| `.nojekyll` | Tells GitHub Pages to serve the files exactly as they are. |

## Put it on GitHub Pages

1. Create a new repository on github.com (for example `ifdsm-question-bank`). Make it **public** if you're on a free GitHub plan — Pages needs that.
2. Upload everything in this folder to the repository root: on the repository page choose **Add file → Upload files**, drag in the *contents* of the unzipped folder (not the folder itself), and commit. Make sure `.nojekyll` comes along — on a Mac, press Cmd + Shift + . in Finder to show hidden files before dragging.
3. Go to **Settings → Pages**. Under *Build and deployment*, set Source to **Deploy from a branch**, Branch to **main** and folder to **/ (root)**, then save.
4. After a minute or two the address appears at the top of that page, in the form `https://your-username.github.io/ifdsm-question-bank/`.

## Install on iPhone or iPad

1. Open the GitHub Pages address in **Safari**.
2. Tap the **Share** button, then **Add to Home Screen**, then **Add**.
3. Open it from the home-screen icon. It runs full screen, and after the first visit it also works without an internet connection.

Progress (answered questions, accuracy by topic) is saved on each device separately. The home-screen app keeps its own progress, separate from the same page opened in Safari. Clearing Safari website data also clears it.

On iPad with a keyboard: A–D or 1–4 to answer, Enter or → for the next question, ← to go back.

## Editing or adding questions

Questions live in `source/t01a.txt` … `source/t10.txt` in this format:

```
@3.4
Q: CPAP titration typically starts at:
+ 4 cmH2O
- 1 cmH2O
- 10 cmH2O
- 15 cmH2O
E: Start at 4, titrate to lowest effective pressure, maximum ~20.
```

`@` is the learning outcome, `+` the correct answer, `-` the three distractors and `E:` the explanation. Leave a blank line between questions. Answer order is shuffled automatically (options that start with a number are sorted in ascending order instead).

To rebuild after editing, with Python 3 installed:

```
python3 source/build.py
```

This regenerates `index.html` and `data/questions.json`. Then, in `sw.js`, change `ifdsm-qb-v1` to `ifdsm-qb-v2` (and so on each time) so installed copies pick up the update, and upload the changed files to GitHub.

## A note on the content

The questions were written from the candidate's own syllabus notes and revision material, cross-checked against AASM, AADSM and ICSD-3-TR sources. They are practice material, not past IFDSM papers. Billing and referral rules are jurisdiction-specific — check local rules before relying on them clinically.
