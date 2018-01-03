# Kubernetes Gluu server

## Overview

Gluu Server on Kubernetes. This readme will deploy gluu server in minikube, a single node cluter as a basic example.

## Tools needed:

- [virtualbox](https://www.virtualbox.org/wiki/Downloads)
- or [KVM2](https://github.com/kubernetes/minikube/blob/master/docs/drivers.md#kvm2-driver)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-binary-via-curl)
- [minikube](https://github.com/kubernetes/minikube)
- [docker](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu)
- git ('apt install git' or 'yum install git')

## Installation guide

### Start minikube vm

```
$ minikube start
```

This command will start a single kubernetes node.

### Clone gluu kubernetes project

```
$ git clone https://github.com/GluuFederation/k8s-gluu-server.git
```

Then Change to k8s-gluu-server dir.

```
$ cd k8s-gluu-server/
```

### Run this command to setup consul in minikube single node cluster

```
$ kubectl create -f stage1.yaml
```

### Get consul service port and minikube ip

```
$ minikube ip
```

this will show minikube ip, save it for later use.

```
$ kubectl get svc
```

Example output:

```
NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
gluuconsul      ClusterIP   10.102.30.247    <none>        8500/TCP         1d
gluuconsul-np   NodePort    10.103.246.9     <none>        8500:30769/TCP   1d

```

For example, save this exposed consule service port "30769" for later use

### Genarate configuration

This cmd will genarate configuration and put it in consul.
For this guide we will use "k8s-gluu-server" as gluu hostname.

```
$ docker run --rm \
    gluufederation/config-init:3.1.1_dev \
    --admin-pw admin@1234 \
    --email support@gluu.local \
    --domain k8s-gluu-server \
    --org-name gluuinc \
    --kv-host <minikube-ip> \
    --kv-port <exposed-consule-service-port> \
    --save
```

### Deploy ldap in another vm

**Note: This ladp deployment is only an example.**
Create a virtual machine using virtualbox. Get its ip. Then run this cmd inside new vm:

```
$ docker run -d \
    --name openldap-init \
    --network=host \
    -e GLUU_KV_HOST=<minikube-vm-ip> \
    -e GLUU_KV_PORT=<exposed-consule-service-port> \
    -e GLUU_LDAP_INIT=true \
    -e GLUU_LDAP_INIT_HOST=<this-vm-ip> \
    -e GLUU_LDAP_INIT_PORT=1389 \
    -v /home/gluu/flag:/flag \
    gluufederation/openldap:3.1.1_dev
```

### Generate stage2.yaml

To run this command we need the ip of our LDAP vm for `ldap-location` and the `domain`, defined above, as `gluu hostname`.

For example:
ldap location : 192.168.xx.xxx:1389
gluu hostname : k8s-gluu-server
You need 'click' to run this script.

```
$ pip install click
$ python gluuk8s.py --ldap-location=192.168.xx.xxx:1389 --k8s-gluu-hostname=k8s-gluu-server > /path/of/stage2.yaml
```

This will create stage2.yaml file.

### Run stage2

```
$ kubectl create -f /path/of/stage2.yaml
```

This will deploy oxauth, oxtrust and nginx services in minikube node.

### Use deployed services

TODO
