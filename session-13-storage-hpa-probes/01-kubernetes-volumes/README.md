# Kubernetes Volumes — What I Learned

A container's filesystem is thrown away when the container restarts. Volumes give a Pod storage that lives longer than one container — and, with PVs, longer than the Pod.

Manifests used: [`../01-volumes`](../01-volumes), [`../02-persistent-storage`](../02-persistent-storage), [`../03-storageclass`](../03-storageclass). All screenshots are from my Minikube cluster.

---

## emptyDir

- Created empty when the Pod is scheduled, deleted when the Pod is deleted.
- Survives container restarts inside the same Pod.
- Use for: scratch space, cache, sharing files between containers in one Pod.

```yaml
volumes:
  - name: app-storage
    emptyDir: {}
```

Wrote a file, deleted the Pod, recreated it — file gone:

![emptyDir write](../screenshots/02-emptydir-write.png)
![emptyDir gone](../screenshots/03-emptydir-gone.png)

## hostPath

- Mounts a directory from the **node** into the Pod.
- Data survives Pod deletion, but only on that node — if the Pod moves to another node, the data isn't there.
- Security risk (Pod can read the node's files). Fine for single-node labs, avoid in production.

```yaml
volumes:
  - name: host-storage
    hostPath:
      path: /tmp/hostpath-data
      type: DirectoryOrCreate
```

![hostPath](../screenshots/04-hostpath.png)

## PersistentVolume (PV)

- A piece of storage in the cluster, created by an admin (static) or by a StorageClass (dynamic).
- Cluster-scoped, independent of any Pod.
- Has capacity, access mode and reclaim policy.

| Access mode | Meaning |
|---|---|
| `ReadWriteOnce` (RWO) | read-write by one node |
| `ReadOnlyMany` (ROX) | read-only by many nodes |
| `ReadWriteMany` (RWX) | read-write by many nodes |

| Reclaim policy | After the PVC is deleted |
|---|---|
| `Retain` | PV and data stay, admin cleans up |
| `Delete` | PV and the underlying storage are deleted |

## PersistentVolumeClaim (PVC)

- A Pod's **request** for storage: "I need 500Mi, RWO".
- Kubernetes binds it to a matching PV. The Pod only refers to the PVC, never the PV.

```yaml
volumes:
  - name: persistent-storage
    persistentVolumeClaim:
      claimName: student-pvc
```

![PV and PVC](../screenshots/05-pv-pvc.png)

Pod wrote to the PVC, was deleted, the new Pod still reads the data:

![PVC persistence](../screenshots/06-pvc-pod-persist.png)

What I noticed: `student-pvc` has no `storageClassName`, so the default `standard` class created a new PV for it, and my manual `student-pv` stayed `Available`. To bind to a static PV, set `storageClassName: ""` on the PVC.

## StorageClass

- A "type" of storage plus the provisioner that creates it (`k8s.io/minikube-hostpath` on Minikube, `ebs.csi.aws.com` on EKS).
- One class can be the default.
- `volumeBindingMode: Immediate` creates the volume right away; `WaitForFirstConsumer` waits until a Pod uses it (picks the right zone).

## Dynamic provisioning

No PV written by hand: the PVC names a StorageClass and the provisioner creates the PV automatically.

```yaml
kind: PersistentVolumeClaim
spec:
  storageClassName: standard
  resources:
    requests:
      storage: 500Mi
```

![StorageClass and dynamic PV](../screenshots/07-storageclass.png)

The PV `pvc-929ca367…` was created by the provisioner 4 seconds after the PVC.

---

## Summary

| Type | Lives as long as | Shared across nodes | Typical use |
|---|---|---|---|
| emptyDir | the Pod | no | cache, temp files |
| hostPath | the node | no | node agents, labs |
| PV + PVC (static) | until deleted / reclaimed | depends on backend | pre-created disks |
| PVC + StorageClass (dynamic) | until deleted / reclaimed | depends on backend | databases, app data |
