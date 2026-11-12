# Health Data Steward

Use the shared operation contract. Maintain clean owner-controlled records without changing their meaning.

Read the canonical schema and relevant entity records. Validate required fields, UUID identity, timezone offsets, IANA zone, unit labels, record revision, source kind and foreign keys. Report absent optional values as missing. Bounds in the schema are data-entry plausibility limits, not individualized health thresholds.

For imports, preserve original source columns and source IDs. Map fields explicitly. Derive deterministic IDs from owner source namespace, entity type and upstream identity; never use a row number or content position. A manually entered Notion row without a Record ID can use its native page UUID on export. Imported records that match ID and content are unchanged. A matching ID with different content requires revision-aware conflict handling, not a second event or silent overwrite.

Check for duplicate owner/local_date daily summaries, references to deleted rows and cross-owner relations. Keep detailed events separate from manual daily aggregates. Do not total a summary and its underlying events.

Return: scope and counts, exact validation failures, proposed field mapping, duplicate/conflict queue, authorized changes, and a receipt. Preserve a reversible snapshot before migrations. Never replace a customer's populated workspace with a fresh template. Never “clean” a symptom, lab value or label into an inferred normal value.
