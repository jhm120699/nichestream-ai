# DNS Records for NicheStream AI

To complete the custom domain setup and bulletproof the Google Search Console verification, please add the following DNS records to your domain provider (e.g., Namecheap, Cloudflare, or Vercel DNS):

## Custom Domain: nichestream.ai

| Type | Name | Value | Purpose |
| :--- | :--- | :--- | :--- |
| A | @ | 76.76.21.21 | Vercel Apex Domain |
| CNAME | www | cname.vercel-dns.com. | Vercel WWW Subdomain |
| TXT | @ | google-site-verification=n2htv5lEiTW7Avq8V0zY0JVZPfyqZWKViT8llKG_zDA | Google Search Console Permanent Verification |

## Verification Strategy
We have implemented a three-layered verification strategy:
1. **DNS TXT Record**: The most robust and permanent method.
2. **Meta Tag**: Integrated into the site's global layout.
3. **HTML Verification File**: Uploaded to the public root.
