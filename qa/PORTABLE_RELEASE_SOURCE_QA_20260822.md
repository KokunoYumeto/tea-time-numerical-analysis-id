# Portable release-source build QA

Date: 2026-08-22  
Result: **PASS**

The public release staging tree was built using only its packaged 289-file LaTeX closure and its portable entry point:

```powershell
pwsh build/Build-PDF.ps1
```

The script copied `source/latex-id-ID/` into an isolated ignored work directory, set the pinned source epoch, invoked `latexmk`, completed the required bibliography and index passes, and converged with all targets current.

Output identity:

- path: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`;
- pages: 387;
- bytes: 8,202,476;
- SHA-256: `cbc31e9e27fdee96845d78fa6a625bf956196001b7941ddf0f1232f5def46b45`.

This is byte-identical to the release artifact admitted by `build/manifests/id-ID-build.json` and `qa/WHOLE_CORPUS_RELEASE_QA_20260822.md`. The staged tree therefore proves that the distributed LaTeX closure can reproduce the released PDF without requiring LyX or any machine-local source path.

The build retained the inherited BibTeX metadata warning for `goldberg` (month without year) and the known layout diagnostics already admitted by the whole-corpus visual QA. It completed with no fatal error, and the final PDF identity proves that these diagnostics did not change the admitted bytes.
