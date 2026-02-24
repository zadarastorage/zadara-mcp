# Quick Reference: Bucket Size Calculation

## Tool Name
`object_get_bucket_sizes`

## Purpose
Calculate total storage usage across buckets in Zadara Object Storage

## Quick Examples

### Get All Bucket Sizes
```json
{
  "bucket_names": null
}
```
**Claude**: "Show me the size of all my buckets"

### Get Specific Bucket Size
```json
{
  "bucket_names": ["backup"]
}
```
**Claude**: "How big is the backup bucket?"

### Get Multiple Bucket Sizes
```json
{
  "bucket_names": ["backup", "media", "logs"]
}
```
**Claude**: "What's the size of backup, media, and logs?"

## Response Fields

### Per Bucket
- `bucket` - Bucket name
- `total_size_bytes` - Size in bytes (number)
- `size_formatted` - Human-readable size (string)
- `object_count` - Number of objects (number)
- `error` - Error message if failed (string or null)

### Summary
- `total_size_bytes` - Total across all buckets
- `size_formatted` - Human-readable total
- `total_objects` - Total object count
- `bucket_count` - Number of successfully processed buckets

## Natural Language Queries

### General Usage
- "Show me the size of all my buckets"
- "How much storage am I using?"
- "What's my total object storage usage?"
- "List bucket sizes"

### Specific Buckets
- "How big is the backup bucket?"
- "What's the size of my media bucket?"
- "Show me the size of bucket X"

### Multiple Buckets
- "Calculate sizes for backup, media, and logs"
- "What's the total size of backup and archive buckets?"
- "Show me sizes for my production buckets"

### Comparative Queries
- "Which bucket is using the most space?"
- "Show me my largest buckets"
- "What's my storage usage by bucket?"

## Size Formatting

| Range | Format | Example |
|-------|--------|---------|
| < 1 KB | bytes | "523 bytes" |
| 1 KB - 1 MB | KB | "45.67 KB" |
| 1 MB - 1 GB | MB | "234.56 MB" |
| >= 1 GB | GB | "12.34 GB" |

## Features

✅ Automatic pagination (handles >1000 objects)  
✅ All buckets or specific subsets  
✅ Human-readable formatting  
✅ Summary statistics  
✅ Graceful error handling  
✅ No bucket modifications  

## Performance Notes

- **Small buckets** (<100 objects): < 1 second
- **Medium buckets** (100-1000 objects): 1-3 seconds  
- **Large buckets** (1000-10000 objects): 3-30 seconds
- **Very large buckets** (>10000 objects): May take minutes

## Permissions Required

- S3 `ListBucket` permission on target buckets
- Read access to bucket metadata

## Common Use Cases

1. **Storage Auditing**: "Show me total storage usage"
2. **Cost Analysis**: "Which buckets are using the most space?"
3. **Cleanup Planning**: "Find my largest buckets for cleanup"
4. **Capacity Planning**: "What's my current storage utilization?"
5. **Backup Verification**: "How much data is in my backup bucket?"

## Error Handling

If a bucket fails:
- Other buckets continue processing
- Error is reported in bucket's `error` field
- Bucket is excluded from summary totals
- User sees which buckets succeeded/failed

## Integration with Other Tools

### Before Cleanup
```
1. object_get_bucket_sizes - See what's using space
2. object_list_objects - List objects in large bucket
3. object_delete - Remove unnecessary objects
4. object_get_bucket_sizes - Verify space freed
```

### Monitoring Workflow
```
1. object_get_bucket_sizes - Weekly storage audit
2. Compare with previous results
3. Investigate anomalies
4. Plan capacity/cleanup
```

## Tips

💡 **Regular Monitoring**: Run weekly to track growth  
💡 **Combine with List**: Use with `object_list_objects` to find large files  
💡 **Backup Validation**: Verify backup bucket sizes match expectations  
💡 **Cost Optimization**: Identify candidates for lifecycle policies  

## Limitations

⚠️ Only counts current object versions (not historical)  
⚠️ Large buckets may take time to calculate  
⚠️ Requires proper authentication  
⚠️ Respects S3 API rate limits  

---
**Version**: 1.3.0  
**Last Updated**: 2026-02-24
