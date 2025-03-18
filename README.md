# Advent of Code MCP

A Mission Control Protocol (MCP) tool for fetching Advent of Code puzzle content and inputs. This tool can be integrated into any MCP-compatible environment (like Cursor) to fetch puzzle descriptions and inputs directly from Advent of Code.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/danielbrowning/aoc-mcp.git
cd aoc-mcp
```

2. Install uv (if not already installed):
```bash
pip install uv  # or brew install uv on macOS
```

3. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
uv pip sync
```

4. Create a `.env` file in the root directory with your Advent of Code session cookie:
```bash
AOC_SESSION_COOKIE=your_session_cookie_here
```

To get your session cookie:
1. Log in to [Advent of Code](https://adventofcode.com)
2. Open your browser's developer tools (F12)
3. Go to the Application/Storage tab
4. Find the 'session' cookie under Cookies
5. Copy the value into your `.env` file

## Using as an MCP Tool

This tool provides a single MCP function that can be used in MCP-compatible environments:

### get_puzzle

Fetches the puzzle description and input for a specific Advent of Code day.

Parameters:
- `year`: Year of the puzzle (2015-2024)
- `day`: Day of the puzzle (1-25)

Returns:
```json
{
    "year": 2023,
    "day": 1,
    "parts": ["Part 1 description", "Part 2 description"],
    "input": "puzzle input..."
}
```

### Example Usage in an MCP Environment

```python
result = await mcp.invoke("get_puzzle", {
    "year": 2023,
    "day": 1
})

# Access the puzzle parts and input
part1_description = result["parts"][0]
part2_description = result["parts"][1]
puzzle_input = result["input"]
```

## Running the Server

To run the MCP server (typically not needed for integration):
```bash
python -m aoc_mcp.server
```

The server will start in stdio mode for MCP communication.

## Notes

- Keep your session cookie private and never commit it to version control
- The tool validates year and day parameters to ensure they're within valid ranges (2015-2024 for year, 1-25 for day)
- If a puzzle is not yet available, the tool will return an appropriate error message
- Invalid session cookies will be detected and reported with clear error messages 