# Fault Scenarios & Interview Talking Points

This document tracks all data quality faults injected into the dataset and how they were detected and remediated. Use this to prepare for interview questions about data quality issues and incident response.

## Fault Scenarios

### 1. NULL payment_status (18.7% of payments)

**Scenario:** Payment API renamed field from `paymentStatus` to `payment_status`, causing NULL values in new records.

**Detection:**
- NULL check on `payment_status` column
- Row count anomaly: sudden increase in NULL percentage
- Freshness check: issue appeared after specific timestamp

**Remediation:**
- Backfill NULL values based on transaction_id mapping to payment gateway logs
- Update ingestion pipeline to handle both field names during transition
- Add schema validation to catch field name changes early

**Interview Talking Points:**
- "This simulates a real-world API contract change without proper migration"
- "I used NULL checks combined with temporal analysis to identify when the issue started"
- "The fix involved both data remediation (backfill) and pipeline hardening (schema validation)"
- "This demonstrates understanding of data contracts and the importance of schema evolution"

---

### 2. NULL customer_id in orders (2% of orders)

**Scenario:** Orphaned orders due to customer deletion or failed customer creation during order placement.

**Detection:**
- NULL check on `customer_id` foreign key
- Referential integrity check between orders and customers
- Business rule: all orders must have a valid customer

**Remediation:**
- Identify if these are test orders or production issues
- If test orders: mark with special status or delete
- If production: reconstruct customer from order metadata or create placeholder customer record
- Add validation at order creation to prevent future orphaned orders

**Interview Talking Points:**
- "Foreign key NULLs can indicate upstream system failures"
- "I used referential integrity checks to catch orphaned records"
- "The remediation strategy depends on business context - test vs production data"
- "Prevention is better than cure: added validation at the ingestion point"

---

### 3. Duplicate customer emails (0.5%)

**Scenario:** User registration race condition or migration issue creating duplicate customer records.

**Detection:**
- Duplicate check on unique constraint field (email)
- Count of emails > 1 per customer

**Remediation:**
- Merge duplicate customer records
- Keep most recent record, consolidate order history
- Add unique constraint enforcement at database level
- Implement idempotent registration logic

**Interview Talking Points:**
- "Duplicates often come from lack of idempotency in upstream systems"
- "I used unique constraint validation to detect duplicates"
- "Remediation required merging records while preserving data integrity"
- "This highlights the importance of idempotent operations in data pipelines"

---

### 4. Duplicate product SKUs (0.5%)

**Scenario:** Product catalog sync issue or manual data entry error.

**Detection:**
- Duplicate check on SKU (should be unique)
- Count of SKUs > 1 per product

**Remediation:**
- Identify which product record is correct (based on created_at, updated_at)
- Deactivate duplicate SKUs or merge product records
- Add unique constraint on SKU column
- Implement upsert logic for product sync

**Interview Talking Points:**
- "SKU duplicates break inventory management and reporting"
- "Detection via unique constraint validation"
- "Remediation involved data deduplication and adding database constraints"
- "This shows understanding of master data management"

---

### 5. Negative product prices (0.2%)

**Scenario:** Data entry error or pricing calculation bug.

**Detection:**
- Range check on price column (price > 0)
- Business rule validation

**Remediation:**
- Identify source of negative prices
- Correct with absolute value or fetch from source system
- Add validation rule: price must be positive
- Implement data quality checks at ingestion

**Interview Talking Points:**
- "Negative prices are business logic violations"
- "Range checks caught this anomaly"
- "Remediation required understanding the root cause - data entry vs calculation"
- "Added validation at multiple layers: database and application"

---

### 6. Invalid order status values (0.3%)

**Scenario:** Hardcoded status values in code not matching database enum/check constraint.

**Detection:**
- Schema check: values not in allowed set
- Data profiling to find unique status values

**Remediation:**
- Map invalid statuses to valid ones based on business rules
- Update application code to use only valid statuses
- Add enum type or check constraint at database level
- Implement status transition validation

**Interview Talking Points:**
- "Invalid status values indicate schema drift or code bugs"
- "Schema checks detected values outside the allowed set"
- "Remediation involved both data correction and code fixes"
- "This demonstrates the importance of schema enforcement"

---

### 7. Future order dates (0.2%)

**Scenario:** System clock issues or timezone handling errors.

**Detection:**
- Range check: order_date <= current_timestamp
- Freshness check with temporal bounds

**Remediation:**
- Investigate timezone configuration
- Correct dates based on order sequence or metadata
- Add temporal validation at ingestion
- Standardize timezone handling across systems

