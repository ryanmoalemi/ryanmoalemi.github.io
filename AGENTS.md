# Notes for contributors and agents

## Section order

On the home page, the post template, the about page, and any hub, put the most engaging block directly under the intro or hero. Engaging content is the latest or best posts, photos, galleries, and tools. Order the rest from most interesting to least interesting. End with notes, disclosures, and fine print.

Move existing sections only. Do not rewrite or remove copy to change the order. Keep the full hero title above the fold on desktop and mobile. Keep each photo's credit with the photo. If a page is already in this order, leave it alone.

## Punctuation

Do not use em dashes. When a title needs a separator, use ` | `.

## Before publishing

Fact-check titles, meta descriptions, alt text, and structured data on AI-assisted content before publishing.

Never bump dates without a real content change.

## Feed

`feed.xml` is built from post meta tags by `scripts/build_feed.py` (runs in Actions on push). New posts need `article:published_time`, `og:title`, `og:url` and a meta description.
