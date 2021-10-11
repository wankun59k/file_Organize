import glob
import os
import asyncio
import aioshutil
import configparser
import shutil


config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
# ex.) F:\**\*.txt
path = config_ini['DEFAULT'].get('path')
# ex.) F:\texts
dst_path = config_ini['DEFAULT'].get('dst_path')
# ex.) F:\tmp
rm_path = config_ini['DEFAULT'].get('rm_path')

tasks = []
moved = []
duplicated = []
rm_cmd = ""

if not os.name == 'posix':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def move_glob(tgt_path):
    tgt_file = os.path.basename(tgt_path)
    if not tgt_file in moved:
        moved.append(tgt_file)
        await aioshutil.move(tgt_path, dst_path)
    else:
        idx = 0
        for itempath in duplicated:
            if os.path.basename(itempath) == tgt_file:
                idx += 1
        tgt_file = tgt_file + '_{:03}'.format(idx+1)
        duplicated.append(tgt_path)
        await aioshutil.move(tgt_path, os.path.join(rm_path, tgt_file))
        

async def main():
    for p in glob.glob(path, recursive=True):
        tasks.append(asyncio.create_task(move_glob(p)))
        #print("target file :{}".format(p))
    
    print("*"*5+"start program"+"*"*5)

    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    print("#" * 20)
    print("target file/path is {}".format(path))
    print("move for {}".format(dst_path))
    print("dupulicate are set at {}".format(rm_path))
    print("#" * 20)

    asyncio.run(main())

    print("{} files are duplicate.".format(len(duplicated)))
    for file in duplicated:
        print("> {} duplicate.".format(file))
    print("{} files are moved.".format(len(moved)))