---
theme: seriph
title: Private Service Connect in GCP
info: From VPC plumbing to service-oriented connectivity.
layout: default
class: text-left
transition: fade-out
mdc: true
fonts:
  sans: Hanken Grotesk
  display: Bricolage Grotesque
  mono: JetBrains Mono
  weights: '300,400,500,600,700,800'
---

<div class="flex items-stretch gap-12 h-full">
  <div class="flex-1 flex flex-col justify-center">
    <div class="flex items-center gap-4">
      <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg" />
      <h1 class="title-display !text-6xl !mb-0">Private <span class="grad-psc">Service Connect</span></h1>
    </div>
    <div class="mt-10 text-2xl font-semibold" style="color:var(--ink)">Pradip Caulagi &amp; Pramod Kumar</div>
    <div class="mt-1 dim" style="font-family:var(--font-mono);font-size:0.95rem">10 June 2026</div>
  </div>
  <div class="imgpanel" style="flex:1"><img src="./assets/title.png" style="object-position:center top" /></div>
</div>

<!--
The problem, then the traditional peering setup and its costs, then PSC as a
publish/consume model.
-->

---
transition: fade-out
---

<div class="h-full flex flex-col">

<div class="kicker">The problem</div>
<h1 class="mt-3">
  “Loose lips sink ships”
  <span style="text-align:right;font-style:italic;font-size:0.72rem;letter-spacing:0.02em;color:var(--pain);margin-top:0.15rem">— U.S. wartime security slogan, 1942</span>
</h1>
<p class="mt-3 max-w-2xl">Your production services talk constantly — those conversations shouldn't be exposed on the public internet.</p>

<div class="flex-1 flex flex-col justify-center">

<div class="grid grid-cols-3 gap-5">
  <div class="prob">
    <div class="prob__viz">
      <img src="./assets/gcp/cloud_apis.svg" class="gcp" />
      <span class="conn conn--bad" style="width:16px"></span><span class="gap__q" style="font-size:1.3rem">?</span><span class="conn conn--bad" style="width:16px"></span>
      <img src="./assets/gcp/compute_engine.svg" class="gcp" />
    </div>
    <div class="prob__title">Service ↔ service</div>
    <div class="prob__sub">two private services need to talk</div>
  </div>

  <div class="prob">
    <div class="prob__viz">
      <img src="./assets/gcp/compute_engine.svg" class="gcp" />
      <span class="conn conn--bad" style="width:16px"></span><span class="gap__q" style="font-size:1.3rem">?</span><span class="conn conn--bad" style="width:16px"></span>
      <img src="./assets/gcp/cloud_sql.svg" class="gcp" />
      <img src="./assets/gcp/memorystore.svg" class="gcp" />
    </div>
    <div class="prob__title">Service → database / cache</div>
    <div class="prob__sub">the managed data it depends on</div>
  </div>

  <div class="prob">
    <div class="prob__viz">
      <img src="./assets/gcp/compute_engine.svg" class="gcp" />
      <span class="conn conn--bad" style="width:16px"></span><span class="gap__q" style="font-size:1.3rem">?</span><span class="conn conn--bad" style="width:16px"></span>
      <img src="./assets/gcp/cloud_interconnect.svg" class="gcp" />
    </div>
    <div class="prob__title">Service → on-prem</div>
    <div class="prob__sub">across the hybrid edge</div>
  </div>
</div>

<p class="text-center text-xl mt-8 dim">Each needs a <strong>private path</strong> — without peering whole networks.</p>

</div>

</div>

---
transition: fade-out
---

<div class="kicker kicker--pain">The traditional answer</div>
<h1 class="mt-4">Stitch the networks with <span class="grad-pain">VPC peering</span></h1>

