# Contributing to Zadara Storage MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/zadara-mcp-server.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit and push
7. Create a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/zadara-mcp-server.git
cd zadara-mcp-server

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run tests
python test.py
```

## Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

## Adding New Tools

To add a new tool to the MCP server:

1. **Define the tool** in the `list_tools()` function:
```python
Tool(
    name="vpsa_new_feature",
    description="Clear description of what this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    }
)
```

2. **Implement the handler** in the `call_tool()` function:
```python
elif name == "vpsa_new_feature":
    param1 = arguments["param1"]
    result = await client.vpsa_request("GET", f"endpoint/{param1}.json")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]
```

3. **Update documentation**:
   - Add tool description to README.md
   - Add usage examples to EXAMPLES.md
   - Update CHANGELOG.md

4. **Test the tool**:
   - Test manually with Claude Desktop
   - Add test cases if applicable
   - Verify error handling

## Testing

- Test all new features with actual Zadara API
- Verify error handling for edge cases
- Test with missing/invalid credentials
- Check for proper error messages

## Documentation

- Update README.md for new features
- Add examples to EXAMPLES.md
- Update QUICKSTART.md if setup changes
- Keep documentation clear and concise

## Pull Request Process

1. Update documentation for any new features
2. Ensure your code follows the style guide
3. Test your changes thoroughly
4. Update CHANGELOG.md with your changes
5. Create a clear PR description explaining:
   - What changes you made
   - Why you made them
   - How to test them

## Commit Messages

Use clear, descriptive commit messages:

- `feat: Add support for volume cloning`
- `fix: Correct authentication header format`
- `docs: Update installation instructions`
- `refactor: Simplify error handling logic`
- `test: Add tests for bucket operations`

## Issue Reporting

When reporting issues, include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages and logs
- Zadara API version if relevant

## Feature Requests

For feature requests, explain:

- What feature you'd like
- Why it would be useful
- How you envision it working
- Any API endpoints involved

## Security

- Never commit API keys or credentials
- Report security vulnerabilities privately
- Don't include sensitive data in issues/PRs
- Use environment variables for secrets

## Code Review

All contributions will be reviewed for:

- Code quality and style
- Documentation completeness
- Test coverage
- Security considerations
- API compatibility

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

Thank you for contributing! 🎉
