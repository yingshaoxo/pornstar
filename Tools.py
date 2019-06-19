#!/usr/bin/env /usr/bin/python3

from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()

class Tools():
    def checklogs(self):
        path_of_log_file = t.fix_path("~/Pornstar/__main.log")
        t.run(f"tail -F {path_of_log_file}")

    def compile(self):
        commands = """
python3 -m nuitka --module pornstar --include-package=pornstar.__utils,pornstar.__model,pornstar.__coco,pornstar.__config,pornstar.__main,pornstar.__PIL_filters --output-dir=build
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

    def publish(self):
        t.run("""
#python3 setup.py register
python3 setup.py sdist
#python3 setup.py sdist upload
""")

py.make_it_runnable()
py.fire(Tools)