<div class="diagram !mt-12">
  <div class="vpc vpc--pain">
    <div class="vpc__title"><span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm inline" /> Consumer VPC</span><span class="chip--pain chip">10.0.0.0/16</span></div>
    <div class="flex gap-3 justify-center mt-4">
      <div class="svc !py-3"><img src="./assets/gcp/compute_engine.svg" class="gcp" /><div class="svc__meta">10.0.1.5</div></div>
      <div class="svc !py-3"><img src="./assets/gcp/cloud_network.svg" class="gcp" /><div class="svc__meta">subnet</div></div>
    </div>
    <div class="flex justify-center mt-4"><span class="fw"><img src="./assets/gcp/cloud_firewall_rules.svg" class="gcp gcp--sm" /> allow → 10.50/16</span></div>
  </div>

  <div class="link">
    <div class="link__label grad-pain">PEERING</div>
    <div class="wire wire--pain wire--stack"></div>
    <div class="wire wire--pain wire--stack"></div>
    <div class="wire wire--pain wire--stack"></div>
    <div class="link__cap">routes exchanged</div>
  </div>

  <div class="vpc vpc--pain">
    <div class="vpc__title"><span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm inline" /> Producer VPC</span><span class="chip--pain chip">10.50.0.0/16</span></div>
    <div class="flex gap-3 justify-center mt-4">
      <div class="svc !py-3"><img src="./assets/gcp/cloud_apis.svg" class="gcp" /><div class="svc__meta">10.50.1.20</div></div>
      <div class="svc !py-3"><img src="./assets/gcp/cloud_network.svg" class="gcp" /><div class="svc__meta">subnet</div></div>
    </div>
    <div class="flex justify-center mt-4"><span class="fw"><img src="./assets/gcp/cloud_firewall_rules.svg" class="gcp gcp--sm" /> allow ← 10.0/16</span></div>
  </div>
</div>

<p class="text-center dim mt-7">Coupling <strong>networks</strong> — not consuming a <em>service</em>.</p>

---
transition: fade-out
---

<div class="h-full flex flex-col">

<div class="kicker kicker--pain">The cost</div>
<h1 class="mt-2 !text-4xl">Access becomes a <span class="grad-pain">network</span> problem</h1>
<p class="dim mt-1 max-w-3xl">Peering ties <em>who may talk to whom</em> to IP ranges and firewall rules — brittle and coupled.</p>

<div class="flex-1 flex flex-col justify-center">

<div class="grid grid-cols-3 gap-5">

  <div class="prob" v-click="1" :class="{ dull: $clicks > 1 }">
    <div class="prob__viz">
      <div class="vmini"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp" /><span class="chip--pain chip">10.0.0.0/16</span></div>
      <div class="collide">⚡</div>
      <div class="vmini"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp" /><span class="chip--pain chip">10.0.0.0/16</span></div>
    </div>
    <div class="prob__title">Coupled to their network</div>
    <div class="prob__sub">coordinate CIDRs and know their subnets &amp; IPs — forever</div>
  </div>

  <div class="prob" v-click="2" :class="{ dull: $clicks > 2 }">
    <div class="prob__viz">
      <div class="fan">
        <span class="chip--pain chip">10.0/16</span>
        <span class="chip--pain chip">10.2/16</span>
        <span class="chip--pain chip">10.4/16</span>
        <span class="faint text-xs">+14 more…</span>
      </div>
      <span class="arrow">→</span>
      <img src="./assets/gcp/cloud_firewall_rules.svg" class="gcp gcp--lg" />
    </div>
    <div class="prob__title">Firewall rules pile up</div>
    <div class="prob__sub">every consumer range, allow-listed</div>
  </div>

  <div class="prob" v-click="3" :class="{ dull: $clicks > 3 }">
    <div class="prob__viz">
      <div class="exposed">
        <img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" />
        <img src="./assets/gcp/compute_engine.svg" class="gcp gcp--sm" />
        <img src="./assets/gcp/cloud_network.svg" class="gcp gcp--sm" />
        <img src="./assets/gcp/cloud_load_balancing.svg" class="gcp gcp--sm" />
        <span class="mark mark--x text-lg">👁</span>
      </div>
    </div>
    <div class="prob__title">The whole VPC is exposed</div>
    <div class="prob__sub">peering shares all routes — not one service</div>
  </div>

</div>

<p v-click="4" class="text-center text-2xl mt-9">Access is decided by <strong>IP address</strong> — <span class="grad-pain font-bold">not by <em>who</em> is calling.</span></p>

</div>

</div>

---
layout: center
class: text-center
transition: fade-out
---

<div class="kicker justify-center">Identity &amp; Access Management</div>
<h1 class="!text-5xl mt-5">IAM answers one question:<br/><span class="grad-psc">who can do what?</span></h1>

