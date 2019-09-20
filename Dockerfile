FROM continuumio/miniconda3
EXPOSE 8888
ADD environment.yml /
RUN conda update -n base conda -y && conda env update
RUN git clone https://github.com/AmirrezaSlt/graph_embedding.git
WORKDIR /graph_embedding
CMD jupyter lab --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='amirreza'
