---
theme: seriph
title: Private Service Connect in GCP
info: From VPC plumbing to service-oriented connectivity.
layout: default
class: text-left
transition: slide-left
mdc: true
fonts:
  sans: Hanken Grotesk
  display: Bricolage Grotesque
  mono: JetBrains Mono
  weights: '300,400,500,600,700,800'
---

<div class="flex items-stretch gap-12 h-full">
  <div class="flex-1 flex flex-col justify-center">
    <div class="kicker">GCP Networking · PSC Lab</div>
    <div class="flex items-center gap-4 mt-6">
      <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg" />
      <h1 class="!text-6xl !mb-0">Private <span class="grad-psc">Service Connect</span></h1>
    </div>
    <p class="lead mt-5 max-w-lg">Reach a private service across VPCs — without the network plumbing.</p>
    <div class="tag-row mt-8 items-center">
      <span class="svc !flex-row !py-2 !px-3 !min-w-0"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /> <span class="svc__label !text-sm">VPC peering</span></span>
      <span class="arrow">→</span>
      <span class="svc svc--glow !flex-row !py-2 !px-3 !min-w-0"><img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--sm" /> <span class="svc__label !text-sm">service-oriented</span></span>
    </div>
  </div>
  <div class="imgpanel" style="flex:1"><img src="./assets/gen/hero/title.png" /></div>
</div>

<!--
The problem, then the traditional peering setup and its costs, then PSC as a
publish/consume model.
-->

---
transition: fade-out
---

<div class="kicker">The problem</div>
<h1 class="mt-3">Two VPCs. One private call.</h1>
<p class="lead mt-2 mb-2 max-w-2xl">A client in one VPC needs a service in another — no public IP, different project, no shared routing.</p>

<div class="diagram !mt-10">
  <div class="vpc vpc--pain">
    <div class="vpc__title"><span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm inline" /> Consumer VPC</span></div>
    <div class="flex justify-center mt-5">
      <div class="svc"><img src="./assets/gcp/compute_engine.svg" class="gcp gcp--lg" /><div class="svc__label">Client</div><div class="svc__meta">wants the service</div></div>
    </div>
  </div>

  <div class="link gap">
    <div class="gap__q">?</div>
    <div class="barrier"></div>
    <div class="link__cap">no public IP<br/>different project<br/>no route between them</div>
  </div>

  <div class="vpc vpc--pain">
    <div class="vpc__title"><span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm inline" /> Producer VPC</span></div>
    <div class="flex justify-center mt-5">
      <div class="svc"><img src="./assets/gcp/cloud_apis.svg" class="gcp gcp--lg" /><div class="svc__label">Service</div><div class="svc__meta">private — by design</div></div>
    </div>
  </div>
</div>

<p v-click class="text-center text-xl mt-7 dim">How do you connect them <strong>privately</strong>?</p>

---
transition: slide-left
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
transition: slide-up
---

<div class="kicker kicker--pain">The cost</div>
<h1 class="mt-3">Why this hurts</h1>

<div class="grid grid-cols-3 gap-4 mt-7">

  <div class="prob">
    <div class="prob__viz">
      <div class="vmini"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp" /><span class="chip--pain chip">10.0.0.0/16</span></div>
      <div class="collide">⚡</div>
      <div class="vmini"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp" /><span class="chip--pain chip">10.0.0.0/16</span></div>
    </div>
    <div class="prob__title">CIDRs can't overlap</div>
    <div class="prob__sub">coordinate IPs with every team, forever</div>
  </div>

  <div class="prob">
    <div class="prob__viz stackrow !min-h-0">
      <div class="r"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><span class="conn conn--ok"></span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><span class="mark mark--ok">✓</span></div>
      <div class="r"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><span class="conn conn--ok"></span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><span class="mark mark--ok">✓</span></div>
      <div class="r"><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><span class="conn conn--bad"></span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm" /><span class="mark mark--x">✕</span></div>
    </div>
    <div class="prob__title">Peering isn't transitive</div>
    <div class="prob__sub">A↔B + B↔C ≠ A↔C — the mesh explodes</div>
  </div>

  <div class="prob">
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

  <div class="prob">
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

  <div class="prob">
    <div class="prob__viz">
      <img src="./assets/gcp/compute_engine.svg" class="gcp" />
      <span class="conn conn--bad !w-8"></span>
      <div class="exposed">
        <img src="./assets/gcp/cloud_network.svg" class="gcp gcp--sm" />
        <img src="./assets/gcp/cloud_apis.svg" class="gcp gcp--sm" />
      </div>
    </div>
    <div class="prob__title">Coupled to their topology</div>
    <div class="prob__sub">you must know their subnets &amp; IPs</div>
  </div>

  <div class="prob justify-center text-center" style="background:rgba(217,105,79,0.06);border-color:rgba(217,105,79,0.4)">
    <div class="text-lg">You wanted <strong>one service</strong>.</div>
    <div class="grad-pain text-2xl font-bold mt-1">You bought their<br/>whole network.</div>
  </div>

</div>

---
layout: center
class: text-center
transition: slide-left
---

<div class="kicker justify-center">The shift</div>

<img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg mx-auto mt-8" style="width:96px;height:96px" />

