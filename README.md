# Zadara Storage MCP Server

An MCP (Model Context Protocol) server that provides access to Zadara Storage APIs, including both VPSA Storage Array and Object Storage endpoints.

## Features

### VPSA Storage Array Support
- List, create, get, and delete volumes
- List storage pools
- List connected servers
- Create and list snapshots
- Get performance metrics
- List controllers
- Custom API requests for any VPSA endpoint

### Object Storage Support
- List, create, and delete buckets
- **Calculate bucket sizes and statistics**
- **Upload objects to buckets (with AWS Signature V4 authentication)**
- **Download objects from buckets (with AWS Signature V4 authentication)**
- **Delete objects from buckets (with AWS Signature V4 authentication)**
- List objects in buckets
- Get and set bucket policies
- Get and set bucket versioning
- Custom API requests for any Object Storage endpoint

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The server requires environment variables for authentication:

### VPSA Storage Array
```bash
export ZADARA_VPSA_URL="https://your-vpsa-hostname.com"
export ZADARA_VPSA_API_KEY="your-api-key"
```

### Object Storage
```bash
export ZADARA_OBJECT_STORAGE_URL="https://your-object-storage-url.com"
export ZADARA_OBJECT_ACCESS_KEY="your-access-key"
export ZADARA_OBJECT_SECRET_KEY="your-secret-key"
```

## Running the Server

### Standalone Mode
```bash
python server.py
```

### With Claude Desktop

