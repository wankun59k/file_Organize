import pathlib
import glob
import os
import asyncio
import aioshutil

path = 'F:/**/(成年コミック)*.*'
dst_path = pathlib.Path('F:\HEN_MANGA\SEIKOMI')
rm_path = pathlib.Path('F:\remove')


tasks = []

async def move_glob(tgt_path):
    if not os.path.exists(os.path.join(dst_path, os.path.basename(tgt_path))):
        await aioshutil.move(tgt_path, dst_path)
    else:
        await aioshutil.move(tgt_path, rm_path)
        await aioshutil.rmtree(rm_path)

async def main():
    for p in glob.glob(path, recursive=True):
        tasks.append(asyncio.create_task(move_glob(p)))
    
    print('start program')

    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())