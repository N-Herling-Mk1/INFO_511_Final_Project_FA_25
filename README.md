<table width="100%">
  <tr>
    <!-- Left: Class Logo -->
    <td style="vertical-align: top; padding-right: 12px; width: 140px;">
      <img src="Images_/0_class_image_2.png" alt="INFO 511 logo" width="120">
    </td>
    <td style="vertical-align: top;">
      <h1>INFO 511 • Final Project (FA 25)</h1>
      <b>Nathan Herling</b><br>
      <i>Project: A Temporal Analysis of Meteorite Findings</i>
    </td>
    <!-- Right: The GIF -->
    <td style="vertical-align: top; text-align: right; width: 220px;">
      <img src="Images_/mk_4d_no_legend__.gif" alt="Meteorite Animation" width="200">
    </td>
  </tr>
</table>

---
<!-- ====================================================== -->
<!--  Provenance Button (opens provenance.html in new tab) -->
<!-- ====================================================== -->
<p style="margin-top: 16px;">
  <a href="Data_/provenance.html" target="_blank" style="
     display:inline-block;
     padding:8px 14px;
     background:#1d4ed8;
     color:white !important;
     text-decoration:none;
     border-radius:6px;
     font-weight:600;
     border:1px solid #0f2a6d;">
    More Provenance Info
  </a>
</p>

---

## 📁 Directory Structure
> Tip: Use **forward slashes** in Markdown paths (GitHub-style), even on Windows.

```
INFO_511_Final_Project_FA_25/
├─ .git/
├─ Data_/                  # raw/processed data, ignore large binaries in git
├─ Docs_/                  # notes, writeups, reports
├─ Images_/                # figures and assets for the README & report
│  ├─ 0_class_image_2.png
│  └─ Make the Arizona “A”.png
├─ Scripts_/               # notebooks, analysis scripts, utilities
└─ README.md
```

---

## 🚀 Quick Start
1. **Clone** the repo and enter the project folder:
   ```bash
   git clone https://github.com/N-Herling-Mk1/INFO_511_Final_Project_FA_25.git
   cd INFO_511_Final_Project_FA_25
   ```
2. (Optional) Create a fresh environment and install deps:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -r requirements.txt
   ```
3. Run analysis scripts/notebooks in `Scripts_/` and save outputs to `Docs_/` or `Images_/`.

---

## 📝 Notes
- Keep large raw data out of git (use `Data_/` with `.gitignore` rules, DVC, or a cloud bucket).
- Use descriptive alt text for images to help screen readers and improve search.
- Prefer **relative paths** for portability (they work on GitHub and locally).

---

## 🔧 Dev Hints
- Regenerate the directory tree for this README (macOS/Linux):
  ```bash
  tree -L 2 -a
  ```
  Windows (PowerShell, minimal pretty-print):
  ```powershell
  gci -Recurse -Depth 2 | % { $_.FullName.Replace("$([Environment]::GetFolderPath('Desktop'))\","") }
  ```

---

© sandbox — INFO 511 Foundation of Data Science
