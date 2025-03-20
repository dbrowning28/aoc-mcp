from typing import Any
import signal
import sys
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from aoc_mcp.utils import get_session_cookie, fetch_aoc_content, handle_interrupt, logger, BASE_URL

# Initialize MCP server
mcp = FastMCP("advent-of-code")

# Get configuration
# Extract session cookie from command line arguments
session_cookie = None
for i, arg in enumerate(sys.argv):
    if arg == '--session-cookie' and i + 1 < len(sys.argv):
        session_cookie = sys.argv[i + 1]
        # Remove these arguments so they don't interfere with other argument parsing
        sys.argv.remove('--session-cookie')
        sys.argv.remove(session_cookie)
        break

AOC_SESSION_COOKIE = get_session_cookie(session_cookie)

@mcp.tool()
async def get_puzzle(year: int, day: int) -> dict[str, Any]:
    """Get puzzle description and input for a specific Advent of Code day.
    
    Args:
        year: Year of the puzzle (2015-2024)
        day: Day of the puzzle (1-25)
    """
    logger.info(f"Fetching puzzle for year {year}, day {day}")
    
    # Validate parameters
    if not (2015 <= year <= 2024):
        raise ValueError(f"Invalid year ({year}). Must be between 2015 and 2024.")
    
    if not (1 <= day <= 25):
        raise ValueError(f"Invalid day ({day}). Must be between 1 and 25.")

    try:
        url = f"{BASE_URL}/{year}/day/{day}"
        content = await fetch_aoc_content(url, AOC_SESSION_COOKIE)
        
        # Parse the puzzle description
        soup = BeautifulSoup(content, 'html.parser')
        puzzle_texts = soup.find_all('article', class_='day-desc')
        
        if not puzzle_texts:
            error_msg = f"No puzzle description found for year {year}, day {day}"
            logger.error(error_msg)
            logger.error(f"HTML content: {content[:500]}...")
            raise ValueError(error_msg)
        
        puzzle_parts = []
        for part in puzzle_texts:
            puzzle_parts.append(part.get_text())
        
        logger.info(f"Successfully parsed puzzle description for year {year}, day {day}")

        # Fetch puzzle input
        input_url = f"{url}/input"
        puzzle_input = await fetch_aoc_content(input_url, AOC_SESSION_COOKIE)
        
        logger.info(f"Successfully fetched puzzle input for year {year}, day {day}")

        return {
            "year": year,
            "day": day,
            "parts": puzzle_parts,
            "input": puzzle_input
        }
    except Exception as e:
        error_msg = f"Error processing puzzle for year {year}, day {day}: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)
    
    try:
        logger.info("Starting MCP server...")
        # Initialize and run the server
        mcp.run(transport='stdio')
    except (KeyboardInterrupt, SystemExit):
        logger.info("Server shutdown complete.")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise 