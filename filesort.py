import glob
import os
import asyncio
import aioshutil
import configparser
import shutil


config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

path = config_ini['DEFAULT'].get('path')
dst_path = config_ini['DEFAULT'].get('dst_path')
rm_path = config_ini['DEFAULT'].get('rm_path')

tasks = []
moved = []
duplicated = []
async def move_glob(tgt_path):
    checkpath = os.path.join(dst_path, os.path.basename(tgt_path))
    if not checkpath in moved:
        moved.append(checkpath)
        await aioshutil.move(tgt_path, dst_path)
    else:
        if checkpath in duplicated:
            shutil.remove(tgt_path)
        duplicated.append(checkpath)
        await aioshutil.move(tgt_path, rm_path)

async def main():
    for p in glob.glob(path, recursive=True):
        tasks.append(asyncio.create_task(move_glob(p)))
        #print(p)
    
    print('start program')

    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
    print("{} files are duplicate.".format(len(duplicated)))
    for file in duplicated:
        print("> {} duplicate.".format(file))
    for file in moved:
        print("> {} moved.".format(file))