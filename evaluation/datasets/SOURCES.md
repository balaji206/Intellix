# Evaluation corpus sources

The corpus files are not committed to Git. Rebuild them with:

```powershell
cd services\rag-service
python -m scripts.download_corpus
```

| File | Source | Format in corpus | Notes |
|---|---|---|---|
| NIST.AI.100-1.pdf | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf | PDF | NIST AI Risk Management Framework 1.0. US government publication, available free of charge from NIST |
| DPDP-Act-2023.pdf | https://www.indiacode.nic.in/bitstream/123456789/22037/2/a2023-22.pdf | PDF | Digital Personal Data Protection Act, 2023 (Government of India). Fallback: MeitY copy |
| rfc7519-jwt.txt | https://www.ietf.org/rfc/rfc7519.txt | TXT | RFC 7519, JSON Web Token (JWT) |
| rfc8725-jwt-bcp.txt | https://www.rfc-editor.org/rfc/rfc8725.txt | TXT | RFC 8725, JWT Best Current Practices. Updates RFC 7519 |
| gitlab-time-off-types.md | https://handbook.gitlab.com/handbook/people-group/time-off-and-absence/time-off-types/ | Markdown (converted from HTML) | GitLab Handbook |
| gitlab-leave-types.docx | https://handbook.gitlab.com/handbook/people-group/time-off-and-absence/leave-types/ | DOCX (converted from HTML) | GitLab Handbook |
| gitlab-time-away-philosophy.md | https://handbook.gitlab.com/handbook/people-group/time-off-and-absence/time-away-philosophy/ | Markdown (converted from HTML) | GitLab Handbook |
| Intellix_Full_Project_Report.docx | Own document | DOCX | Added manually |

## Licence notes

- Check each source's own terms before redistributing any copy. This repository stores only the URLs and the questions, not the documents.
- The GitLab Handbook is published as open content. Verify the licence and attribution requirements on the site before reusing it outside local evaluation.
- Handbook pages change over time. Record the date you downloaded them, because gold phrases in `questions.json` must match the text you actually evaluated against.

Downloaded on: ____-__-__