<div class="flex items-stretch justify-center gap-3 mt-9">
  <div class="prob items-center text-center" style="width:235px">
    <div style="height:72px;display:flex;align-items:center"><img src="./assets/gcp/identity_and_access_management.svg" class="gcp gcp--lg" /></div>
    <div class="prob__title mt-1">Who</div>
    <div class="prob__sub">a principal — user, group, or service identity</div>
  </div>
  <div class="flex items-center"><span class="arrow" style="font-size:1.6rem">→</span></div>
  <div class="prob items-center text-center" style="width:235px">
    <div style="height:72px;display:flex;align-items:center;gap:.4rem"><span class="chip--ip chip">invoke</span><span class="chip--ip chip">read</span></div>
    <div class="prob__title mt-1">can do what</div>
    <div class="prob__sub">a role — the set of allowed actions</div>
  </div>
  <div class="flex items-center"><span class="arrow" style="font-size:1.6rem">→</span></div>
  <div class="prob items-center text-center" style="width:235px">
    <div style="height:72px;display:flex;align-items:center"><img src="./assets/gcp/cloud_apis.svg" class="gcp gcp--lg" /></div>
    <div class="prob__title mt-1">on which resource</div>
    <div class="prob__sub">a specific service, database, bucket…</div>
  </div>
</div>

<div class="mt-7 inline-block chip" style="font-size:0.82rem;padding:0.5em 1.1em">
  allow <strong>analytics-sa@data-prod</strong> &nbsp;to&nbsp; <strong>invoke</strong> &nbsp;→&nbsp; <strong>reports-api</strong>
</div>

<p class="lead mt-5">Central, auditable, <em>identity-based</em> — no IP rules, no firewalls.</p>

---
transition: fade-out
---

<div class="kicker">In one line</div>
<h1 class="mt-3">What is <span class="grad-psc">Private Service Connect</span>?</h1>

<p class="lead mt-5 max-w-4xl">A consumer reaches a producer's service through a <strong>private endpoint in its own VPC</strong>. The producer <strong>publishes</strong> a service attachment and <strong>chooses who may connect</strong> — no VPC peering, no shared address space, neither side's network exposed.</p>

<div class="grid grid-cols-3 gap-5 mt-9">
  <div class="prob items-center text-center">
    <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg" />
    <div class="prob__title mt-2">Publish</div>
    <div class="prob__sub">producer exposes a service attachment</div>
  </div>
  <div class="prob items-center text-center">
    <img src="./assets/gcp/identity_and_access_management.svg" class="gcp gcp--lg" />
    <div class="prob__title mt-2">Authorize</div>
    <div class="prob__sub">the producer decides who connects</div>
  </div>
  <div class="prob items-center text-center">
    <img src="./assets/gcp/compute_engine.svg" class="gcp gcp--lg" />
    <div class="prob__title mt-2">Consume</div>
    <div class="prob__sub">a private endpoint IP in your own VPC</div>
  </div>
</div>

---
transition: fade-out
---

<div class="kicker">The key idea</div>
<h1 class="mt-2 !text-4xl">Authorize by <span class="grad-psc">policy</span>. Hide the network.</h1>

