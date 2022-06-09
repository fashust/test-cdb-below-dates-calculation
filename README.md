# Test/check what exactly dates will CDB expected based on input data

> **important note** - it's relevant only for belowThreshold tenders

## Example:
```bash
pip install -r requirements.txt
python test_cdb_dates_calculation.py 2022-05-27T15:39:12 2022-06-02T00:00:00 2022-06-02T00:00:00 2022-06-05T00:00:00
name                  requested            calculated by CDB
--------------------  -------------------  -------------------
enquiry period start  2022-05-27T15:39:12  2022-05-28T00:00:00
enquiry period end    2022-06-02T00:00:00  2022-06-02T00:00:00
tender period start   2022-06-02T00:00:00  2022-06-02T00:00:00
tender period end     2022-06-05T00:00:00  2022-06-04T00:00:00
```

## Common description

```
python test_cdb_dates_calculation.py enquiryPeriodStartDT enquiryPeriodEndDT tenderPeriodStartDT tenderPeriodEndDT
```