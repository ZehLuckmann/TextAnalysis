sudo docker kill ancon-desenv
sudo docker rm ancon-desenv
sudo docker run -d -p 8080:8080 -it --name ancon-desenv -v `pwd`:/src ancon_img 
sudo docker exec -it ancon-desenv bash
