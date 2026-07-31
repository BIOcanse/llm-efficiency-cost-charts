# Repository entry and locale contract

## Boundary

- `README.md` is a small repository entry page, not a second copy of the
  analysis.
- GitHub Pages is the only maintained reading surface for charts,
  explanations, rankings, recommendations, sources, and snapshot switching.
- GitHub Releases are the download surface for complete dated chart sets.
- The README must not embed the chart gallery, duplicate methodology, or keep
  separate Chinese and English document bodies.

## Language behavior

GitHub Markdown does not run repository JavaScript. Common multilingual
repositories therefore link to separate Markdown files, while GitHub's native
interactive option is limited to collapsible `<details>` sections. Neither is
a true in-place locale switch.

Reference implementations and platform behavior:

- GitHub documents README rendering, relative links, and section anchors:
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- GitHub documents `<details>` as the native collapsed-section interaction:
  https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections
- PaddleOCR and Fish Speech use the common separate-file language-link pattern:
  https://github.com/PaddlePaddle/PaddleOCR
  https://github.com/fishaudio/fish-speech

This repository instead uses one Pages document:

- `?lang=zh-CN` opens the Chinese interface.
- `?lang=en` opens the English interface.
- The visible language buttons update the same document without a reload.
- The selected locale is reflected in the URL and saved locally.
- An explicit URL locale takes priority over the saved preference and browser
  language so README links are deterministic.

Snapshot selection follows the same rule through `?snapshot=YYYY-MM-DD`.
Language and snapshot parameters remain shareable and update without adding
fake document pages.

## README layout

1. One neutral bilingual title.
2. One short bilingual purpose line.
3. Plain text links for Chinese site, English site, and latest Release.
4. Current snapshot and benchmark identifier only.

No oversized image button, badges, chart images, ranking tables, duplicated
limitations, or language-specific README files.

## Recommendation section

The Pages recommendation section remains visibly marked as personal opinion,
but it uses the same white page background and text hierarchy as the rest of
the analysis. It must not resemble a promotional hero or separate campaign
landing page.
