# Project Structure

This document explains the organization of the Zadara Storage MCP Server project.

## Directory Layout

```
zadara-mcp-server/
├── .github/                      # GitHub-specific files
│   ├── workflows/
│   │   └── ci.yml               # CI/CD pipeline configuration
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md        # Bug report template
│   │   └── feature_request.md   # Feature request template
│   └── PULL_REQUEST_TEMPLATE.md # PR template
├── server.py                     # Main MCP server implementation
├── test.py                       # Test and validation script
├── setup.sh                      # Automated setup script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXAMPLES.md                   # Usage examples
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
├── SECURITY.md                   # Security policy
├── PROJECT_STRUCTURE.md          # This file
└── claude_desktop_config.json.example  # Claude Desktop config template
```

## File Descriptions

### Core Files

#### `server.py`
The main MCP server implementation containing:
- `ZadaraClient` class for API communication
- Tool definitions for both VPSA and Object Storage
- Request handlers for all supported operations
- Error handling and logging
- MCP protocol implementation

**Key Components:**
- Connection management
- Authentication handling
- JSON request/response processing
- Tool registration and execution

#### `requirements.txt`
Python package dependencies:
- `mcp>=0.9.0` - Model Context Protocol SDK
- `httpx>=0.24.0` - Async HTTP client

#### `test.py`
Validation and testing script that checks:
- Python environment
- Required dependencies
- Environment configuration
- Server module import
- Basic functionality

### Configuration Files

#### `.env.example`
Template for environment variables:
```bash
ZADARA_VPSA_URL=           # VPSA endpoint URL
ZADARA_VPSA_API_KEY=       # VPSA API key
ZADARA_OBJECT_STORAGE_URL= # Object Storage endpoint
ZADARA_OBJECT_ACCESS_KEY=  # S3 access key
ZADARA_OBJECT_SECRET_KEY=  # S3 secret key
```

#### `claude_desktop_config.json.example`
Template for Claude Desktop integration:
```json
{
  "mcpServers": {
    "zadara-storage": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": { ... }
    }
  }
}
```

#### `.gitignore`
Prevents committing:
- Environment files (`.env`)
- Python cache (`__pycache__/`)
- Virtual environments
- IDE configurations
- Secrets and keys
- Log files

### Documentation Files

#### `README.md`
Main project documentation covering:
- Feature overview
- Installation instructions
- Configuration guide
- Tool documentation
- Usage examples
- Troubleshooting

#### `QUICKSTART.md`
Fast-track setup guide:
- Prerequisites
- 5-step installation
- Common issues
- Quick verification

#### `EXAMPLES.md`
Comprehensive usage examples:
- VPSA operations
- Object Storage operations
- Natural language queries
- Complex workflows
- Error handling

#### `CONTRIBUTING.md`
Guidelines for contributors:
- Development setup
- Code style
- Adding new tools
- Testing requirements
- PR process

#### `CHANGELOG.md`
Version history tracking:
- Release notes
- Feature additions
- Bug fixes
- Breaking changes
- Future roadmap

#### `SECURITY.md`
Security guidelines:
- Reporting vulnerabilities
- Best practices
- Security features
- Incident response
- Compliance notes

### Scripts

#### `setup.sh`
Automated setup script that:
- Checks Python installation
- Installs dependencies
- Creates `.env` from template
- Validates configuration
- Provides next steps

### GitHub Integration

#### `.github/workflows/ci.yml`
CI/CD pipeline that runs on push/PR:
- **Lint Job**: Code quality checks (Black, Flake8, Pylint)
- **Security Job**: Vulnerability scanning (Safety, Bandit)
- **Test Job**: Multi-version Python testing
- **Docs Job**: Documentation validation
- **Version Job**: Changelog verification

#### `.github/ISSUE_TEMPLATE/bug_report.md`
Structured bug report form requesting:
- Bug description
- Reproduction steps
- Environment details
- Error messages
- Screenshots

#### `.github/ISSUE_TEMPLATE/feature_request.md`
Feature request form asking for:
- Feature description
- Problem it solves
- Proposed solution
- Use cases
- Priority level

#### `.github/PULL_REQUEST_TEMPLATE.md`
PR template with checklists for:
- Change description
- Testing performed
- Documentation updates
- Security review
- Breaking changes

## Development Workflow

### 1. Local Development
```bash
git clone <repository>
cd zadara-mcp-server
./setup.sh
python test.py
```

### 2. Making Changes
```bash
git checkout -b feature/my-feature
# Make changes
python test.py
git commit -m "feat: description"
git push origin feature/my-feature
```

### 3. Pull Request
- Create PR using template
- CI pipeline runs automatically
- Address review feedback
- Merge when approved

### 4. Release
- Update CHANGELOG.md
- Tag version
- GitHub Actions creates release notes

## Code Organization

### `server.py` Structure

```python
# Imports
import asyncio, json, os, httpx
from mcp.server import Server
from mcp.types import *

# Configuration
VPSA_BASE_URL = os.getenv(...)
VPSA_API_KEY = os.getenv(...)

# Client Class
class ZadaraClient:
    def __init__(self): ...
    async def vpsa_request(self, ...): ...
    async def object_storage_request(self, ...): ...

# Server Instance
app = Server("zadara-storage-mcp")
client = ZadaraClient()

# Tool Handlers
@app.list_tools()
async def list_tools(): ...

@app.call_tool()
async def call_tool(name, arguments): ...

# Main Entry Point
async def main(): ...
if __name__ == "__main__":
    asyncio.run(main())
```

## Extension Points

### Adding New Tools

1. **Define in `list_tools()`:**
```python
Tool(
    name="new_tool_name",
    description="What it does",
    inputSchema={ ... }
)
```

2. **Implement in `call_tool()`:**
```python
elif name == "new_tool_name":
    result = await client.vpsa_request(...)
    return [TextContent(type="text", text=json.dumps(result))]
```

3. **Document:**
- Add to README.md
- Add examples to EXAMPLES.md
- Update CHANGELOG.md

### Adding New APIs

1. Add configuration variables
2. Extend `ZadaraClient` class
3. Add authentication logic
4. Create tool definitions
5. Update documentation

## Dependencies

### Runtime Dependencies
- Python 3.8+
- `mcp` - MCP protocol implementation
- `httpx` - HTTP client library

### Development Dependencies
- `black` - Code formatting
- `flake8` - Linting
- `pylint` - Code analysis
- `safety` - Security scanning
- `bandit` - Security linting

## Testing Strategy

### Unit Testing
- Import validation
- Configuration checking
- Environment verification

### Integration Testing
- API connectivity
- Authentication
- Tool execution

### Manual Testing
- Claude Desktop integration
- Real API calls
- Error scenarios

## Deployment

### Claude Desktop
1. Install server locally
2. Configure in `claude_desktop_config.json`
3. Restart Claude Desktop
4. Verify connection

### Standalone
1. Run `python server.py`
2. Server listens on stdio
3. MCP client connects
4. Tools available via protocol

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review security advisories
- Update documentation
- Test with latest Zadara APIs
- Rotate test credentials

### Version Management
- Follow semantic versioning
- Update CHANGELOG.md
- Tag releases
- Create GitHub releases

## Support

### Getting Help
- Check documentation
- Review examples
- Search issues
- Create new issue

### Contributing
- Follow CONTRIBUTING.md
- Use issue templates
- Write clear commits
- Add tests
- Update docs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
