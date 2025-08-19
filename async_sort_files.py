import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(file_path: AsyncPath, output_folder: AsyncPath):
    """Copy file into subfolder by extension"""
    try:
        ext = file_path.suffix.lower().lstrip(".") or "no_extension"
        target_dir = output_folder / ext
        await target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / file_path.name
        await copyfile(file_path, target_file)
        logging.info(f"Copied: {file_path} -> {target_file}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")


async def read_folder(source_folder: AsyncPath, output_folder: AsyncPath):
    """Read all files in folder and copy them"""
    try:
        async for path in source_folder.glob("**/*"):
            if await path.is_file():
                await copy_file(path, output_folder)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Async file sorting by extensions")
    parser.add_argument("source", help="Path to source folder")
    parser.add_argument("output", help="Path to output folder")
    args = parser.parse_args()

    source_folder = AsyncPath(args.source)
    output_folder = AsyncPath(args.output)

    if not await source_folder.exists():
        logging.error(f"Source folder {source_folder} does not exist")
        return

    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    asyncio.run(main())
