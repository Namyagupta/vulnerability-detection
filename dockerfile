FROM continuumio/miniconda3
COPY environment.yml .
RUN conda env create -f environment.yml
RUN conda activate web
RUN streamlit run app.py