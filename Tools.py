#!/usr/bin/env /usr/bin/python3

from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()

class Tools():
    def compile(self):
        commands = """
python3 -m nuitka --module pornstar.py --include-package=lib --output-dir=build
        """
        t.run(commands)

    def push(self, comment):
        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def reset(self):
        t.run("""
git reset --hard HEAD^
""")

py.make_it_runnable()
py.fire(Tools)