<div class="flex gap-6 items-stretch mt-4">
  <div class="prob flex-1">
    <div class="flex items-center gap-3">
      <img src="./assets/gcp/identity_and_access_management.svg" class="gcp" />
      <div class="prob__title !text-lg">Who may connect → the producer's accept-list</div>
    </div>
    <div class="flow tight mt-3">
      <div class="node node--glow"><img src="./assets/gcp/compute_engine.svg" class="gcp gcp--sm" /><div><div class="node__name">shop-prod</div><div class="node__sub">consumer</div></div><span class="mark mark--ok" style="margin-left:auto">✓ accepted</span></div>
      <div class="node"><img src="./assets/gcp/compute_engine.svg" class="gcp gcp--sm" /><div><div class="node__name">fin-prod</div><div class="node__sub">consumer</div></div><span class="mark mark--ok" style="margin-left:auto">✓ accepted</span></div>
      <div class="node" style="opacity:.6"><img src="./assets/gcp/compute_engine.svg" class="gcp gcp--sm" /><div><div class="node__name">any other</div><div class="node__sub">not on the list</div></div><span class="mark mark--x" style="margin-left:auto">✕ rejected</span></div>
    </div>
    <div class="prob__sub mt-3">Authorized by policy — not by IP ranges or firewall rules.</div>
  </div>

  <div class="prob flex-1">
    <div class="prob__title !text-lg mb-3">The producer's network → hidden</div>
    <div class="flow tight" style="opacity:.55;filter:grayscale(.25)">
      <div class="node"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><div><div class="node__name">VPC peering</div></div><span class="mark mark--x" style="margin-left:auto">not needed</span></div>
      <div class="node"><img src="./assets/gcp/cloud_network.svg" class="gcp gcp--sm" /><div><div class="node__name">overlapping CIDRs</div></div><span class="mark mark--x" style="margin-left:auto">gone</span></div>
      <div class="node"><img src="./assets/gcp/cloud_apis.svg" class="gcp gcp--sm" /><div><div class="node__name">their subnets &amp; routes</div></div><span class="mark mark--x" style="margin-left:auto">invisible</span></div>
    </div>
    <div class="prob__sub mt-3">Addresses are translated; you never see the other side's topology.</div>
  </div>
</div>

<p class="text-center text-lg mt-3"><strong>Which</strong> consumers may connect is policy — the producer's network stays <em>hidden</em>.</p>

---
transition: fade-out
---

<div class="kicker">Architecture</div>
<h1 class="mt-3">PSC: the key elements</h1>
<p class="lead mt-2 mb-5">How PSC implements it — brokered connection, translated addresses, access by policy.</p>

<div class="flex gap-8 items-stretch">
  <div class="grid grid-cols-2 gap-4 flex-1">
    <div class="prob">
      <div class="chip--ip chip self-start">01</div>
      <div class="prob__title mt-2">Consumer endpoint</div>
      <div class="prob__sub">A forwarding rule + internal IP inside your VPC. Traffic to the service enters here, at a local address you own.</div>
    </div>
    <div class="prob">
      <div class="chip--ip chip self-start">02</div>
      <div class="prob__title mt-2">Service attachment</div>
      <div class="prob__sub">The producer's published surface, fronted by an internal load balancer. It accepts or rejects each connection.</div>
    </div>
    <div class="prob">
      <div class="chip--ip chip self-start">03</div>
      <div class="prob__title mt-2">PSC NAT subnet</div>
      <div class="prob__sub">A dedicated producer-side subnet. Google source-NATs consumer traffic into it — so overlapping consumer IPs stop mattering.</div>
    </div>
    <div class="prob">
      <div class="chip--ip chip self-start">04</div>
      <div class="prob__title mt-2">Connection brokering</div>
      <div class="prob__sub">The producer accepts or rejects each consumer by project / identity — authorization, not firewall rules. One-way, no peering.</div>
    </div>
  </div>
  <div class="flow" style="flex:0 0 31%">
    <div class="node node--glow">
      <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--sm" />
      <div><div class="node__name">Endpoint <span class="tag">01</span></div><div class="node__sub">consumer VPC</div></div>
    </div>
    <div class="step">↓ &nbsp;<b>04</b> brokered · one-way</div>
    <div class="node node--attach">
      <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--sm" />
      <div><div class="node__name">Service attachment <span class="tag">02</span></div></div>
    </div>
    <div class="step">↓</div>
    <div class="node">
      <img src="./assets/gcp/cloud_network.svg" class="gcp gcp--sm" />
      <div><div class="node__name">PSC NAT subnet <span class="tag">03</span></div><div class="node__sub">source-NAT</div></div>
    </div>
    <div class="step">↓</div>
    <div class="node">
      <img src="./assets/gcp/cloud_apis.svg" class="gcp gcp--sm" />
      <div><div class="node__name">Service</div></div>
    </div>
  </div>
</div>

---
transition: fade-out
---

<div class="kicker">Calling it</div>
<h1 class="mt-3">Reach it by <span class="grad-psc">name</span>, not IP</h1>
<p class="lead mt-2 max-w-3xl">The endpoint is just a private IP — front it with DNS so callers use a stable hostname.</p>