Add this configuration to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "zadara-storage": {
      "command": "python",
      "args": ["/path/to/zadara-mcp-server/server.py"],
      "env": {
        "ZADARA_VPSA_URL": "https://your-vpsa-hostname.com",
        "ZADARA_VPSA_API_KEY": "your-api-key",
        "ZADARA_OBJECT_STORAGE_URL": "https://your-object-storage-url.com",
        "ZADARA_OBJECT_ACCESS_KEY": "your-access-key",
        "ZADARA_OBJECT_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

## Available Tools

### VPSA Storage Array Tools

#### `vpsa_list_volumes`
List all volumes in the VPSA storage array.

**Parameters:**
- `limit` (optional): Maximum number of volumes to return
- `offset` (optional): Offset for pagination

#### `vpsa_create_volume`
Create a new volume in the VPSA storage array.

**Parameters:**
- `name` (required): Name of the volume
- `capacity` (required): Capacity in GB
- `pool` (required): Storage pool name or ID
- `block_size` (optional): Block size in KB

#### `vpsa_get_volume`
Get details of a specific volume.

**Parameters:**
- `volume_id` (required): Volume ID or name

#### `vpsa_delete_volume`
Delete a volume from the VPSA storage array.

**Parameters:**
- `volume_id` (required): Volume ID or name to delete

#### `vpsa_list_pools`
List all storage pools in the VPSA.

#### `vpsa_list_servers`
List all servers connected to the VPSA.

#### `vpsa_create_snapshot`
Create a snapshot of a volume.

**Parameters:**
- `volume_id` (required): Volume ID to snapshot
- `snapshot_name` (required): Name for the snapshot

#### `vpsa_list_snapshots`
List all snapshots.

**Parameters:**
- `volume_id` (optional): Filter by volume ID

#### `vpsa_get_performance`
Get performance metrics for the VPSA.

**Parameters:**
- `interval` (optional): Time interval (e.g., '1h', '24h', '7d')

#### `vpsa_list_controllers`
List all controllers in the VPSA.

#### `vpsa_custom_request`
Make a custom API request to VPSA Storage Array.

**Parameters:**
- `method` (required): HTTP method (GET, POST, PUT, DELETE)
- `endpoint` (required): API endpoint path (without /api/ prefix)
- `data` (optional): Request body data
- `params` (optional): Query parameters

### Object Storage Tools

#### `object_list_buckets`
List all buckets in object storage.

#### `object_create_bucket`
Create a new bucket in object storage.

**Parameters:**
- `bucket_name` (required): Name of the bucket to create
- `region` (optional): Region for the bucket

#### `object_delete_bucket`
Delete a bucket from object storage.

**Parameters:**
- `bucket_name` (required): Name of the bucket to delete

#### `object_get_bucket_sizes`
Calculate the total size of all buckets or specific buckets.

**Parameters:**
- `bucket_names` (optional): Array of specific bucket names to calculate sizes for. If omitted, calculates sizes for all buckets.

**Returns:**
- Per-bucket statistics: name, total size in bytes, formatted size string, object count
- Summary statistics: total size across all buckets, total object count, successful bucket count
- Handles errors gracefully on a per-bucket basis

**Features:**
- Automatically handles pagination for buckets with >1000 objects
- Supports calculating sizes for all buckets or specific subsets
- Human-readable size formatting (bytes, KB, MB, GB)
- Continues processing remaining buckets if one fails

**Example Response:**
```json
{
  "buckets": [
    {
      "bucket": "backup",
      "total_size_bytes": 1073741824,
      "size_formatted": "1.00 GB",
      "object_count": 1523,
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

#### `object_list_objects`
List objects in a bucket.

**Parameters:**
- `bucket_name` (required): Name of the bucket
- `prefix` (optional): Prefix filter for object keys
- `max_keys` (optional): Maximum number of keys to return

#### `object_upload`
Upload an object to object storage.

**Parameters:**
- `bucket_name` (required): Name of the bucket
- `object_key` (required): Object key/path (e.g., 'document.pdf' or 'folder/file.txt')
- `content_base64` (required): Base64-encoded file content
- `content_type` (optional): MIME type (default: application/octet-stream)

**Note:** This tool uses AWS Signature V4 authentication for secure uploads.

#### `object_download`
Download an object from object storage.

**Parameters:**
- `bucket_name` (required): Name of the bucket
- `object_key` (required): Object key/path

**Returns:** Base64-encoded file content with metadata

**Note:** This tool uses AWS Signature V4 authentication for secure downloads.

#### `object_delete`
Delete an object from object storage.

**Parameters:**
- `bucket_name` (required): Name of the bucket
- `object_key` (required): Object key/path to delete

**Note:** This tool uses AWS Signature V4 authentication for secure deletions.

#### `object_get_bucket_policy`
Get the policy of a bucket.

**Parameters:**
- `bucket_name` (required): Name of the bucket

#### `object_set_bucket_policy`
Set the policy of a bucket.

**Parameters:**
- `bucket_name` (required): Name of the bucket
- `policy` (required): Bucket policy JSON

#### `object_get_bucket_versioning`
Get versioning configuration of a bucket.

**Parameters:**
- `bucket_name` (required): Name of the bucket

#### `object_set_bucket_versioning`
Set versioning configuration of a bucket.

**Parameters:**
- `bucket_name` (required): Name of the bucket
- `status` (required): Versioning status (Enabled or Suspended)

#### `object_custom_request`
Make a custom API request to Object Storage.

**Parameters:**
- `method` (required): HTTP method (GET, POST, PUT, DELETE)
- `endpoint` (required): API endpoint path
- `data` (optional): Request body data
- `params` (optional): Query parameters

## Usage Examples

Once configured with Claude Desktop, you can interact with the server using natural language:

```
"List all volumes in my VPSA storage"
"Create a new volume named 'backup-vol' with 100GB capacity in pool 'pool-1'"
"Show me all buckets in my object storage"
"Create a snapshot of volume 'vol-123' named 'snapshot-2024'"
"List all objects in bucket 'my-data-bucket'"
```

## API Documentation

For detailed API documentation, refer to:
- VPSA Storage Array: https://api-doc.zadarastorage.com/?urls.primaryName=VPSA%20Storage%20Array%20-%20VPSA%20Flash%20Array
- Object Storage: https://api-doc.zadarastorage.com/?urls.primaryName=Object%20Storage

## Authentication

### VPSA Storage Array
The VPSA API uses API key authentication via the `X-Access-Key` header.

### Object Storage
The Object Storage API uses AWS S3-compatible authentication with **AWS Signature Version 4**:
- Access Key and Secret Key are used to generate request signatures
- Each request is signed with HMAC-SHA256
- Payload hashing ensures data integrity
- Canonical headers include host, date, and content hash
- Compatible with standard S3 authentication

**Object operations (upload, download, delete)** use AWS Signature V4 for enhanced security and compatibility with S3-compatible tools.

## Error Handling

The server will return error messages in the following cases:
- Missing or invalid credentials
- Invalid API endpoints
- Network connectivity issues
- API rate limiting
- Invalid parameters

## Development

To extend this server with additional tools:

1. Add the tool definition to the `list_tools()` function
2. Implement the tool handler in the `call_tool()` function
3. Use the `ZadaraClient` class methods to make API requests

## Security Notes

- Never commit your API keys or credentials to version control
- Use environment variables for all sensitive configuration
- Ensure your VPSA and Object Storage endpoints use HTTPS
- Regularly rotate your API keys
- Follow the principle of least privilege when creating API keys

## Troubleshooting

### Connection Issues
- Verify your VPSA_URL and OBJECT_STORAGE_URL are correct
- Check network connectivity to your Zadara endpoints
- Ensure firewall rules allow outbound HTTPS connections

### Authentication Errors
- Verify your API keys are correct
- Check that your API keys have the necessary permissions
- Ensure keys haven't expired

### Tool Not Working
- Check the server logs for detailed error messages
- Verify the tool parameters match the expected schema
- Test the API endpoint directly using curl or Postman

## License

This MCP server is provided as-is for use with Zadara Storage systems.

## Support

For Zadara Storage API support, refer to the official Zadara documentation or contact Zadara support.

For MCP server issues, please check the MCP documentation at https://modelcontextprotocol.io/
