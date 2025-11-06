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
       alt="Class image example"
       width="120"
       style="margin-right: 1rem; border-radius: 8px; border: 1px solid #c5f7c5;" />

  <div>
    <h1 style="margin: 0; color: #065f46;">INFO 511 • Final Project (FA 25)</h1>
    <p style="margin: 0.3rem 0 0 0;"><strong>Nathan Herling</strong></p>
    <p style="margin: 0;">Project:<br><em>A temporal analysis of Meteorite findings.</em></p>
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
