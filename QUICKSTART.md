# Quick Start Guide

Get up and running with the Zadara Storage MCP Server in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Zadara Storage account with API access
- Claude Desktop (for MCP integration)

## Step 1: Installation

```bash
# Clone or download the repository
cd zadara-mcp-server

# Run the setup script
./setup.sh
```

Or manually:

```bash
pip install -r requirements.txt
```

## Step 2: Configuration

### Get Your API Credentials

#### VPSA Storage Array
1. Log into your VPSA web interface
2. Go to Settings → API Keys
3. Generate a new API key or copy existing one
4. Note your VPSA URL (e.g., `https://vsa-00000123.zadaravpsa.com`)

#### Object Storage
1. Log into your Object Storage console
2. Go to Access Keys or IAM settings
3. Create or retrieve Access Key and Secret Key
4. Note your Object Storage URL

### Configure Environment

Edit the `.env` file:

```bash
# VPSA Storage Array
ZADARA_VPSA_URL=https://vsa-00000123.zadaravpsa.com
ZADARA_VPSA_API_KEY=your-actual-vpsa-api-key

# Object Storage
ZADARA_OBJECT_STORAGE_URL=https://bucket.zadarastorage.com
ZADARA_OBJECT_ACCESS_KEY=your-actual-access-key
ZADARA_OBJECT_SECRET_KEY=your-actual-secret-key
```

## Step 3: Test the Server

```bash
# Run the test script
python test.py

# Or test manually
python server.py
```

If everything is configured correctly, the server will start without errors.

## Step 4: Configure Claude Desktop

1. Locate your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Edit the file and add:

```json
{
  "mcpServers": {
    "zadara-storage": {
      "command": "python3",
      "args": ["/full/path/to/zadara-mcp-server/server.py"],
      "env": {
        "ZADARA_VPSA_URL": "https://vsa-00000123.zadaravpsa.com",
        "ZADARA_VPSA_API_KEY": "your-actual-vpsa-api-key",
        "ZADARA_OBJECT_STORAGE_URL": "https://bucket.zadarastorage.com",
        "ZADARA_OBJECT_ACCESS_KEY": "your-actual-access-key",
        "ZADARA_OBJECT_SECRET_KEY": "your-actual-secret-key"
      }
    }
  }
}
```

3. **Important**: Replace `/full/path/to/zadara-mcp-server/server.py` with the actual absolute path

4. Restart Claude Desktop

## Step 5: Verify Integration

Open Claude Desktop and try these commands:

```
"List all volumes in my VPSA storage"
"Show me all buckets in my object storage"
"What storage pools are available?"
"Create a bucket called 'test-bucket'"
"Generate a simple PDF and upload it to 'test-bucket'"
```

If Claude responds with data from your Zadara system, you're all set!

**New in v1.1.0:** You can now upload, download, and delete files!
```
"Upload a document to my object storage"
"Download the report.pdf from bucket 'documents'"
"Delete old files from bucket 'archives'"
```

## Common Issues

### "Command not found: python3"
- Use `python` instead of `python3` in the config
- Or install Python 3

### "Module not found: mcp"
- Run: `pip install -r requirements.txt`
- Ensure you're using the same Python that Claude Desktop uses

### "Authentication failed"
- Double-check your API keys
- Verify URLs don't have trailing slashes
- Test API access with curl:
  ```bash
  curl -H "X-Access-Key: YOUR_KEY" https://your-vpsa-url.com/api/volumes.json
  ```

### "Server not responding"
- Check Claude Desktop logs
- Ensure the server.py path is absolute (not relative)
- Try running `python server.py` manually to see errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all available tools and their parameters
- Check the Zadara API documentation for advanced features

## Getting Help

- Check server logs in Claude Desktop
- Run `python test.py` to diagnose issues
- Review the [Zadara API documentation](https://api-doc.zadarastorage.com/)
- Verify MCP protocol compatibility

## Security Reminders

- Never commit `.env` file to version control
- Regularly rotate your API keys
- Use read-only API keys when possible
- Monitor API usage and access logs
