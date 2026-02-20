# Changelog

All notable changes to the Zadara Storage MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-20

### Added
- **Object Upload Support**: New `object_upload` tool for uploading files to Object Storage
  - Accepts base64-encoded file content
  - Supports custom content types (PDF, images, JSON, etc.)
  - Uses AWS Signature V4 authentication for secure uploads
- **Object Download Support**: New `object_download` tool for downloading files from Object Storage
  - Returns base64-encoded file content
  - Includes metadata (size, content type, headers)
  - Uses AWS Signature V4 authentication for secure downloads
- **Object Delete Support**: New `object_delete` tool for deleting objects from Object Storage
  - Permanently removes objects from buckets
  - Uses AWS Signature V4 authentication for secure deletions
- **AWS Signature V4 Authentication**: Implemented proper AWS Signature Version 4 signing
  - HMAC-SHA256 request signing
  - Canonical headers with payload hashing
  - Proper credential scoping with date, region, and service
  - Compatible with S3-compatible object storage systems

### Changed
- Enhanced `ZadaraClient` class with new authentication method `_sign_aws_request()`
- Updated object storage methods to use AWS Signature V4 instead of simple authorization
- Improved error handling for object operations

### Documentation
- Updated README.md with new object management tools
- Added comprehensive examples for upload/download/delete in EXAMPLES.md
- Added workflow examples showing complete file management scenarios
- Created CHANGELOG.md to track version history

### Security
- Implemented industry-standard AWS Signature V4 authentication
- Proper payload hashing for all object operations
- Enhanced security for file uploads and downloads

## [1.0.0] - 2026-02-03

### Added
- Initial release of Zadara Storage MCP Server
- VPSA Storage Array support:
  - Volume management (list, create, get, delete)
  - Storage pool listing
  - Server connection management
  - Snapshot operations (create, list)
  - Performance metrics retrieval
  - Controller status
  - Custom API requests
- Object Storage support:
  - Bucket management (list, create, delete)
  - Object listing with filtering
  - Bucket policy management (get, set)
  - Bucket versioning control (get, set)
  - Custom API requests
- Complete documentation:
  - Comprehensive README.md
  - Quick start guide (QUICKSTART.md)
  - Usage examples (EXAMPLES.md)
- Development tools:
  - Automated setup script (setup.sh)
  - Testing script (test.py)
- GitHub integration:
  - CI/CD pipeline configuration
  - Issue templates
  - Pull request template
- Security:
  - Environment variable configuration
  - .gitignore for sensitive data
  - Security policy (SECURITY.md)
- Licensing:
  - MIT License

### Security
- Basic AWS-style authentication for Object Storage
- API key authentication for VPSA Storage Array
- Environment variable based credential management

## [Unreleased]

### Planned
- Enhanced object listing with AWS Signature V4 authentication
- Bucket policy operations with proper authentication
- Multi-part upload support for large files
- Object metadata management
- Batch operations for multiple objects
- Progress tracking for large uploads/downloads
- Retry logic for failed operations
- Connection pooling for improved performance

---

## Version History Summary

- **v1.1.0** (2026-02-20): Added object upload/download/delete with AWS Signature V4
- **v1.0.0** (2026-02-03): Initial release with VPSA and Object Storage support
