# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-02-03

### Fixed
- Fixed Object Storage authentication by implementing proper AWS Signature Version 4 (SigV4) using boto3
- Object Storage tools now correctly authenticate with S3-compatible endpoints
- Replaced custom HTTP request signing with boto3's built-in S3 client

### Changed
- Added boto3 dependency for proper S3-compatible authentication
- Object Storage custom requests now require using specific tool methods instead of generic HTTP requests

## [1.0.0] - 2024-02-03

### Added
- Initial release of Zadara Storage MCP Server
- VPSA Storage Array support with 10 tools:
  - `vpsa_list_volumes` - List all volumes
  - `vpsa_create_volume` - Create new volumes
  - `vpsa_get_volume` - Get volume details
  - `vpsa_delete_volume` - Delete volumes
  - `vpsa_list_pools` - List storage pools
  - `vpsa_list_servers` - List connected servers
  - `vpsa_create_snapshot` - Create volume snapshots
  - `vpsa_list_snapshots` - List snapshots
  - `vpsa_get_performance` - Get performance metrics
  - `vpsa_list_controllers` - List controllers
- Object Storage support with 8 tools:
  - `object_list_buckets` - List all buckets
  - `object_create_bucket` - Create new buckets
  - `object_delete_bucket` - Delete buckets
  - `object_list_objects` - List objects in buckets
  - `object_get_bucket_policy` - Get bucket policy
  - `object_set_bucket_policy` - Set bucket policy
  - `object_get_bucket_versioning` - Get versioning status
  - `object_set_bucket_versioning` - Set versioning status
- Custom request tools for both APIs:
  - `vpsa_custom_request` - Make custom VPSA API calls
  - `object_custom_request` - Make custom Object Storage API calls
- Comprehensive documentation:
  - README.md with full documentation
  - QUICKSTART.md for fast setup
  - EXAMPLES.md with usage examples
  - CONTRIBUTING.md with contribution guidelines
- Setup automation:
  - setup.sh for easy installation
  - test.py for validation
- Configuration templates:
  - .env.example for environment variables
  - claude_desktop_config.json.example for Claude integration
- Security features:
  - .gitignore to protect sensitive data
  - Environment variable configuration
  - API key authentication support

### Security
- API keys stored in environment variables
- No credentials in code or version control
- HTTPS-only API communication

## Future Enhancements

### Planned for v1.1.0
- [ ] Add batch operation tools
- [ ] Support for VPSA drive management
- [ ] Object storage multipart upload support
- [ ] Enhanced error messages
- [ ] Retry logic for transient failures

### Planned for v1.2.0
- [ ] Volume attachment/detachment tools
- [ ] RAID group management
- [ ] Object storage lifecycle policies
- [ ] Storage analytics and reporting
- [ ] Performance optimization

### Planned for v2.0.0
- [ ] Async operations with progress tracking
- [ ] Webhook notifications
- [ ] Multi-VPSA support
- [ ] Advanced filtering and search
- [ ] Cost analysis tools

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Links

- [Zadara API Documentation](https://api-doc.zadarastorage.com/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub Repository](https://github.com/your-username/zadara-mcp-server)
