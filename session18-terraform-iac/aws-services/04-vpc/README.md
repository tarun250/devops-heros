# VPC — Virtual Private Cloud (Networking)

**What it is:** your own isolated network inside an AWS region. You choose the IP range, split it into subnets, and control routing and firewalls.

## CIDR

An IP range written as `address/prefix`; the prefix is how many leading bits are fixed.

| CIDR | Addresses | Typical use |
|---|---|---|
| `10.0.0.0/16` | 65,536 | a whole VPC |
| `10.0.1.0/24` | 256 (251 usable — AWS reserves 5 per subnet) | one subnet |

Subnets must sit inside the VPC CIDR and must not overlap.

## Building blocks

| Component | What it does |
|---|---|
| **Subnet** | a slice of the VPC CIDR in **one** Availability Zone |
| **Route table** | rules for where traffic goes; every subnet is associated with one |
| **Internet Gateway (IGW)** | connects the VPC to the internet, both directions |
| **NAT Gateway** | lets **private** subnets reach out to the internet (updates, image pulls) without being reachable from it; lives in a public subnet and is billed per hour |
| **Security Group** | stateful firewall on an instance/ENI; allow rules only; return traffic allowed automatically |
| **Network ACL** | stateless firewall on a subnet; allow **and** deny rules, evaluated in rule-number order; return traffic must be allowed explicitly |

## Public vs private subnet

The difference is only the route table:

| | Default route `0.0.0.0/0` → | Instances get | Used for |
|---|---|---|---|
| Public subnet | Internet Gateway | public IPs | load balancers, bastion, NAT Gateway |
| Private subnet | NAT Gateway (or none) | private IPs only | app servers, databases |

```text
            Internet
               │
              IGW
               │
┌──────────── VPC 10.0.0.0/16 ─────────────┐
│  Public subnet 10.0.1.0/24               │
│    ALB, NAT GW                           │
│        │                                 │
│  Private subnet 10.0.2.0/24              │
│    app servers, database                 │
└──────────────────────────────────────────┘
```

## Security Group vs NACL

| | Security Group | Network ACL |
|---|---|---|
| Applies to | instance / ENI | subnet |
| State | stateful | stateless |
| Rules | allow only | allow + deny |
| Evaluation | all rules | lowest number first |

My Terraform VPC: [`../../../session19-cloud-terraform/09-cloud-infra-project`](../../../session19-cloud-terraform/09-cloud-infra-project).
