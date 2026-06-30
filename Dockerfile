FROM node:26

RUN apt-get update -y \
    && apt-get install curl libatomic1 git -y
USER 1000:1000
RUN mkdir -p ~/.config \
    && curl -fsSL https://opencode.ai/install | bash \
    && wget -qO- https://get.pnpm.io/install.sh | ENV="$HOME/.bashrc" SHELL="$(which bash)" bash -

EXPOSE 4096

CMD ["/root/.opencode/bin/opencode", "serve", "--hostname", "0.0.0.0"]
