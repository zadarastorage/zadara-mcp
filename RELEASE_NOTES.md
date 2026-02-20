# Release Notes - Version 1.1.0

**Release Date:** February 20, 2026

## 🎉 What's New

### Object Storage File Management

Version 1.1.0 introduces full file management capabilities for Zadara Object Storage, allowing you to upload, download, and delete files directly through Claude!

### New Features

#### 1. **Object Upload** (`object_upload`)
Upload any type of file to your object storage buckets:
- Supports all file types (PDFs, images, JSON, text, binary files)
- Base64 encoding for reliable data transfer
- Custom content-type support
- Secure AWS Signature V4 authentication

**Example Usage:**
```
"Generate a PDF report and upload it to bucket 'reports'"
"Upload this image to 'media-storage' as 'photos/vacation.jpg'"
```

#### 2. **Object Download** (`object_download`)
Download files from your object storage:
- Returns base64-encoded content
- Includes full metadata (size, content type, headers)
- Secure AWS Signature V4 authentication

**Example Usage:**
```
"Download 'report.pdf' from bucket 'documents'"
"Get the latest backup from 'archives' bucket"
```

#### 3. **Object Delete** (`object_delete`)
Safely delete objects from storage:
- Permanent deletion with confirmation
- Secure AWS Signature V4 authentication

**Example Usage:**
```
"Delete 'old-file.dat' from bucket 'temporary'"
"Remove test files from 'development' bucket"
```

### Enhanced Security

#### AWS Signature Version 4 Implementation
All object operations now use industry-standard AWS Signature V4 authentication:
- **HMAC-SHA256 signing** - Cryptographically secure request signing
- **Payload hashing** - SHA-256 hash of request body for integrity
- **Canonical headers** - Standardized header format with host, date, and content hash
- **Credential scoping** - Proper date, region, and service scoping
- **Compatible** - Works with any S3-compatible storage system

This implementation matches the security standards used by AWS S3 and other major cloud storage providers.

## 🔧 Technical Improvements

### Authentication Architecture
- Added `_sign_aws_request()` method to `ZadaraClient` class
- Implements full AWS Signature V4 signing algorithm
- Proper HMAC-SHA256 key derivation
- Canonical request construction with sorted headers
- String-to-sign generation with credential scope

### Error Handling
- Enhanced error messages for authentication failures
- Better handling of network timeouts
- Improved status code reporting

### Code Quality
- Added base64, hashlib, hmac, and datetime imports
- Enhanced type hints for better IDE support
- Improved method documentation

## 📚 Documentation Updates

### Updated Files
- **README.md** - Added new tools documentation with security notes
- **EXAMPLES.md** - Comprehensive examples for upload/download/delete operations
- **QUICKSTART.md** - Added verification examples for new features
- **CHANGELOG.md** - Complete version history
- **VERSION** - Updated to 1.1.0

### New Documentation
- **RELEASE_NOTES.md** - This file
- Detailed workflow examples for file management
- Security best practices for object operations

## 🚀 Getting Started

### Upgrading from v1.0.0

1. **Download the updated server.py**
2. **Replace your current server file**
3. **Restart Claude Desktop**
4. **Test the new features:**
   ```
   "Create a bucket called 'test'"
   "Upload a file to 'test' bucket"
   "List objects in 'test' bucket"
   ```

### New Installation

Follow the [QUICKSTART.md](QUICKSTART.md) guide for complete setup instructions.

## 💡 Usage Examples

### Complete Workflow Example

```
User: "Create a bucket called 'company-reports'"
Claude: ✓ Bucket created successfully

User: "Generate a quarterly report PDF and upload it to 'company-reports'"
Claude: ✓ PDF generated (2,345 bytes)
        ✓ Uploaded as 'quarterly_report.pdf'

User: "Download the report from 'company-reports'"
Claude: ✓ Downloaded 'quarterly_report.pdf' (2,345 bytes)
        [Returns base64-encoded content]

User: "Delete old reports from 'company-reports'"
Claude: Which specific files should I delete?
```

### Practical Use Cases

1. **Document Management**
   - Upload reports, invoices, and contracts
   - Download files for review or editing
   - Clean up old documents

2. **Backup and Archive**
   - Upload backup files with timestamps
   - Download backups for restoration
   - Delete old backups based on retention policies

3. **Media Storage**
   - Upload images, videos, and audio files
   - Download media for processing
   - Manage media library

4. **Data Processing**
   - Upload datasets for analysis
   - Download processed results
   - Clean up intermediate files

## 🔒 Security Considerations

### Best Practices
- Always use HTTPS endpoints
- Rotate access keys regularly
- Use bucket policies to restrict access
- Enable versioning for important data
- Monitor access logs

### Authentication Flow
1. Request is constructed with headers and payload
2. Payload is hashed with SHA-256
3. Canonical request is created with sorted headers
4. Signing key is derived using HMAC-SHA256
5. Request is signed with the derived key
6. Authorization header is added to request

## 🐛 Bug Fixes

- Fixed 403 Forbidden errors on object operations
- Improved authentication header construction
- Enhanced error messages for debugging

## ⚡ Performance

- Efficient base64 encoding/decoding
- Optimized request signing
- Connection reuse for multiple operations
- Proper timeout handling (60s for uploads/downloads)

## 🔮 What's Next

### Planned for v1.2.0
- Enhanced object listing with AWS Signature V4
- Multi-part upload for large files (>5GB)
- Object metadata management
- Batch operations for multiple files
- Progress tracking for large transfers
- Retry logic with exponential backoff
- Connection pooling

### Future Enhancements
- Pre-signed URL generation
- Server-side encryption support
- Access control list (ACL) management
- Cross-region replication
- Lifecycle policy management

## 📞 Support

### Getting Help
- Check [README.md](README.md) for detailed documentation
- Review [EXAMPLES.md](EXAMPLES.md) for usage examples
- See [CHANGELOG.md](CHANGELOG.md) for version history
- Visit [Zadara API Documentation](https://api-doc.zadarastorage.com/)

### Reporting Issues
- Check server logs in Claude Desktop
- Run `python test.py` for diagnostics
- Review error messages carefully
- Test with minimal examples first

## 🙏 Acknowledgments

This release implements industry-standard AWS Signature V4 authentication, ensuring compatibility with S3-compatible storage systems and providing enterprise-grade security for object operations.

---

**Version:** 1.1.0  
**Release Date:** February 20, 2026  
**Previous Version:** 1.0.0 (February 3, 2026)
