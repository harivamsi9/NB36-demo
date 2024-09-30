# NB36-demo

## Customer Communication Docs
https://docs.google.com/document/d/1FhXzqi17IqoIgh82L0lT6bo2ZL6_vUboJXRTWqpY33U/edit?usp=sharing

## High Level Design
Link: https://app.eraser.io/workspace/vlsKlvMxvDpaa5rEbeee?origin=share
<img width="1152" alt="image" src="https://github.com/user-attachments/assets/986dcdd1-c569-40c8-8b29-a61c289df5b8">

## Technological Details

### Existing

### Modification
- Added `.github/workflows/update_taktile.yml` workflow file
-- -> Responsible for automating the process of updating Taktile Code Nodes upon each merge to the main branch by triggering the relevant Taktile API calls file i.e. taktile_update_handler.py
- Added `.github/workflows/taktile_github_integration/taktile_update_handler.py` file  -> Responsible for Handling backend Taktile API calls for updating Taktile Code Nodes
- `Taktile_API_KEY` is a unique private key, and must be protected and not revealed to public -> Used Github Actions Secrets to securely use this. [Github Actions Secrets Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
- 

 


## Sanity Testing
testing update 1: updating directing the main branch ✅ \
testing update 2: creating new feature branch (from local) and trying to merge to main later ✅ \
testing update 3: created taktile_github integration 


