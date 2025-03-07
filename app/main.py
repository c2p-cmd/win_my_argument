from argparse import ArgumentParser
from debate.service import make_debate
import asyncio
from dotenv import load_dotenv

parser = ArgumentParser(
    description="Debate on a topic",
)
parser.add_argument(
    "--query",
    type=str,
    help="The topic to debate",
)
args = parser.parse_args()

if __name__ == "__main__":
    load_dotenv('../.env')
    result = asyncio.run(
        make_debate(query=args.query),
        debug=True,
    )
    print(result)
