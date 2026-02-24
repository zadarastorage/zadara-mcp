# Zadara MCP Server v1.3.0 - Bucket Size Calculation Update

## Summary

This update adds bucket size calculation functionality to the Zadara Storage MCP Server, allowing users to easily determine storage usage across their object storage buckets.

## What's New in v1.3.0

### New Tool: `object_get_bucket_sizes`

A new tool that calculates the total size and object count for buckets in your Zadara Object Storage.

**Key Features:**
- Calculate sizes for all buckets or specific buckets
- Automatic pagination support for buckets with >1000 objects
- Returns both raw bytes and human-readable formatted sizes
- Per-bucket statistics and summary across all buckets
- Graceful error handling - continues processing if individual buckets fail

**Parameters:**
- `bucket_names` (optional): Array of specific bucket names to calculate sizes for
  - If omitted, calculates sizes for all buckets in the storage account

**Response Format:**
```json
{
  "buckets": [
    {
      "bucket": "backup",
      "total_size_bytes": 1073741824,
      "size_formatted": "1.00 GB",
      "object_count": 1523,
      "error": null
    },
    {
      "bucket": "media",
      "total_size_bytes": 524288000,
      "size_formatted": "500.00 MB",
      "object_count": 245,
      "error": null
    }
  ],
  "summary": {
    "total_size_bytes": 5368709120,
    "size_formatted": "5.00 GB",
    "total_objects": 4567,
    "bucket_count": 11
  }
}
```

## Usage Examples

### Get Sizes for All Buckets
```
User: "Show me the size of all my buckets"
Claude: [calls object_get_bucket_sizes with no parameters]
```

### Get Size for Specific Bucket
```
User: "How big is the backup bucket?"
Claude: [calls object_get_bucket_sizes with bucket_names: ["backup"]]
```

### Get Sizes for Multiple Specific Buckets
```
User: "Calculate sizes for backup, media, and logs buckets"
Claude: [calls object_get_bucket_sizes with bucket_names: ["backup", "media", "logs"]]
```

### Natural Language Queries
```
"How much storage am I using?"
"What's the total size across all buckets?"
"Show me storage usage by bucket"
"Which bucket is using the most space?"
```

## Technical Implementation

### How It Works

1. **Bucket Discovery**: If no specific buckets are provided, the tool first lists all buckets in the storage account

2. **Object Iteration**: For each bucket, it iterates through all objects using the S3-compatible ListObjectsV2 API

3. **Pagination**: Automatically handles pagination using continuation tokens for buckets with more than 1000 objects

4. **Size Calculation**: Sums up the size of all objects in each bucket

5. **Formatting**: Converts raw byte counts to human-readable formats (KB, MB, GB)

6. **Error Handling**: If a bucket fails (permissions, network issues, etc.), the tool continues processing remaining buckets and reports the error

### Performance Considerations

- **Pagination**: Each API call retrieves up to 1000 objects. For large buckets, multiple API calls are made automatically.
- **Rate Limiting**: The tool respects AWS Signature V4 authentication and standard S3 rate limits
- **Network Efficiency**: All size calculations are done server-side - only metadata is transferred, not file contents

## Files Updated

### Core Server Files
- `server.py` - Added `object_get_bucket_sizes` tool definition and implementation
- `VERSION` - Updated to 1.3.0

### Documentation Files
- `CHANGELOG.md` - Added v1.3.0 changelog entry
- `README.md` - Updated features list and added tool documentation
- `EXAMPLES.md` - Added usage examples for bucket size calculation

### Test Files
- `test_bucket_sizes.py` - New test script demonstrating the functionality

## Implementation Details

### Tool Definition
```python
Tool(
    name="object_get_bucket_sizes",
    description="Calculate the total size of all buckets or specific buckets. Returns bucket names, object counts, total sizes, and formatted size strings.",
    inputSchema={
        "type": "object",
        "properties": {
            "bucket_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of specific bucket names to calculate sizes for. If omitted, calculates sizes for all buckets."
            }
        }
    }
)
```

### Tool Handler
The implementation includes:
- XML parsing for bucket listing and object iteration
- Pagination support with continuation tokens
- Per-bucket error handling
- Human-readable size formatting
- Summary statistics calculation

## Upgrade Instructions

### For Existing Users

1. **Stop the MCP server** if it's running
2. **Backup your current installation** (optional but recommended)
3. **Replace the server files** with the new v1.3.0 files:
   - `server.py`
   - `VERSION`
   - `CHANGELOG.md`
   - `README.md`
   - `EXAMPLES.md`
4. **Restart the MCP server**
5. **Test the new tool** by asking Claude: "Show me the size of all my buckets"

### For New Users

Follow the standard installation instructions in the README.md file.

## Compatibility

- **Backward Compatible**: All existing tools continue to work as before
- **No Breaking Changes**: This is a feature addition only
- **Environment Variables**: No new environment variables required
- **Dependencies**: No new dependencies added

## Testing

### Manual Testing

You can test the new functionality using:

1. **Via Claude Desktop**:
   ```
   "Show me the size of all my buckets"
   "Calculate size for the backup bucket"
   ```

2. **Via Test Script**:
   ```bash
   cd /path/to/zadara-mcp-server
   python test_bucket_sizes.py
   ```

### Expected Results

The tool should:
- Successfully list all buckets (or specified buckets)
- Calculate accurate total sizes by summing all object sizes
- Format sizes appropriately (bytes, KB, MB, GB)
- Handle pagination for large buckets
- Continue processing if individual buckets fail
- Provide summary statistics

## Known Limitations

1. **Performance**: For buckets with millions of objects, the calculation may take several seconds to minutes
2. **Permissions**: Requires LIST permission on buckets to calculate sizes
3. **Versioned Buckets**: If bucket versioning is enabled, only current versions are counted (not historical versions)
4. **Lifecycle Rules**: Objects that are archived or in glacier storage are still counted in the size

## Future Enhancements

Potential improvements for future versions:
- Add caching to avoid recalculating frequently-accessed bucket sizes
- Include versioned object sizes
- Add filtering by object age or prefix
- Support for lifecycle policy-aware calculations
- Parallel bucket processing for faster results

## Support

For issues or questions:
1. Check the EXAMPLES.md file for usage patterns
2. Review the CHANGELOG.md for version-specific information
3. Examine the test_bucket_sizes.py script for implementation details
4. Refer to the Zadara Storage API documentation for S3 compatibility

## Version History

- **v1.3.0** (2026-02-24): Added bucket size calculation tool
- **v1.2.0** (2026-02-20): Enhanced object listing with AWS Signature V4
- **v1.1.0** (2026-02-20): Added object upload/download/delete support
- **v1.0.0** (2026-02-03): Initial release

---

**Author**: Marco  
**Date**: February 24, 2026  
**Version**: 1.3.0
