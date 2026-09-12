# Public site image sources

## `mbbn-figure-2.png`

- **Work:** Sangyoon Bae, Junbeom Kwon, Shinjae Yoo and Jiook Cha, “Learning brain dynamics across distinct scaling regimes reveals psychiatric signatures,” *Communications Biology* 9, 963 (2026), Figure 2.
- **DOI:** [10.1038/s42003-026-10011-7](https://doi.org/10.1038/s42003-026-10011-7).
- **Figure and caption:** [Publisher Figure 2 page](https://www.nature.com/articles/s42003-026-10011-7/figures/2).
- **Original image:** [Publisher full-resolution PNG](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs42003-026-10011-7/MediaObjects/42003_2026_10011_Fig2_HTML.png).
- **License:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). The publisher's [Rights and permissions](https://www.nature.com/articles/s42003-026-10011-7#rightslink) states that the article and its images are covered unless a separate credit line says otherwise. Figure 2 carries no separate third-party exception. Verified on 2026-09-12.
- **Original dimensions:** 1234 × 2495 pixels; 1,007,212 bytes. Reproduce dimensions with `python3 -c 'from PIL import Image; print(Image.open("public/assets/site/mbbn-figure-2.png").size)'`.
- **SHA-256:** `98583e0cf7d7dde33444c311c0472362f04ac3c4147f71f714e967725a4f691d`. Recheck with `sha256sum public/assets/site/mbbn-figure-2.png`.
- **Asset changes:** None. The saved PNG is the unmodified publisher image.

The figure depicts model-derived brain connectivity patterns associated with ADHD (panels A–C) and ASD (panels D–F). It is a published research figure, not a photograph or direct evidence of a causal mechanism. Figure context and statistical details remain available in the linked original paper.

The webpage or a screenshot of a code-authored OG composition may frame an excerpt with CSS. Such a presentation must identify the displayed panels and state “excerpt” (발췌), retain visible author/publication/license credit, and link to the complete figure or paper. CSS framing does not change this original asset. If only the top panels A–C are visible, identify the subject as ADHD-related patterns rather than all ADHD and ASD panels.

Suggested credit: **Bae et al., Communications Biology (2026), Fig. 2. CC BY 4.0.** For a framed top-half excerpt: **Fig. 2A–C, excerpt / 그림 2A–C, 발췌**.


## `og-homepage.png`

The 1200 × 630 social preview is a screenshot of a code-authored composition:
lab name and official domain on the left, Figure 2A–C excerpt on the right,
with visible author, publication and CC BY 4.0 credit. It is not an AI-generated
research figure. The original research PNG remains unchanged.

The layout source is `scripts/og-homepage.html`. Serve the repository root with
`python3 -m http.server 8765`, open `/scripts/og-homepage.html` at a 1200 × 630
viewport, wait for `document.fonts.ready`, and take a viewport screenshot to
`public/assets/site/og-homepage.png`. The source references repository-local
image and MaruBuri font assets; Hahmlet loads from Google Fonts.
