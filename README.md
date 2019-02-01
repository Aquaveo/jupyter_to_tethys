# jupyter_to_tethys
Examples and prototypes from research on how to transition Jupyter notebooks to Tethys apps.

**Jupyter2Tethys Development Environment Setup**



**0. Prerequisites**

1) Ubuntu 18.04 x64 Desktop

2) miniconda3

3) PyCharm community edition

**1. Setup Conda Env**

1) $ git clone [https://github.com/Aquaveo/jupyter\_to\_tethys.git](https://github.com/Aquaveo/jupyter_to_tethys.git)

2) $ cd  jupyter\_to\_tethys

3) $ conda env create --name j2t --file environment.yml

4) $ conda activate j2t

**2. Start Jupyter to view notebook examples**

1) $ jupyter notebook

2) Navigate to &quot;reviews&quot;



**3. Run DjangoBokeh in Terminal**

1) Download sample data &quot;[nyc\_taxi\_wide.parq](https://s3.amazonaws.com/datashader-data/nyc_taxi_wide.parq)&quot;, and put in folder &quot;jupyter\_to\_tethys/embedding/deep/my\_django\_bokeh\_site/djangobokeh/bokeh\_apps/data&quot;

2) cd jupyter\_to\_tethys/embedding/deep/my\_django\_bokeh\_site

3) $ python manage.py runserver --noreload

4) Check app &quot;sliders&quot; in browser: [http://127.0.0.1:8000/bokehapps/sliders](http://127.0.0.1:8000/bokehapps/sliders)

5) Check app &quot;nyc\_pickup&quot; in browser: [http://127.0.0.1:8000/bokehapps/nyc\_pickup](http://127.0.0.1:8000/bokehapps/nyc_pickup)



**4. Setup PyCharm Visual Debugging for DjangoBokeh**

1) Open folder &quot;jupyter\_to\_tethys&quot; with PyCharm

2) File-\&gt;Settings-\&gt;Project-\&gt;Project Interpreter-\&gt;upper-right Gear icon-\&gt;Add

3) Virtualenv Environment -\&gt; Existing environment -\&gt; Check &quot;Make available to all projects&quot;-\&gt; Click 3-dot icon



4) Select the python executable in j2t conda environment

5) PyCharm will search and load all installed libs in &quot;j2t&quot; conda environment; Click OK;



6) Click &quot;Add Configuration...&quot;

7) Click + icon and click &quot;Python&quot;

8) Name: &quot;djangobokeh&quot;;

Point &quot;Script path&quot; to file &quot;manage.py&quot;;

Set &quot;Parameters&quot;  to &quot;runserver -noreload&quot;;

Point &quot;Python interpreter&quot; to &quot;j2t&quot; Python instance;

Click OK;



9) Select &quot;djangobokeh&quot; then click &quot;Run&quot; icon;

Test two apps: [http://127.0.0.1:8000/bokehapps/sliders](http://127.0.0.1:8000/bokehapps/sliders)

and [http://127.0.0.1:8000/bokehapps/nyc\_pickup](http://127.0.0.1:8000/bokehapps/nyc_pickup)

10) Set a breakpoint and click &quot;Debug&quot; icon



**5. Setup PyCharm Visual Debugging for Bokeh**

1) Click &quot;Edit Configurations...&quot;;

2) Click + icon and click &quot;Python&quot;;

3) Name: &quot;bokeh&quot;;

Point &quot;Script path&quot; to file &quot;jupyter\_to\_tehtys/bokeh\_debug/bokeh\_debug\_entry.py&quot;;

Point &quot;Python interpreter&quot; to &quot;j2t&quot; Python instance;

Click OK;

4) Run Bokeh with two sample apps;

5) Set breakpoint and Debug Bokeh; Step into Bokeh source code;