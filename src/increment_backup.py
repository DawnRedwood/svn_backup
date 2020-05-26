import os
import logging
import json
import time


# 设置参数
SVN_ROOT = 'D:/"Program Files"/"VisualSVN Server"' # SVN根目录
REPO_ROOT = 'D:/Repositories' # 仓库根目录
BACKUP_ROOT = 'Z:/VisualSVN_bak' # 备份根目录
BACKUP_FOLDER = 'Increment_' + time.strftime('%Y%m%d_%H%M%S') # 备份文件夹
BACKUP_DIR = os.path.join(BACKUP_ROOT, BACKUP_FOLDER) # 备份目录
# 新建目录
os.mkdir(BACKUP_DIR)
# 设置日志
logging.basicConfig(filename=os.path.join(BACKUP_DIR, 'Log %s.log') % time.strftime('%Y-%m-%d %H_%M_%S'), filemode='w',
                    level=logging.INFO, format='[%(levelname)s] %(asctime)s %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H_%M_%S')
try:
    # 从json获取旧版本
    with open(os.path.join(BACKUP_ROOT, 'version.json'), 'r') as f:
        old_versions = json.load(f)
    new_versions = {}
    # 对每个库分别备份
    for repo, old_version in old_versions.items():
        logging.info('[*] 备份 %s 库.' % repo)
        # 获取当前库的新版本
        if os.system('%s/bin/svnlook youngest %s/%s>%s/version.txt' % (SVN_ROOT, REPO_ROOT, repo, BACKUP_ROOT)) == 0:
            with open(os.path.join(BACKUP_ROOT, 'version.txt'), 'r') as f:
                new_version = int(f.readline())
            new_versions[repo] = new_version
        # 判断旧版本是否小于最新版本
        if old_version < new_version:
            logging.info('[*] 上次增量备份版本：%s < 当前最新版本：%s, 准备开始增量备份.' % (old_version, new_version))
            # 增量备份当前库,并判断当前库的备份是否成功
            if os.system('%s/bin/svnadmin dump %s/%s -r %s:%s --incremental>%s/%s.dmp'
                % (SVN_ROOT, REPO_ROOT, repo, old_version + 1, new_version, BACKUP_DIR, repo)) == 0:
                logging.info('[*] %s 库备份成功' % repo)
            else:
                logging.error('[*] %s 库备份失败' % repo)
        else:
            logging.error('[*] 上次增量备份版本：%s >= 当前最新版本：%s, 故不进行增量备份.' % (old_version, new_version))
    # 将新版本写入json
    with open(os.path.join(BACKUP_ROOT, 'version.json'), 'w') as f:
        json.dump(new_versions, f)
except Exception as e:
    logging.error('[*] ERROR: %s' % str(e))