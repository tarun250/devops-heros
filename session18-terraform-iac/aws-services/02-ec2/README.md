# EC2 — Elastic Compute Cloud (Compute)

**What it is:** virtual machines in AWS. You choose the OS image, size, network and storage, and pay per second while it runs.

| Concept | Meaning |
|---|---|
| **AMI** | Amazon Machine Image — the template the VM boots from (OS + preinstalled software): Amazon Linux, Ubuntu, or your own custom AMI |
| **Instance type** | CPU/RAM size: family + generation + size, e.g. `t3.micro`, `m7i.large`. `t` burstable, `m` general, `c` compute, `r` memory, `g` GPU |
| **Key pair** | SSH key: AWS keeps the public key, you download the private `.pem` once |
| **Security Group** | stateful firewall on the instance — allow rules only (e.g. 22 from my IP, 80 from anywhere) |
| **EBS** | Elastic Block Store — network disk attached to one instance; survives stop/start; snapshots for backup. Types `gp3` (general), `io2` (high IOPS) |
| **Instance store** | local disk on the physical host, lost when the instance stops |

## Public vs private IP

| | Private IP | Public IP | Elastic IP |
|---|---|---|---|
| Reachable from | inside the VPC | internet | internet |
| Changes on stop/start | no | **yes** | no (static, you own it) |
| Needs | a subnet | public subnet + IGW route | allocation |

## Instance lifecycle

```text
pending → running → stopping → stopped → (start) → pending → running
running → rebooting → running
running/stopped → shutting-down → terminated   (gone; root EBS deleted by default)
```

Stopped = no compute charge, but you still pay for the EBS volume. Terminated = deleted for good.

## Common use cases

- Web/app servers behind a load balancer in an Auto Scaling Group.
- Jenkins or build agents, bastion hosts.
- Kubernetes worker nodes (EKS node groups are EC2 instances).
- Lift-and-shift of on-prem VMs.
