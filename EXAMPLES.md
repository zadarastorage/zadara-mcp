# Usage Examples

This document provides practical examples of using the Zadara Storage MCP Server with Claude Desktop.

## VPSA Storage Array Examples

### Volume Management

#### List All Volumes
```
"Show me all volumes in my storage array"
"List volumes with pagination - limit 10"
```

Expected Response: List of volumes with details like name, capacity, pool, status, etc.

#### Create a Volume
```
"Create a new volume named 'backup-volume' with 500GB capacity in pool 'pool-1'"
"Add a 1TB volume called 'database-storage' to pool 'ssd-pool' with 4KB block size"
```

Example parameters:
- Name: "backup-volume"
- Capacity: 500 (GB)
- Pool: "pool-1"
- Block size: 4 (KB, optional)

#### Get Volume Details
```
"Show me details of volume 'backup-volume'"
"What's the status of volume vol-00001?"
```

#### Delete a Volume
```
"Delete volume 'old-backup'"
"Remove volume vol-00001 from storage"
```

⚠️ **Warning**: This permanently deletes the volume!

### Pool Management

#### List Storage Pools
```
"What storage pools are available?"
"Show me all pools in the VPSA"
"List pools with their capacity and usage"
```

Expected Response: Pools with name, capacity, available space, RAID level, etc.

### Server Management

#### List Connected Servers
```
"Show me all servers connected to the storage"
"List servers accessing the VPSA"
"Which hosts are connected?"
```

### Snapshot Management

#### Create Snapshots
```
"Create a snapshot of volume 'production-db' named 'daily-backup-2024-01-15'"
"Take a snapshot of vol-00001 called 'before-upgrade'"
```

#### List Snapshots
```
"Show me all snapshots"
"List snapshots for volume 'production-db'"
"What snapshots exist?"
```

### Performance Monitoring

#### Get Performance Metrics
```
"Show me performance metrics for the last hour"
"Get VPSA performance stats for the last 24 hours"
"Display performance data with 7 day interval"
```

Example intervals:
- "1h" - Last hour
- "24h" - Last 24 hours
- "7d" - Last 7 days

### Controller Management

#### List Controllers
```
"Show me all controllers"
"List VPSA controllers and their status"
"What controllers are active?"
```

## Object Storage Examples

### Bucket Management

#### List Buckets
```
"Show me all buckets in object storage"
"List my S3-compatible buckets"
"What buckets exist?"
```

#### Create a Bucket
```
"Create a new bucket named 'backup-data'"
"Add bucket 'media-storage' in region us-east-1"
```

#### Delete a Bucket
```
"Delete bucket 'old-backups'"
"Remove bucket 'temporary-storage'"
```

⚠️ **Warning**: Bucket must be empty before deletion!

### Object Management

#### List Objects
```
"List all objects in bucket 'backup-data'"
"Show me files in 'media-storage' bucket with prefix 'images/'"
"Get first 100 objects from bucket 'logs'"
```

Example parameters:
- Bucket: "backup-data"
- Prefix: "images/" (optional filter)
- Max keys: 100 (optional limit)

### Bucket Policies

#### Get Bucket Policy
```
"Show me the policy for bucket 'backup-data'"
"What's the access policy on 'public-files' bucket?"
```

#### Set Bucket Policy
```
"Set a policy on bucket 'backup-data' to allow public read access"
```

