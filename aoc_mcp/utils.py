import os
import logging
import argparse
from dotenv import load_dotenv
import aiohttp
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('aoc_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://adventofcode.com"

def get_session_cookie():
    """Get the AOC session cookie from command line args or environment"""
    parser = argparse.ArgumentParser(description='Run the Advent of Code MCP server')
    parser.add_argument('--session-cookie', 
                       help='Advent of Code session cookie. If not provided, will check AOC_SESSION_COOKIE environment variable.')
    args = parser.parse_args()
    
    # First try command line argument
    if args.session_cookie:
        logger.info("Using session cookie from command line argument")
        return args.session_cookie
    
    # Then try environment variables
    load_dotenv()
    logger.info("Looking for .env file at: %s", os.path.abspath(".env"))
    
    env_cookie = os.getenv("AOC_SESSION_COOKIE")
    if env_cookie:
        logger.info("Using session cookie from environment variable")
        return env_cookie
    
    logger.error("No session cookie provided. Please provide it via --session-cookie argument or AOC_SESSION_COOKIE environment variable")
    raise ValueError("Session cookie not found")

async def fetch_aoc_content(url: str, session_cookie: str) -> str:
    """Fetch content from Advent of Code website using session cookie."""
    headers = {"Cookie": f"session={session_cookie}"}
    try:
        async with aiohttp.ClientSession() as session:
            logger.info(f"Fetching content from: {url}")
            logger.info(f"Using headers: {headers}")
            async with session.get(url, headers=headers) as response:
                response_text = await response.text()
                logger.info(f"Response status: {response.status}")
                logger.info(f"Response headers: {dict(response.headers)}")
                
                if response.status != 200:
                    error_msg = f"Failed to fetch AoC content: Status {response.status}"
                    logger.error(error_msg)
                    logger.error(f"Response text: {response_text}")
                    raise ValueError(error_msg)
                
                if "Puzzle inputs differ by user." in response_text:
                    error_msg = "Invalid session cookie. Please check your AOC_SESSION_COOKIE value."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                
                if "Please don't repeatedly request this endpoint before it unlocks!" in response_text:
                    error_msg = "Puzzle not yet available"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                
                logger.debug(f"Successfully fetched content from {url}")
                return response_text
    except Exception as e:
        error_msg = f"Error fetching content: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

def handle_interrupt(signum, frame):
    """Handle interrupt signal gracefully"""
    logger.info("Received interrupt signal. Shutting down gracefully...")
    raise SystemExit(0) 