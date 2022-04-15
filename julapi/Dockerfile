FROM julia:1.7

ENV JULIA_NUM_THREADS=2
WORKDIR /opt/julapi/
COPY . .
RUN julia --project="." -e 'import Pkg; Pkg.instantiate();'
RUN julia --project=. precompile.jl
EXPOSE 8081

CMD ["bash"]
