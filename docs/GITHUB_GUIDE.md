# GitHub upload guide (web interface)

This guide uses the GitHub website only. The repository should remain **Private** during review.

## 1. Create the repository

1. Sign in at https://github.com.
2. Open https://github.com/new.
3. Set the repository name to `cvd-stress-risk-chart`.
4. Add a short description, for example: `Research code for CVD modelling and stress-related risk-chart visualization`.
5. Select **Private**.
6. Leave “Add a README”, `.gitignore`, and license unchecked because these files are already included in this project.
7. Select **Create repository**.

## 2. Upload the project files

1. Extract the ZIP archive on your computer.
2. Open the newly created empty repository.
3. Select **Add file → Upload files**.
4. Open the extracted `cvd-stress-risk-chart` folder on your computer.
5. Select the contents of that folder (including hidden files such as `.gitignore`) and drag them into the GitHub upload area. Upload the contents, not an extra nested `cvd-stress-risk-chart` folder.
6. Check the file list before committing. Do not upload participant data, spreadsheets, raw exports, or any file containing personal or sensitive information.
7. Enter a commit message such as `Add initial research code and documentation`.
8. Select **Commit changes**.

The web uploader may not show hidden files in every file picker. Confirm that `.gitignore` is present in the repository after upload. If it is missing, use **Add file → Create new file**, name it `.gitignore`, and copy the project's `.gitignore` contents into it.

## 3. Verify the private repository

- Confirm the repository visibility says **Private**.
- Confirm the root contains `README.md`, `LICENSE`, `requirements.txt`, `.gitignore`, `data/`, `src/`, `results/`, and `docs/`.
- Confirm `data/` contains only `README.md` and `.gitkeep`.
- Confirm no `.csv`, `.xlsx`, `.xls`, `.sav`, `.rds`, `.RData`, or participant-level files were uploaded.
- Confirm `src/07_risk_chart.py` and `src/06_model_evaluation.py` are the revised versions in this archive.

## 4. Review before sharing with a supervisor

Before granting access or changing visibility:
- Replace the citation placeholder in `README.md` with the approved thesis citation.
- Replace `<YOUR NAME>` in `LICENSE` only after confirming the correct copyright holder and licensing rights.
- Verify the SPSS Constant before using `CVD_INTERCEPT` to produce absolute-risk interpretations.
- Confirm the logic behind the 640 chart combinations against the original Appendix 7.
- Confirm that the institution/data-use agreement permits sharing any aggregate result figures.

## 5. Keep the repository private

Do not change visibility to Public until the code, citation, license, data permissions, and figures have been reviewed. To invite a supervisor to a private repository, use **Settings → Collaborators** (GitHub may label this section differently) and grant access only to the intended account.
