# Final

## Windows Setup

```cmd
%windir%\System32\cmd.exe "/K" C:\Users\HaoVA\anaconda3\Scripts\activate.bat C:\Users\HaoVA\anaconda3
conda create --name steg-final python=3.10
conda activate steg-final
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
python -m pip install "tensorflow<2.11"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/haova/miniconda3/pkgs/cudatoolkit-11.2.2-hbe64b41_10/lib
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -m pip install pyside6
python -m pip install opencv-python
```

```cmd
python src/main.py
```
