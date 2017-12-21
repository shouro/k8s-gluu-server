# Kubernetes Gluu server

## Overview

This is gluu server for kubernetis. This readme will deploy gluu server in minikube, a single node cluter as a basic example.

## Tools needed:

- virtualbox
- minikube
- kubectl
- git

## Installaction guide

### Start minikube vm

```
$ minikube start
```

This command will start a single kubernetis node.

### Clone gluu kubernetes project

```
$ git clone https://github.com/GluuFederation/k8s-gluu-server.git
```

Then Change to k8s-gluu-server dir.

### Create volume and volume claim

```
$ kubectl create -f persistent-volume.yaml
$ kubectl create -f persistent-volume-claim.yaml
```

### Create consul deployment

```
$ kubectl create -f consul.yaml
```

### Create consul service

```
$ kubectl create -f consul-svc.yaml
```

### Expose consul

```
$  kubectl create -f consul-svc-np.yaml
```

### Get consul service port and minikube ip

```
$ minikube ip
```

this will show minikube ip, save it for later use.

```
$ kubectl get svc
```

example output:

```
NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
gluuconsul      ClusterIP   10.102.30.247    <none>        8500/TCP         1d
gluuconsul-np   NodePort    10.103.246.9     <none>        8500:30769/TCP   1d

```

for example, save this exposed consule service port "30769" for later use

### Genarate configuration

This cmd will genarate important configuration

```
$ docker run --rm \
    gluufederation/config-init:3.1.1_dev \
    --admin-pw admin@1234 \
    --email support@gluu.local \
    --domain k8s.gluu.local \
    --org-name gluuinc \
    --kv-host <minikube-ip> \
    --kv-port <exposed-consule-service-port> \
    --save
```

### Deploy ldap in another vm

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

### Add external ldap server endpoint to kubernetis cluster

For example, Edit this line '- ip: "192.168.33.100"' in ext-openldap.yaml to set ldap virtual machines ip.
Then run this command.

```
$ kubectl create -f ext-openldap.yaml
```

### Create oxauth deployemnt

```
$ kubectl create -f oxauth.yaml
$ kubectl create -f oxauth-svc.yaml
```

### Create oxtrust deployemnt

```
$ kubectl create -f oxtrust.yaml
$ kubectl create -f oxtrust-svc.yaml
```

### Create keyrotation deployemnt

```
$ kubectl create -f keyrotation.yaml
```

### Expose oxauth and oxtrust using nginx

TODO
