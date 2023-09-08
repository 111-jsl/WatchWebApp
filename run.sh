# for mac
brew cask install docker
docker build -t watch_streamlit .
docker images
docker run -p 8501:8501 watch_streamlit