**Interview Talking Points:**
- "Future dates often indicate timezone or clock synchronization issues"
- "Temporal range checks caught this anomaly"
- "Remediation required understanding the root cause - timezone vs clock"
- "Highlights the importance of consistent time handling in data pipelines"

---

### 8. High revenue outliers (0.5%)

**Scenario:** Data entry error, fraud, or test data in production.

**Detection:**
- Statistical anomaly detection (z-score, IQR)
- Business rule: orders above threshold (e.g., $10,000) require review

**Remediation:**
- Flag for manual review
- If error: correct with reasonable value
- If fraud: preserve for investigation
- Add anomaly detection alerts

**Interview Talking Points:**
- "Outliers can be legitimate (high-value customers) or errors"
- "Used statistical methods (z-score) to detect anomalies"
- "Remediation depends on context - error vs fraud vs legitimate"
- "This shows understanding of anomaly detection in data quality"

---

### 9. Referential integrity - orphaned product references

**Scenario:** Product deleted but order_items still reference it.

**Detection:**
- Referential integrity check between order_items and products
- Foreign key validation

**Remediation:**
- Restore deleted products if needed for historical orders
- Add soft delete instead of hard delete
- Implement cascade rules or restrict deletion
- Add foreign key constraints with appropriate ON DELETE behavior

**Interview Talking Points:**
- "Hard deletes break referential integrity in historical data"
- "Referential integrity checks caught orphaned references"
- "Remediation involved restoring data and changing deletion strategy"
- "This demonstrates understanding of data lifecycle management"

---

## Detection Methods Summary

| Method | What It Catches | Faults Detected |
|--------|----------------|-----------------|
| NULL check | Missing required data | payment_status, customer_id |
| Duplicate check | Non-unique unique fields | emails, SKUs |
| Schema check | Values outside allowed set | invalid statuses |
| Range check | Values outside valid range | negative prices, future dates |
| Referential integrity | Broken foreign keys | orphaned products |
| Statistical anomaly | Outliers | high revenue |
| Row count anomaly | Unexpected volume changes | NULL spikes |

## Interview Questions & Answers

### Q: How do you approach data quality issues?

**A:** "I take a layered approach:
1. **Prevention**: Schema validation, constraints, idempotent operations
2. **Detection**: Automated checks (NULL, duplicate, schema, range, referential integrity)
3. **Remediation**: Understand root cause, fix data, fix pipeline, add monitoring
4. **Monitoring**: Continuous checks with alerts for regressions

For example, in this project I injected 9 different fault scenarios and built detection methods for each, then documented the remediation strategies."

### Q: How do you prioritize data quality issues?

**A:** "I prioritize based on:
1. **Business impact**: Does this affect revenue, reporting, or customer experience?
2. **Data volume**: How many records are affected?
3. **Urgency**: Is this blocking downstream processes?
4. **Root cause**: Is this a one-time issue or systemic?

For example, NULL payment_status at 18.7% is high priority because it affects payment processing, while a few duplicate SKUs might be lower priority."

### Q: How do you prevent data quality issues from recurring?

**A:** "I focus on:
1. **Schema enforcement**: Database constraints, validation rules
2. **Contract testing**: Validate data contracts between systems
3. **Monitoring**: Automated checks with alerts
4. **Process improvements**: Idempotent operations, soft deletes
5. **Documentation**: Data dictionaries, schema evolution policies

In this project, each fault scenario led to specific prevention measures - like adding unique constraints for SKUs or implementing schema validation for API changes."

### Q: How do you handle schema changes?

**A:** "I follow a schema evolution strategy:
1. **Backward compatibility**: Support old and new field names during transition
2. **Validation**: Detect schema drift early
3. **Migration**: Plan data migration for breaking changes
4. **Communication**: Document and communicate changes to consumers

The payment_status scenario demonstrates this - the API renamed a field without proper migration, causing NULLs. The fix involved supporting both names during transition and adding schema validation."

### Q: How do you measure data quality?

**A:** "I use both quantitative and qualitative metrics:
1. **Completeness**: Percentage of NULL values in required fields
2. **Uniqueness**: Duplicate rate in unique fields
3. **Validity**: Percentage of values passing schema/range checks
4. **Consistency**: Referential integrity pass rate
5. **Timeliness**: Data freshness metrics
6. **Accuracy**: Sample validation against source systems

Each fault scenario in this project maps to one or more of these dimensions."

---

## Notes

- Add new fault scenarios as they are discovered or injected
- Update remediation strategies as they are implemented
- Refine interview talking points based on actual experience
- Link to specific code commits or pipeline runs for each scenario
