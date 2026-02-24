# Zadara Storage MCP Server v1.3.0 - Distribution Package

## 📦 Package Contents

This package contains everything you need to run the Zadara Storage MCP Server.

### Core Files
- `server.py` - Main MCP server implementation
- `requirements.txt` - Python dependencies
- `install.sh` - Automated installation script (Unix/Mac)
- `setup.sh` - Quick setup script

### Configuration Files
- `.env.example` - Example environment configuration
- `claude_desktop_config.json.example` - Example Claude Desktop integration

### Documentation
- `README.md` - Complete server documentation
- `QUICKSTART.md` - Quick start guide
- `EXAMPLES.md` - Usage examples and patterns
- `CHANGELOG.md` - Version history
- `UPDATE_SUMMARY_v1.3.0.md` - What's new in this version
- `QUICK_REFERENCE_BUCKET_SIZES.md` - Quick reference for new feature
- `PROJECT_STRUCTURE.md` - Project organization
- `CONTRIBUTING.md` - Contribution guidelines
- `SECURITY.md` - Security best practices
- `RELEASE_NOTES.md` - Release information

### Test Files
- `test.py` - Basic functionality tests
- `test_bucket_sizes.py` - Bucket size calculation tests

## 🚀 Quick Installation

### Automated Installation (Recommended)

**Unix/Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

The installer will:
1. Check Python and pip installation
2. Install required dependencies
3. Guide you through configuration setup
4. Verify the installation

### Manual Installation

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Test the server:**
   ```bash
   python3 server.py
   ```

## 🎯 What's New in v1.3.0

### Bucket Size Calculation Tool

Calculate storage usage across your Zadara Object Storage buckets!

**Features:**
- 📊 Calculate sizes for all buckets or specific buckets
- 🔄 Automatic pagination for large buckets (>1000 objects)
- 📏 Human-readable formatting (bytes, KB, MB, GB)
- 📈 Summary statistics across all buckets
- ✅ Graceful error handling

**Usage Examples:**
```
"Show me the size of all my buckets"
"How big is the backup bucket?"
"Calculate sizes for backup, media, and logs"
"How much storage am I using?"
```

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

See `UPDATE_SUMMARY_v1.3.0.md` for complete details.

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Dependencies**: httpx, mcp (installed automatically)
- **Zadara Storage**: Access to VPSA and/or Object Storage

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your credentials:

```bash
# VPSA Storage Array
ZADARA_VPSA_URL=https://your-vpsa-hostname.com
ZADARA_VPSA_API_KEY=your-api-key

# Object Storage
ZADARA_OBJECT_STORAGE_URL=https://your-object-storage-url.com
ZADARA_OBJECT_ACCESS_KEY=your-access-key
ZADARA_OBJECT_SECRET_KEY=your-secret-key
```

### Claude Desktop Integration

Add to your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "zadara-storage": {
      "command": "python3",
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

See `claude_desktop_config.json.example` for more details.

## 📚 Documentation Guide

### Getting Started
1. **QUICKSTART.md** - Start here for quick setup
2. **README.md** - Complete feature documentation
3. **EXAMPLES.md** - Real-world usage examples

### New Feature
1. **UPDATE_SUMMARY_v1.3.0.md** - Complete v1.3.0 update guide
2. **QUICK_REFERENCE_BUCKET_SIZES.md** - Quick reference card
3. **EXAMPLES.md** - Bucket size calculation examples

### Development
1. **PROJECT_STRUCTURE.md** - Code organization
2. **CONTRIBUTING.md** - How to contribute
3. **test.py** / **test_bucket_sizes.py** - Test scripts

## 🧪 Testing

### Test Basic Functionality
```bash
python3 test.py
```

### Test Bucket Size Calculation
```bash
python3 test_bucket_sizes.py
```

### Interactive Testing with Claude
1. Start the server: `python3 server.py`
2. In Claude Desktop, try:
   - "Show me the size of all my buckets"
   - "List my storage volumes"
   - "Upload a file to bucket 'test'"

## 🌟 Key Features

### VPSA Storage Array
- Volume management (list, create, delete)
- Storage pool information
- Snapshot management
- Performance metrics
- Controller status

### Object Storage
- Bucket management
- **NEW: Bucket size calculation**
- Object upload/download/delete (AWS Signature V4)
- Bucket policies and versioning
- Object listing and search

## 📊 All Available Tools

### Object Storage Tools (15 tools)
- `object_list_buckets` - List all buckets
- `object_create_bucket` - Create new bucket
- `object_delete_bucket` - Delete bucket
- **`object_get_bucket_sizes`** - Calculate bucket sizes (NEW!)
- `object_list_objects` - List objects in bucket
- `object_upload` - Upload objects
- `object_download` - Download objects
- `object_delete` - Delete objects
- `object_get_bucket_policy` - Get bucket policy
- `object_set_bucket_policy` - Set bucket policy
- `object_get_bucket_versioning` - Get versioning config
- `object_set_bucket_versioning` - Set versioning config
- `object_custom_request` - Custom API requests

### VPSA Tools (11 tools)
- `vpsa_list_volumes` - List volumes
- `vpsa_create_volume` - Create volume
- `vpsa_get_volume` - Get volume details
- `vpsa_delete_volume` - Delete volume
- `vpsa_list_pools` - List storage pools
- `vpsa_list_servers` - List servers
- `vpsa_create_snapshot` - Create snapshot
- `vpsa_list_snapshots` - List snapshots
- `vpsa_get_performance` - Get metrics
- `vpsa_list_controllers` - List controllers
- `vpsa_custom_request` - Custom API requests

## 🔐 Security

- AWS Signature V4 authentication for all Object Storage operations
- API key authentication for VPSA operations
- Environment-based credential management
- No credentials stored in code
- See `SECURITY.md` for best practices

## 🆘 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip3 install -r requirements.txt
```

**"Permission denied" when running install.sh:**
```bash
chmod +x install.sh
```

**Authentication failures:**
- Verify credentials in `.env` file
- Check URL formats (include https://)
- Verify API key/access key permissions

**Bucket size calculation takes long:**
- Normal for large buckets (>10,000 objects)
- Uses pagination to handle any bucket size
- Shows progress in real-time

## 📞 Support

- **Documentation**: See README.md and other docs
- **Issues**: See CONTRIBUTING.md for reporting
- **Updates**: See CHANGELOG.md for version history
- **Security**: See SECURITY.md for security practices

## 📜 License

See LICENSE file for details.

## 🎉 Version History

- **v1.3.0** (2026-02-24) - Added bucket size calculation
- **v1.2.0** (2026-02-20) - Enhanced object listing with AWS Signature V4
- **v1.1.0** (2026-02-20) - Added upload/download/delete support
- **v1.0.0** (2026-02-03) - Initial release

See `CHANGELOG.md` for complete version history.

---

**Package Version**: 1.3.0  
**Release Date**: February 24, 2026  
**Package Type**: Source Distribution  

For the latest version, visit: [Your Repository URL]
