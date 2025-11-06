<div style="
  border: 2px solid limegreen;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  background: #f8fff8;
">

  <img src="Images_/0_class_image_2.png"
       alt="INFO 511 logo"
       width="120"
       style="margin-right: 1.5rem; border-radius: 10px; border: 1px solid #baf7ba;" />

  <div>
    <h1 style="margin: 0; font-size: 1.8rem; color: #064e3b;">
      INFO 511 • Final Project (FA 25)
    </h1>
    <p style="margin: 0.4rem 0 0 0; font-weight: 700; font-size: 1.2rem;">Nathan Herling</p>
    <p style="margin: 0.2rem 0 0 0; font-size: 1.05rem;">
      <strong>Project:</strong><br>
      <em>A Temporal Analysis of Meteorite Findings</em>
    </p>
  </div>

</div>
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
   git clone <YOUR-REPO-URL>
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
