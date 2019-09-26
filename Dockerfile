FROM tensorflow/tensorflow:latest-gpu-py3-jupyter
EXPOSE 8888
ADD environment.yml /
RUN conda update -n base conda -y && conda env update && \
    jupyter labextension install @jupyterlab/plotly-extension
WORKDIR /root
RUN git init && \
    git remote add origin https://github.com/AmirrezaSlt/graph_embedding.git && \
    git pull origin master
CMD jupyter lab --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='amirreza'