<h1 class="!text-5xl mt-6">Consume a <em>service</em>,<br/>not a <span class="grad-pain">network</span>.</h1>

<div v-click class="text-6xl font-extrabold grad-psc mt-8" style="font-family: var(--font-display); letter-spacing:-.04em;">
  Private Service Connect
</div>

---
transition: slide-left
---

<div class="kicker">The PSC model</div>
<h1 class="mt-3">Publish a service. Consume a <span class="grad-psc">local endpoint</span>.</h1>

<div class="diagram !mt-10">
  <div class="vpc vpc--consumer">
    <div class="vpc__title"><span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm inline" /> Consumer VPC</span><span class="chip">any CIDR</span></div>
    <div class="flex gap-3 justify-center mt-5">
      <div class="svc !py-3"><img src="./assets/gcp/compute_engine.svg" class="gcp" /><div class="svc__meta">Client</div></div>
      <div class="svc svc--glow !py-3"><img src="./assets/gcp/private_service_connect.svg" class="gcp" /><div class="svc__label !text-sm">Endpoint</div><div class="svc__meta">10.0.1.9</div></div>
    </div>
  </div>

  <div class="link">
    <div class="link__label grad-psc">PRIVATE</div>
    <div class="wire wire--clean"></div>
    <div class="link__cap">Google's fabric</div>
  </div>

  <div class="vpc vpc--producer opaque">
    <div class="veil"></div>
    <div class="vpc__title"><span><img src="./assets/gcp/virtual_private_cloud.svg" class="gcp gcp--sm inline" /> Producer VPC</span></div>
    <div class="flex gap-3 justify-center mt-5 items-stretch">
      <div class="svc !py-3 !min-w-0"><img src="./assets/gcp/private_service_connect.svg" class="gcp" /><div class="svc__meta">attachment</div></div>
      <div class="svc !py-3 !min-w-0"><img src="./assets/gcp/cloud_load_balancing.svg" class="gcp" /><div class="svc__meta">ILB</div></div>
      <div class="svc !py-3 !min-w-0"><img src="./assets/gcp/cloud_apis.svg" class="gcp" /><div class="svc__meta">service</div></div>
    </div>
  </div>
</div>

<p class="text-center dim mt-7">The VPCs <strong>never merge</strong>. You call an IP you own.</p>

---
transition: slide-left
---

<div class="kicker">Architecture</div>
<h1 class="mt-3">PSC: the key elements</h1>
<p class="lead mt-2 mb-5">Connectivity features built into GCP's VPC — not your routing.</p>

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
      <div class="prob__sub">Google's fabric brokers endpoint ↔ attachment. One-way, no peering; the producer controls accept / reject.</div>
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
layout: default
transition: fade
---

<div class="kicker">Head to head</div>
<h1 class="mt-3">Side by side</h1>

<table class="cmp mt-7">
  <thead>
    <tr><th></th><th>VPC Peering</th><th>Private Service Connect</th></tr>
  </thead>
  <tbody>
    <tr><td>Unit of connection</td><td>Whole network</td><td>A single service</td></tr>
    <tr><td>IP coordination</td><td>Required — no overlap</td><td>None — use your own IPs</td></tr>
    <tr><td>Routing exposed</td><td>Entire peered VPC</td><td>Just the endpoint</td></tr>
    <tr><td>Transitive</td><td>No — mesh explodes</td><td>N/A — endpoints independent</td></tr>
    <tr><td>Firewall rules</td><td>Per-consumer ranges</td><td>Local to the endpoint</td></tr>
    <tr><td>Coupling</td><td>Tight — topology-aware</td><td>Loose — service-oriented</td></tr>
  </tbody>
</table>

---
layout: center
class: text-center
transition: slide-up
---

<div class="kicker justify-center">Takeaways</div>

<div class="grid grid-cols-3 gap-5 mt-10 max-w-4xl">
  <div v-click class="prob items-center text-center">
    <img src="./assets/gcp/private_service_connect.svg" class="gcp gcp--lg mx-auto" />
    <div class="prob__title mt-3">Publish / consume</div>
    <div class="prob__sub">connectivity as a service</div>
  </div>
  <div v-click class="prob items-center text-center">
    <img src="./assets/gcp/cloud_network.svg" class="gcp gcp--lg mx-auto" />
    <div class="prob__title mt-3">No shared CIDRs</div>
    <div class="prob__sub">no mesh, no topology leak</div>
  </div>
  <div v-click class="prob items-center text-center">
    <img src="./assets/gcp/cloud_load_balancing.svg" class="gcp gcp--lg mx-auto" />
    <div class="prob__title mt-3">Local endpoint</div>
    <div class="prob__sub">an IP in your own VPC</div>
  </div>
</div>

<p v-click class="lead mt-12">Coupled at the <em>service</em> layer — not the <strong>network</strong>.</p>

---
layout: center
class: text-center
---

<div class="imground mx-auto mb-8" style="max-width:30rem"><img src="./assets/gen/hero/close.png" /></div>

<div class="text-6xl font-extrabold" style="font-family: var(--font-display); letter-spacing:-.04em;">
  Let's build it <span class="grad-psc">in the lab</span> →
</div>
