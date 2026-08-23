# Portable release-source build QA

Date: 2026-08-23  
Result: **PASS**

The public release staging tree was built using only its packaged 289-file LaTeX closure and its portable entry point:

```powershell
pwsh build/Build-PDF.ps1
```

The script copied `source/latex-id-ID/` into an isolated ignored work directory, set the pinned source epoch, invoked `latexmk`, completed the required bibliography and index passes, and converged with all targets current.

Output identity:

- path: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`;
- pages: 387;
- bytes: 8,202,487;
- SHA-256: `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d`.

This is byte-identical to the release artifact admitted by `build/manifests/id-ID-build.json` and `qa/WHOLE_CORPUS_RELEASE_QA_20260822.md`. The staged tree therefore proves that the distributed LaTeX closure can reproduce the released PDF without requiring LyX or any machine-local source path.

The build retained the inherited BibTeX metadata warning for `goldberg` (month without year) and the known layout diagnostics already admitted by the whole-corpus visual QA. It completed with no fatal error, and the final PDF identity proves that these diagnostics did not change the admitted bytes.