<div class="flex items-center justify-center gap-4 mt-14">
  <div class="svc"><img src="./assets/gcp/compute_engine.svg" class="gcp gcp--lg" /><div class="svc__label">Client</div><div class="svc__meta">“payments.internal”</div></div>
  <span class="arrow" style="font-size:1.5rem">→</span>
  <div class="svc"><img src="./assets/gcp/cloud_dns.svg" class="gcp gcp--lg" /><div class="svc__label">Private DNS</div><div class="svc__meta">name → 10.0.1.9</div></div>
  <span class="arrow" style="font-size:1.5rem">→</span>
  <div class="svc"><img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg" /><div class="svc__label">PSC endpoint</div><div class="svc__meta">10.0.1.9</div></div>
  <span class="arrow" style="font-size:1.5rem">→</span>
  <div class="svc"><img src="./assets/gcp/cloud_apis.svg" class="gcp gcp--lg" /><div class="svc__label">Service</div><div class="svc__meta">10.0.1.9</div></div>
</div>

<p class="text-center dim mt-14">A Cloud DNS private zone (or Service Directory) maps the name to the endpoint — callers never hardcode an address.</p>

---
layout: center
class: text-center
transition: fade-out
---

<h1 class="mt-3">Takeaways</h1>

<div class="grid grid-cols-3 gap-5 mt-10 max-w-4xl">
  <div class="prob items-center text-center">
    <img src="./assets/gcp/identity_and_access_management.svg" class="gcp gcp--lg mx-auto" />
    <div class="prob__title mt-3">Authorize by identity</div>
    <div class="prob__sub">the producer accepts <em>who</em>, by project / IAM</div>
  </div>
  <div class="prob items-center text-center">
    <img src="./assets/gcp/cloud_network.svg" class="gcp gcp--lg mx-auto" />
    <div class="prob__title mt-3">Network abstracted</div>
    <div class="prob__sub">no CIDRs, peering, or firewall rules</div>
  </div>
  <div class="prob items-center text-center">
    <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg mx-auto" />
    <div class="prob__title mt-3">Publish &amp; consume</div>
    <div class="prob__sub">a private endpoint you own</div>
  </div>
</div>

<p class="mt-12"><strong>Who</strong> talks to <strong>whom</strong> is policy — not network plumbing.</p>

---
transition: fade-out
---

<div class="h-full flex flex-col">

<div class="kicker kicker--pain">Reality check</div>
<h1 class="mt-2 !text-4xl">Is PSC a <span class="grad-pain">silver bullet</span>?</h1>
<p class="dim mt-1 max-w-3xl">Not quite. Acceptance is <strong>project-level</strong> — you authorize a whole consumer project, not one workload.</p>

<div class="flex-1 flex flex-col justify-center">

<div class="flex gap-6 items-stretch">
  <div class="prob flex-1">
    <div class="prob__title !text-lg mb-3">What you'd love to write</div>
    <div style="font-family:var(--font-mono);font-size:0.82rem;line-height:1.7;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:0.7rem 0.9rem">accept from <strong>cart-service</strong><br/>in <strong>shop-prod</strong> — and nothing else</div>
    <div class="mark mark--x mt-3">✕ not expressible</div>
    <div class="prob__sub mt-1">per-service / per-identity acceptance isn't available</div>
  </div>
  <div class="prob flex-1">
    <div class="prob__title !text-lg mb-3">What PSC actually allows</div>
    <div style="font-family:var(--font-mono);font-size:0.82rem;line-height:1.7;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:0.7rem 0.9rem">accept connections from<br/>project <strong>shop-prod</strong></div>
    <div class="mark mark--ok mt-3">✓ project-level only</div>
    <div class="prob__sub mt-1">any workload in that project can connect</div>
  </div>
</div>

<p class="text-center text-lg mt-8">Want “only cart-service”? Enforce <em>caller identity</em> at the service — mTLS / IAM.</p>

</div>

</div>

---
layout: center
class: text-center
transition: fade-out
---

<div class="imground mx-auto mb-8" style="max-width:34rem"><img src="./assets/close.png" /></div>

<div class="text-3xl font-extrabold" style="font-family: var(--font-display); letter-spacing:-.04em;">
  Let's build it <span class="grad-psc">in the lab</span> →
</div>
