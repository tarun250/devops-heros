# Session 14 - Kubernetes Troubleshooting (Screenshots)

## 01-kubectl-get

**Create the Pod**
![Create pod](./screenshots/01-01-apply.png)

**Check Pods**
![Get pods](./screenshots/01-02-get-pods.png)

**Get More Information**
![Get pods wide](./screenshots/01-04-wide.png)

**Check Different Resources**
![Get resources](./screenshots/01-05-resources.png)

**Watch Changes**
![Watch pods](./screenshots/01-06-watch.png)

## 02-kubectl-describe

**Create the Pod**
![Create pod](./screenshots/02-01-apply.png)

**Describe the Pod**
![Describe pod](./screenshots/02-02-describe.png)

**Describe Other Resources**
![Describe deployment and service](./screenshots/02-06-other.png)
![Describe node](./screenshots/02-06-node.png)

## 03-kubectl-logs

**Create the Pod**
![Create pod](./screenshots/03-01-apply.png)

**Check the Pod**
![Get pod](./screenshots/03-02-get.png)

**Check Logs**
![Logs](./screenshots/03-03-logs.png)

**Follow Logs**
![Follow logs](./screenshots/03-04-follow.png)

**Previous Container Logs / Multiple Containers**
![Previous logs](./screenshots/03-06-previous.png)

## 04-kubectl-exec

**Create the Pod**
![Create pod](./screenshots/04-01-apply.png)

**Open a Shell / Check Files / Check the Application**
![Shell](./screenshots/04-02-shell.png)

**nginx -T and Exit**
![nginx -T](./screenshots/04-04-nginx-T.png)

**Run One Command Without Opening Shell**
![One command](./screenshots/04-06-one-command.png)

## 05-events

**Create the Pod**
![Create pod](./screenshots/05-01-apply.png)

**Check Events**
![Events](./screenshots/05-02-events.png)

**Sort Events**
![Sorted events](./screenshots/05-03-sorted.png)

**Describe Also Shows Events**
![Describe events](./screenshots/05-04-describe.png)

**Watch Events**
![Watch events](./screenshots/05-06-watch.png)

## 06-crashloopbackoff

**Create The Broken Pod**
![Broken pod](./screenshots/06-01-broken.png)

**Describe**
![Describe](./screenshots/06-03-describe.png)

**Check Logs / Previous Logs**
![Logs](./screenshots/06-04-logs.png)

**Fix The Pod / Check Logs Again**
![Fix](./screenshots/06-07-fix.png)

## 07-imagepullbackoff

**Create The Broken Pod**
![Broken pod](./screenshots/07-01-broken.png)

**Describe The Pod**
![Describe](./screenshots/07-03-describe.png)

**Fix The Image**
![Fix](./screenshots/07-05-fix.png)

## 08-pending-pods

**Create The Broken Pod**
![Broken pod](./screenshots/08-01-broken.png)

**Why Is It Pending?**
![Describe](./screenshots/08-02-describe.png)

**Check Nodes**
![Nodes](./screenshots/08-03-nodes.png)

**Fix The Pod**
![Fix](./screenshots/08-04-fix.png)

## 09-service-dns-troubleshooting

**Create The Application**
![Deployment](./screenshots/09-01-deploy.png)

**Create The Service**
![Service](./screenshots/09-02-service.png)

**Check Service Details**
![Describe service](./screenshots/09-03-describe.png)

**Check Endpoints**
![Endpoints](./screenshots/09-04-endpoints.png)

**Test DNS**
![DNS test pod](./screenshots/09-06-dns-pod.png)

**Test Service DNS**
![nslookup](./screenshots/09-07-nslookup.png)

**Test HTTP Connection**
![wget](./screenshots/09-08-wget.png)

**Intentionally Break The Service**
![Broken service](./screenshots/09-09-broken.png)

**Fix The Service**
![Fix service](./screenshots/09-11-fix.png)

**Check Pod Labels**
![Labels](./screenshots/09-13-labels.png)

**Check CoreDNS**
![CoreDNS pods](./screenshots/09-14-coredns.png)

**Check DNS Configuration**
![resolv.conf](./screenshots/09-15-resolv.png)

**Check CoreDNS Logs**
![CoreDNS logs](./screenshots/09-16-coredns-logs.png)
