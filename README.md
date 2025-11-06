# INFO 511 • Final Project (FA 25)

A concise, well-structured README to orient readers to the repository layout and key assets.

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

## 🖼️ Key Images

### Option A — Side-by-side (HTML; works on GitHub)
<div style="display:flex; gap:16px; align-items:flex-start; flex-wrap:wrap;">
  <figure style="margin:0;">
    <img src="Images_/0_class_image_2.png" alt="Class image example" style="max-width:480px; width:100%; height:auto; border:1px solid #e5e7eb; border-radius:8px;" />
    <figcaption style="font-size:0.9rem; color:#4b5563; margin-top:6px;">Figure 1. Class image example</figcaption>
  </figure>
  <figure style="margin:0;">
    <img src="Images_/Make the Arizona “A”.png" alt="Make the Arizona A" style="max-width:480px; width:100%; height:auto; border:1px solid #e5e7eb; border-radius:8px;" />
    <figcaption style="font-size:0.9rem; color:#4b5563; margin-top:6px;">Figure 2. “Make the Arizona A”</figcaption>
  </figure>
</div>

### Option B — Plain Markdown (one per line)
![Class image example](Images_/0_class_image_2.png)

![“Make the Arizona A”](Images_/Make%20the%20Arizona%20%E2%80%9CA%E2%80%9D.png)

> If the filename with smart quotes gives trouble on your platform, consider renaming it to `Make_the_Arizona_A.png` and updating the path accordingly.

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
