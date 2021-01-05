#!/usr/bin/env python3
# 项目：标准库
# 模块：版本管理程序
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-05-20 15:32
# 修订：2016-9-6 将其迁移至orange 库，并移除对stdlib 的依赖
# 修订：2017-2-10 pyver 增加 -y 功能，与远程服务器同步

import os
import sys
import setuptools
from orange import Path, R, sh
from orange.utils import arg
from .version import Ver
from .setup import get_pkg_ver


class VersionMgr:
    branch = None   # 当前git分支
    up_to_date = True  # 与版本库是否同步
    untracted_files = []  # 未跟踪文件
    not_staged = []       # 已更新文件
    to_be_commited = []   # 待提交文件
    is_clean = False      # 工作区是否干净
    ver = None            # 当前程序版本
    repository = True     # 是否纳入git版本管理
    file_type = None

    def proc_git(self):
        from re import compile
        patterns = {
            compile(r'(On branch|位于分支) (?P<branch>\w+)'):
            lambda branch: setattr(self, 'branch', branch),
            compile(r"(Your branch is up-to-date with|您的分支与上游分支) '.*?'."):
            lambda: setattr(self, 'up_to_date', True),
            compile(r"(Changes not staged for commit:|尚未暂存以备提交的变更：)"):
            lambda: setattr(self, 'file_type', 'not_staged'),
            compile(r"(Untracked files:|未跟踪的文件:)"):
            lambda: setattr(self, 'file_type', 'untracted_files'),
            compile(r"(Changes to be committed:|要提交的变更：)"):
            lambda: setattr(self, 'file_type', 'to_be_commited'),
            compile(r"\t(.*?:\s*)?(?P<file>.*)"):
            lambda file: getattr(self, self.file_type).append(file),
            compile(r"(nothing to commit|无文件要提交，干净的工作区)"):
            lambda: setattr(self, 'is_clean', True)
        }

        out = sh('git status')[1]  # 读取git状态
        for line in out.splitlines():
            for k, v in patterns.items():
                r = k.match(line)
                if r:
                    v(**r.groupdict())
                    break

    def __init__(self):
        if Path('.git').is_dir():
            ver = get_pkg_ver()
            if ver:
                self.verfile, ver = ver
                self.ver = Ver(ver)
                self.proc_git()

    def write_version_file(self):
        self.verfile.text = f'version = "{self.ver}"'

    def show_version(self):     # 显示版本号与git状态
        if self.branch:
            print(f'当前分支：           {self.branch}')
            print(f'远程版本最否最新：   {self.up_to_date}')
            print(f'工作区是否干净：     {self.is_clean}')
            if self.ver:
                print(f'当前版本文件名：     {self.verfile}')
                print(f'当前程序版本：       {self.ver}')
        else:
            print('没有纳入GIT管理')

    def commit_(self):        # 提交变更
        if self.branch == 'master':
            raise Exception('错误：当前git分支必须不能为master')
        if self.is_clean:
            raise Exception('错误：当前工作区无待提交的更改')
        if not self.ver.prerelease:
            raise Exception('错误：当前版本为最终版')
        if self.untracted_files:
            print('下面的文件没有被纳入git监控:')
            [print('\t%s' % (file_name)) for file_name in
             self.untracted_files]
            cmd = None
            while cmd not in ('a', 'A', 'y', 'Y', 'n', 'N'):
                cmd = input(
                    '请选择： Y-全部跟踪,N-全部不跟踪,A-放弃操作：')
                if cmd in ('a', 'A'):
                    print("放弃本次操作，程序退出")
                    return
                elif cmd in ('y', 'Y'):
                    self.not_staged.extend(self.untracted_files)

        if self.not_staged:
            print('以下文件将被提交到git')
            [print('\t%s' % (fil)) for fil in self.not_staged]
            [sh > f'git add "{fil}"' for fil in
             self.not_staged]
            self.to_be_commited.extend(self.not_staged)

        if self.to_be_commited:
            if self.ver:
                ver = str(self.ver)
                self.ver.upgrade()
                print('版本号由%s升级到%s' % (ver, self.ver))
                self.write_version_file()
                sh > f'git commit -a -m "{self.commit}"'
                sh > 'git push --all'

    def upgrade_ver(self):
        ver = self.ver
        if self.branch == 'master':
            raise Exception('错误：当前git分支必须不能为master')

        if self.upgrade not in ('major', 'minor', 'micro', 'dev', 'p', 'patch',
                                'm', 'n', 'o', 'd'):
            raise Exception('错误：参数输入错误')

        if not self.is_clean and self.upgrade in ('d', 'dev',):
            raise Exception('错误：当前工作区有待提交的更改')

        if self.upgrade in ('d', 'dev') and ver.prerelease is None:
            raise Exception('错误：已经是最终版本')

        if self.upgrade not in ('d', 'dev') and ver.prerelease:
            raise Exception('错误：当前版本非最终版')

        if self.ver:
            self.ver.upgrade(self.upgrade)
            print('版本号由%s升级到%s' % (ver, self.ver))
            self.write_version_file()
            ver = self.ver
            if ver.prerelease is None:
                cmds = ['git commit -a -m "升级到最终版"',
                        'git checkout master',
                        'git merge %s' % (self.branch),
                        'git tag ver%s' % (self.ver),
                        'git checkout %s' % (self.branch),
                        'git push --all',
                        'git push --tags',
                        'pysdist',
                        'pysetup']
                for cmd in cmds:
                    sh > cmd

    def sync(self):
        s = sh('git status')[1].splitlines()
        if 'working directory clean' not in s[-1]:
            print(*s, sep='\n')
        elif "Your branch is ahead of" in s[1]:
            sh > 'git push --all'
        sh > 'git pull --all'

    @classmethod
    @arg('-u', '--upgrade', nargs='?', action='store',
         metavar='segment', help=('升级版本号，可以为major,'
                                  'minor,micro,dev'))
    @arg('-c', '--commit', nargs='?', metavar='message', help='提交变更')
    @arg('-s', '--show', action='store_true', help='查看当前版本状态')
    @arg('-y', '--sync', action='store_true', help='同步程序')
    def main(cls, show=None, upgrade=None, commit=None, sync=False):
        obj = cls()
        if obj:
            if show:
                obj.show_version()
            if commit:
                obj.commit = commit
                obj.commit_()
            if upgrade:
                obj.upgrade = upgrade
                obj.upgrade_ver()
            if sync:
                obj.sync()


Pattern = R/r'\d+(\.\d+)*([ab]\d+)?'


def find_ver(path):
    return Ver(str(path))


def get_cur_ver(paths):
    if paths:
        return tuple(sorted(paths, key=lambda x: find_ver(x)))[-1]
