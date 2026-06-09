---
theme: seriph
title: Private Service Connect in GCP
info: |
  ## Private Service Connect
  From VPC plumbing to service-oriented connectivity.
class: text-center
transition: slide-left
mdc: true
---

# Private Service Connect

### Connecting to private services in GCP — without the VPC plumbing

<div class="abs-br m-6 text-sm opacity-60">
  GCP Networking · PSC Lab
</div>

<!--
Speaker note: We'll start with the problem — how do you reach a private service
today — walk through the traditional VPC-peering setup, then show how PSC turns
this into a service-oriented model.
-->

---
transition: fade-out
---

# The problem

You have a **service** running in one VPC.<br>
You have a **client** running in another VPC.

<v-clicks>

- Different teams. Different projects. Maybe different orgs.
- The service has **no public IP** — and shouldn't.
- The client just wants to call `https://service/...` privately.

</v-clicks>

<div v-click class="mt-8 text-xl">

So… how do you connect them?

</div>

<!--
The naive answer is "peer the VPCs". Let's see what that actually costs.
-->

---
layout: default
transition: slide-left
---

# Traditional setup: VPC Peering

The two VPCs are stitched together at the network layer.

```mermaid {scale: 0.62}
flowchart LR
  subgraph CONSUMER["Consumer VPC  (10.0.0.0/16)"]
    direction TB
    CSub["Subnet<br/>10.0.1.0/24"]
    Client["Client VM<br/>10.0.1.5"]
    CFW["Firewall rules<br/>allow → 10.50.0.0/16"]
    Client --- CSub
  end

  subgraph PRODUCER["Producer VPC  (10.50.0.0/16)"]
    direction TB
    PSub["Subnet<br/>10.50.1.0/24"]
    Svc["Service<br/>10.50.1.20"]
    PFW["Firewall rules<br/>allow ← 10.0.0.0/16"]
    Svc --- PSub
  end

  CONSUMER <== "VPC Peering<br/>(routes exchanged)" ==> PRODUCER
```

<div class="text-sm opacity-70 mt-2">

Both networks now share routing scope. You're coupling **networks**, not consuming a **service**.

</div>

---
transition: slide-up
---

# Why this hurts

<v-clicks>

- 🔢 **IP coordination** — CIDR ranges must not overlap. Forever. Across every team you peer with.
- 🔗 **No transitive peering** — A↔B and B↔C does *not* give you A↔C. The mesh explodes.
- 🧱 **Firewall sprawl** — every consumer needs rules; every producer must allow each consumer range.
- 👀 **Over-exposure** — peering exposes the *whole* VPC's routes, not just the one service.
- ⛓️ **Tight coupling** — the consumer must know the producer's subnets, IPs, and topology.

</v-clicks>

<div v-click class="mt-6 text-xl">

You wanted to call **one service**. You bought into **someone else's entire network**.

</div>

---
layout: center
class: text-center
transition: slide-left
---

# What if you could just consume a *service*?

<div class="text-2xl opacity-70 mt-4">

No peering. No shared CIDRs. No knowledge of the other VPC.

</div>

<div v-click class="text-3xl mt-10 font-bold text-teal-400">

Private Service Connect

</div>

---
transition: slide-left
---

# PSC: service-oriented connectivity

The producer publishes a **Service Attachment**. The consumer creates an **Endpoint** — an IP *in its own VPC*.

```mermaid {scale: 0.6}
flowchart LR
  subgraph CONSUMER["Consumer VPC  (any CIDR — no coordination)"]
    direction TB
    Client["Client VM"]
    EP["PSC Endpoint<br/>10.0.1.9<br/>(local IP)"]
    Client --> EP
  end

  EP -. "private, one-way<br/>connection" .-> SA

  subgraph PRODUCER["Producer VPC  (opaque to consumer)"]
    direction TB
    SA["Service Attachment"]
    ILB["Internal Load Balancer"]
    Svc["Service"]
    SA --> ILB --> Svc
  end

  style EP fill:#0d9488,color:#fff
  style SA fill:#0d9488,color:#fff
```

<div class="text-sm opacity-70 mt-2">

The consumer talks to a **local IP**. GCP's fabric carries the traffic. The two VPCs never merge.

</div>

---
transition: slide-up
---

# What PSC abstracts away

<div class="grid grid-cols-2 gap-6 mt-4">

<div>

### Gone ✅

<v-clicks>

- Shared / non-overlapping CIDR ranges
- VPC peering & route exchange
- Cross-VPC firewall coordination
- Knowing the producer's topology
- Transitive-peering workarounds

</v-clicks>

</div>

<div>

### What you deal with instead

<v-clicks>

- A **service attachment** (producer side)
- An **endpoint IP** in your own VPC
- Connection accept/reject by the producer
- That's basically it

</v-clicks>

</div>

</div>

<div v-click class="mt-6 text-center text-xl">

The unit of connectivity is now a **service**, not a **network**.

</div>

---
layout: default
transition: fade
---

# Side by side

<div class="text-sm">

| | VPC Peering | Private Service Connect |
|---|---|---|
| **Unit of connection** | Whole network | A single service |
| **IP coordination** | Required (no overlap) | None — consumer uses its own IPs |
| **Routing scope exposed** | Entire peered VPC | Just the endpoint |
| **Transitive** | No (mesh explodes) | N/A — each endpoint is independent |
| **Firewall rules** | Per-consumer ranges | Local to the endpoint |
| **Coupling** | Tight (topology-aware) | Loose (service-oriented) |
| **Who initiates** | Symmetric | Consumer → producer, one-way |

</div>

---
layout: center
class: text-center
transition: slide-up
---

# Takeaways

<v-clicks>

<div class="text-xl">🔌 PSC turns private connectivity into a <b>publish / consume</b> model.</div>

<div class="text-xl">🧭 No shared CIDRs, no peering mesh, no topology leakage.</div>

<div class="text-xl">🏷️ Producers expose a <b>service attachment</b>; consumers get a <b>local endpoint</b>.</div>

<div class="text-xl mt-6 opacity-80">Same goal — reach a private service — but coupled at the <b>service</b> layer, not the <b>network</b> layer.</div>

</v-clicks>

---
layout: center
class: text-center
---

# Thanks

Let's build it in the lab →

<div class="abs-br m-6 text-sm opacity-60">
  psc-lab
</div>