Example policy JSON:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicRead",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::backup-data/*"
  }]
}
```

### Bucket Versioning

#### Get Versioning Status
```
"Is versioning enabled on bucket 'backup-data'?"
"Check versioning status for 'documents' bucket"
```

#### Enable Versioning
```
"Enable versioning on bucket 'important-files'"
"Turn on versioning for 'backup-data'"
```

#### Suspend Versioning
```
"Suspend versioning on bucket 'temp-storage'"
"Disable versioning for 'old-bucket'"
```

## Advanced Examples

### Custom API Requests

#### VPSA Custom Request
```
"Make a GET request to VPSA endpoint 'raid_groups.json'"
"Call VPSA API endpoint 'settings/nfs.json' with GET method"
```

Example for POST:
```
"Make a custom VPSA API call:
- Method: POST
- Endpoint: volumes/vol-001/attach.json
- Data: {server: 'srv-001', access_type: 'readwrite'}"
```

#### Object Storage Custom Request
```
"Make a GET request to Object Storage endpoint '/bucket-name?lifecycle'"
"Call Object Storage API at '/bucket-name?tagging' with GET"
```

### Complex Workflows

#### Backup Workflow
```
1. "List all volumes"
2. "Create snapshot of volume 'prod-db' named 'backup-{date}'"
3. "List snapshots to verify creation"
```

#### Storage Audit
```
1. "Show me all volumes with their capacities"
2. "List all storage pools and their usage"
3. "Get performance metrics for the last 24 hours"
4. "Show me all connected servers"
```

#### Object Storage Setup
```
1. "Create bucket 'new-project-data'"
2. "Enable versioning on bucket 'new-project-data'"
3. "Set bucket policy for 'new-project-data' to allow team access"
4. "List objects in 'new-project-data' to verify"
```

## Natural Language Examples

The MCP server understands natural language, so you can ask questions in various ways:

### Informal Questions
```
"How much storage do I have left?"
"What's eating up my storage space?"
"Can you show me my backup volumes?"
"Do I have any snapshots from last week?"
```

### Task-Oriented Requests
```
"I need to create a 2TB volume for the new database"
"Help me set up a new storage bucket for logs"
"Find all volumes that start with 'prod-'"
"Clean up old snapshots from January"
```

### Information Requests
```
"What's the difference between my storage pools?"
"Which volumes are using the most space?"
"Are there any performance issues in the last hour?"
"What buckets have versioning enabled?"
```

## Error Handling Examples

### Handling Common Errors

#### Volume Already Exists
```
Request: "Create volume 'test-vol' with 100GB in pool-1"
Error: "Volume with name 'test-vol' already exists"
Solution: Choose a different name or delete the existing volume
```

#### Insufficient Space
```
Request: "Create volume 'huge-vol' with 10TB in pool-1"
Error: "Pool 'pool-1' has insufficient available space"
Solution: Choose a smaller size or different pool
```

#### Bucket Not Empty
```
Request: "Delete bucket 'data-bucket'"
Error: "Bucket must be empty before deletion"
Solution: Delete all objects first, then delete bucket
```

#### Authentication Failed
```
Error: "Invalid API key or unauthorized access"
Solution: Verify credentials in configuration
```

## Best Practices

### Volume Management
- Always specify meaningful names for volumes
- Use consistent naming conventions (e.g., `{project}-{purpose}-{date}`)
- Document volume purposes in descriptions
- Regularly review and cleanup unused volumes

### Snapshot Management
- Create snapshots before major changes
- Use descriptive snapshot names with timestamps
- Implement retention policies (delete old snapshots)
- Test snapshot restoration procedures

### Object Storage
- Use appropriate bucket names (DNS-compliant)
- Enable versioning for critical data
- Implement lifecycle policies for cost optimization
- Use appropriate access policies (least privilege)

### Monitoring
- Regularly check performance metrics
- Set up alerts for capacity thresholds
- Monitor controller health
- Review server connections

## Tips and Tricks

### Efficient Querying
```
Instead of: "Show me everything about storage"
Better: "List volumes with their capacity and pool assignments"
```

### Batch Operations
```
"Show me volumes, pools, and performance metrics"
```

### Using Filters
```
"List snapshots for volume 'prod-db' created in the last 7 days"
"Show objects in bucket 'logs' with prefix '2024/'"
```

### Combining Information
```
"Check if I have enough space in pool-1 to create a 500GB volume, and show me current pool usage"
```

## Troubleshooting Examples

### Volume Issues
```
"Why can't I delete volume 'test-vol'?"
→ Check if volume is attached to servers
→ Verify volume status is 'available'
```

### Performance Issues
```
"Why is my storage slow?"
→ "Show me performance metrics for the last hour"
→ "List all active servers and their connections"
→ "Check controller status"
```

### Bucket Access Issues
```
"I can't access bucket 'private-data'"
→ "Show me the policy for bucket 'private-data'"
→ Verify credentials and permissions
```

## Integration Examples

### With Monitoring Tools
```
1. Get performance metrics
2. Export to monitoring system
3. Set up alerts based on thresholds
```

### With Backup Scripts
```
1. List volumes to backup
2. Create snapshots with timestamps
3. Verify snapshot creation
4. Log results
```

### With Automation
```
1. Check available space
2. If low, create alert
3. List largest volumes
4. Recommend cleanup actions
```
