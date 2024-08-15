# mice-video-lable

mICE Video Label is a tool to mark ROI (Region of Interest), i.e. the location of the food pellet, in the video of mice behavior. The tool is developed using Python and OpenCV library. Minimizing the memory usage while keeping the ease of use for researchers is the main goal of this tool.

## Environments

### To create a new conda environment

Need to be done only once

    conda env create --name mice-videomarker --file environment.yml 

### To activate the environment

Need to be done every time you open a new terminal

    conda activate mice-videomarker

(Optional) To check whether the environment is activated

    conda info --envs

(Optional) Run test command to check whether the environment is activated and the libraries are installed correctly

    python utils.py

### To run the application

Please noted that the application is still in development. Therefore, the application might not work as expected. Create `apps_xxx.py` file to create a new application. The `xxx` is the name of the application. The application will be run using the following command:

    python apps_xxx.py

For example, to run the `apps_test.py` application, run the following command:

    python apps_test.py

In `main.py`, the well tested apps will implemented in the main file. The main file will be the main entry point of the application. You can use it as the template to create a new application.


### To Install Additional Packages

1. Install the package

    ```bash
    conda install <package_name>
    ```

2. Update the environment.yml file

    ```bash
    conda env export --from-history > environment.yml
    ```

3. Update the environment

    ```bash
    conda env update --file environment.yml
    ```

## Noted

- In some cases, the environment.yml file might updated from branch to branch. Therefore, it is recommended to update your environment before running the application. Especially if you are switching branches. Or rebasing your branch to the latest master branch.