import os
import logging
import json
import time


# 设置参数
SVN_ROOT = 'D:/"Program Files"/"VisualSVN Server"' # SVN根目录
REPO_ROOT = 'D:/Repositories' # 仓库根目录
BACKUP_ROOT = 'Z:/VisualSVN_bak' # 备份根目录
BACKUP_FOLDER = 'Full_' + time.strftime('%Y%m%d_%H%M%S') # 备份文件夹
BACKUP_DIR = os.path.join(BACKUP_ROOT, BACKUP_FOLDER) # 备份目录
# 新建目录
os.mkdir(BACKUP_DIR)
# 设置日志
logging.basicConfig(filename=os.path.join(BACKUP_DIR, 'Log %s.log') % time.strftime('%Y-%m-%d %H_%M_%S'), filemode='w',
                    level=logging.INFO, format='[%(levelname)s] %(asctime)s %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H_%M_%S')
try:
    # 从json获取库信息
    with open(os.path.join(BACKUP_ROOT, 'version.json'), 'r') as f:
        old_versions = json.load(f)
    # 对每个库分别备份
    for repo in old_versions.keys():
        logging.info('[*] 备份 %s 库.' % repo)
        # 全量备份当前库,并判断当前库的备份是否成功
        if os.system('%s/bin/svnadmin dump %s/%s>%s/%s.dmp' % (SVN_ROOT, REPO_ROOT, repo, BACKUP_DIR, repo)) == 0:
            logging.info('[*] %s 库备份成功' % repo)
        else:
            logging.error('[*] %s 库备份失败' % repo)
except Exception as e:
    logging.error('[*] ERROR: %s' % str(e))