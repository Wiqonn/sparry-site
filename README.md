# Sparry deployment

Target: **https://sparry.wiqonn.com**. Repository: **[Wiqonn/sparry-site](https://github.com/Wiqonn/sparry-site)**, branch **main**. The initial landing was committed and pushed with the owner's approval as `08c9e43`. GitHub Actions deployed it successfully, and Pages is configured for the Sparry subdomain. DNS and HTTPS verification are still pending.

## Existing site

Inspected on 15 October 2026:

- `/code/wiqonn.github.io` is the separate Next.js website, exported to static files and deployed by GitHub Actions to GitHub Pages.
- Its Pages custom domain is `www.wiqonn.com`; its source branch is `master`.
- The domain's authoritative nameservers are Cloudflare's `cloe.ns.cloudflare.com` and `elliot.ns.cloudflare.com`.
- `sparry.wiqonn.com` currently has no A or CNAME answer. The separate landing repository was created after inspecting the existing deployment.

Use an independent Pages repository for Sparry. Keep the existing website's CNAME, workflows and DNS records intact. A subfolder of the current Next.js export would be a path on the existing website rather than an independently configured Pages custom domain.

## Prepared package

The source lives in `audit-studio/landing`. From that repository, run:

```sh
node landing/scripts/build-spanish.mjs
node landing/scripts/build-pages.mjs
```

The generated `landing/.pages/` directory is ready to become the independent repository:

```text
.github/workflows/pages.yml
site/
  index.html
  index-es.html
  styles.css
  experience.css
  app.js
  motion.js
  assets/
  CNAME
  .nojekyll
  robots.txt
  sitemap.xml
site-manifest.json
README.md
```

The workflow publishes only `site/`. It does not install Next.js or upload application source, development scripts, review notes, browser receipts or credentials. Only referenced media, public demo downloads and their licenses are copied; old unused screenshots and chart revisions stay in the private source workspace. CSS and JavaScript URLs contain content hashes, so updated builds request fresh styles and scripts. Canonical URLs and English/Spanish alternatives use the Sparry subdomain.

## Publication and domain setup

1. Commit and push the prepared files to `Wiqonn/sparry-site` on `main` only after the owner's explicit git approval. Proposed initial message: `feat: launch Sparry landing page`.
2. In that repository's **Settings → Pages**, select **GitHub Actions** as the publishing source. Set **Custom domain** to `sparry.wiqonn.com`. If the initial workflow ran before Pages was enabled, rerun **Deploy Sparry landing** from Actions.
3. In Cloudflare's DNS records for `wiqonn.com`, add this record:

   | Field        | Value                                                |
   | ------------ | ---------------------------------------------------- |
   | Type         | CNAME                                                |
   | Name         | sparry                                               |
   | Target       | wiqonn.github.io                                     |
   | Proxy status | DNS only for initial domain/certificate verification |
   | TTL          | Auto                                                 |

4. Wait for GitHub's DNS check and certificate provisioning, then enable **Enforce HTTPS** for the Sparry repository.
5. Verify the English page, Spanish switch, images, SQL/PDF downloads, contact links, animations and narrow layouts on the live hostname.

With a custom Actions publishing source, the `CNAME` file does not configure the repository's Pages settings. Set the custom domain in Settings explicitly, before creating its DNS record. The DNS target is the organization hostname, not a repository path or the main website's custom domain.

No existing `wiqonn.com` or `www.wiqonn.com` configuration needs changing. Sparry Cloud remains a planned product feature, separate from hosting this marketing website.

References: [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [official static Pages workflow](https://github.com/actions/starter-workflows/blob/main/pages/static.yml), [Cloudflare DNS records](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/).
