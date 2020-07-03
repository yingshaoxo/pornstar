#!/usr/bin/env /usr/bin/python3

from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()


class Tools():
    def checklogs(self):
        path_of_log_file = t.fix_path("~/Pornstar/_main.log")
        t.run(f"tail -F {path_of_log_file}")

    def compile(self):
        commands = """
python3 -m nuitka --module pornstar --include-package=pornstar._deeplab,pornstar._main,pornstar._PIL_filters,pornstar._CV2_filters --output-dir=build
        """
        t.run(commands)

    def push(self, comment):
        self.make_docs()
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

    def make_docs(self):
        t.run("""
sudo pip3 install pdoc3
mkdir docs
rm docs/* -fr
pdoc --html --output-dir docs pornstar._main 
mv docs/pornstar/_main.html docs/index.html
rm docs/pornstar -fr
        """)

    def install(self):
        #self.make_docs()
        t.run("""
sudo rm -fr dist
sudo rm -fr build
sudo pip3 uninstall -y pornstar
sudo -H python3 setup.py sdist bdist_wheel
#cd dist
#sudo pip3 install auto_everything*
sudo pip3 install -e .
#cd ..
""")

    def publish(self):
        self.make_docs()
        t.run("""
sudo rm -fr dist
sudo rm -fr build
sudo pip3 install -U twine wheel setuptools
sudo -H python3 setup.py sdist bdist_wheel
twine upload dist/*
""")


py.make_it_runnable()
py.fire(Tools)
