# Zadara Storage MCP Server v1.3.0
# Release Manifest

## Release Information
Version: 1.3.0
Release Date: 2026-02-24
Package Type: Source Distribution
Build Type: Production

## Package Integrity
Checksum File: CHECKSUMS.txt
Checksum Algorithm: SHA256

## System Requirements
Python Version: >= 3.8
Operating Systems: Windows, macOS, Linux
Required Disk Space: ~100 KB
Network Access: Required for Zadara Storage APIs

## Dependencies
httpx >= 0.24.0
mcp >= 0.1.0

See requirements.txt for complete list.

## Core Components

### Main Server
- server.py (42.9 KB) - Main MCP server implementation

### Installation
- install.sh - Automated installation script (Unix/Mac/Linux)
- setup.sh - Quick setup script
- requirements.txt - Python dependencies

### Configuration
- .env.example - Environment configuration template
- claude_desktop_config.json.example - Claude Desktop integration template

### Documentation (9 files)
- README.md - Complete documentation
- PACKAGE_README.md - Package-specific readme
- QUICKSTART.md - Quick start guide
- EXAMPLES.md - Usage examples
- CHANGELOG.md - Version history
- UPDATE_SUMMARY_v1.3.0.md - Release summary
- QUICK_REFERENCE_BUCKET_SIZES.md - Feature quick reference
- PROJECT_STRUCTURE.md - Project organization
- CONTRIBUTING.md - Contribution guidelines
- SECURITY.md - Security best practices
- RELEASE_NOTES.md - Release information
- LICENSE - Software license

### Test Suite
- test.py - Basic functionality tests
- test_bucket_sizes.py - Bucket size calculation tests

## What's New in v1.3.0

### New Features
1. Bucket Size Calculation Tool
   - Tool: object_get_bucket_sizes
   - Calculates total size for all buckets or specific buckets
   - Automatic pagination for large buckets (>1000 objects)
   - Human-readable size formatting (bytes, KB, MB, GB)
   - Per-bucket and summary statistics
   - Graceful error handling

### Technical Improvements
- Enhanced XML parsing for S3 ListObjectsV2 responses
- Pagination support with continuation tokens
- Per-bucket error isolation
- Comprehensive size formatting utilities

### Documentation Updates
- Added UPDATE_SUMMARY_v1.3.0.md
- Added QUICK_REFERENCE_BUCKET_SIZES.md
- Updated README.md with new tool documentation
- Updated EXAMPLES.md with bucket size examples
- Updated CHANGELOG.md

## Features Overview

### VPSA Storage Array (11 tools)
- Volume Management: Create, list, get, delete volumes
- Pool Management: List storage pools
- Server Management: List connected servers
- Snapshot Management: Create and list snapshots
- Performance Monitoring: Get performance metrics
- Controller Status: List controllers
- Custom API: Make custom VPSA API requests

### Object Storage (13 tools)
- Bucket Management: List, create, delete buckets
- Bucket Size Calculation: Calculate storage usage (NEW v1.3.0)
- Object Management: Upload, download, delete, list objects
- Policy Management: Get and set bucket policies
- Versioning: Configure bucket versioning
- Custom API: Make custom Object Storage API requests

## Security Features
- AWS Signature V4 authentication for Object Storage
- API key authentication for VPSA
- Environment-based credential management
- No hardcoded credentials
- Secure credential storage in .env file

## Installation Methods

### Automated Installation
```bash
chmod +x install.sh
./install.sh
```

### Manual Installation
```bash
pip3 install -r requirements.txt
cp .env.example .env
# Edit .env with credentials
python3 server.py
```

## Testing
```bash
# Basic tests
python3 test.py

# Bucket size tests
python3 test_bucket_sizes.py
```

## Integration Points
- Claude Desktop (via MCP protocol)
- Zadara VPSA Storage Array API
- Zadara Object Storage (S3-compatible API)

## Support Channels
- Documentation: See README.md
- Issues: See CONTRIBUTING.md
- Security: See SECURITY.md

## Verification
To verify package integrity:
```bash
sha256sum -c CHECKSUMS.txt
```

## Upgrade Path
From v1.2.0 to v1.3.0:
- Backup current installation
- Replace server.py
- Restart MCP server
- No configuration changes required
- Backward compatible

## Known Limitations
- Large bucket calculations may take time (normal for >10k objects)
- Requires network access to Zadara Storage
- Versioned bucket sizes count current versions only

## Future Roadmap
- Bucket size caching
- Parallel bucket processing
- Lifecycle policy-aware calculations
- Version history size calculations

## License
See LICENSE file

## Credits
Developer: Marco
Release Manager: Marco
Build Date: 2026-02-24
Build Environment: Production

## Package Formats
- Source Distribution (this package)
- Git Repository (with version control)

## Compatibility
- Backward Compatible: Yes (with v1.2.0, v1.1.0, v1.0.0)
- Breaking Changes: None
- API Version: MCP 1.0
- Protocol Version: stdio

---
Generated: 2026-02-24
Package Hash: See CHECKSUMS.txt
