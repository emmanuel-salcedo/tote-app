from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["frontend"])


APP_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Tote Tracker</title>
    <style>
      :root {
        --bg: #f3efe8;
        --surface: #fffdf8;
        --ink: #1f2430;
        --muted: #616874;
        --line: #dfd9ce;
        --accent: #0a6a62;
        --accent-2: #e6f4f2;
        --danger: #a12f2f;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        color: var(--ink);
        font-family: "Avenir Next", "Segoe UI", sans-serif;
        background:
          radial-gradient(80rem 40rem at -20% -10%, #f9f5ee, transparent),
          radial-gradient(80rem 40rem at 120% -20%, #e8f5f3, transparent),
          var(--bg);
      }
      .shell {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 16px 36px;
      }
      .topbar {
        display: flex;
        gap: 12px;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
      }
      .brand {
        margin: 0;
        font-size: 1.4rem;
        letter-spacing: 0.02em;
      }
      .muted { color: var(--muted); }
      .btn {
        border: 1px solid var(--line);
        background: var(--surface);
        color: var(--ink);
        border-radius: 10px;
        padding: 8px 12px;
        font-weight: 600;
        cursor: pointer;
      }
      .btn.primary {
        background: var(--accent);
        color: #fff;
        border-color: transparent;
      }
      .btn.ghost {
        background: transparent;
      }
      .btn.danger {
        background: #fff5f5;
        color: var(--danger);
        border-color: #f0d9d9;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(12, minmax(0, 1fr));
        gap: 12px;
      }
      .card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
      }
      .card h2 {
        margin: 0 0 10px;
        font-size: 1rem;
      }
      .span-3 { grid-column: span 3; }
      .span-4 { grid-column: span 4; }
      .span-5 { grid-column: span 5; }
      .span-6 { grid-column: span 6; }
      .span-7 { grid-column: span 7; }
      .span-8 { grid-column: span 8; }
      .span-12 { grid-column: span 12; }
      label {
        display: block;
        font-size: 0.82rem;
        font-weight: 700;
        margin: 8px 0 5px;
      }
      input, textarea, select {
        width: 100%;
        border: 1px solid #cfc7ba;
        border-radius: 10px;
        background: #fff;
        padding: 9px 10px;
        color: var(--ink);
      }
      textarea { min-height: 74px; resize: vertical; }
      .row {
        display: flex;
        gap: 8px;
        align-items: center;
      }
      .row.wrap { flex-wrap: wrap; }
      .stack { display: grid; gap: 8px; }
      .list {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: #fff;
        overflow: auto;
        max-height: 320px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
      }
      th, td {
        border-bottom: 1px solid #eee6da;
        text-align: left;
        padding: 8px 10px;
        vertical-align: top;
      }
      th { background: #faf7f1; position: sticky; top: 0; z-index: 1; }
      .kpi {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
      }
      .pill {
        background: var(--accent-2);
        color: #0b4f48;
        border-radius: 999px;
        padding: 4px 9px;
        font-size: 0.76rem;
        font-weight: 700;
      }
      #status {
        margin-bottom: 10px;
        min-height: 22px;
      }
      .status-ok { color: #146d35; }
      .status-err { color: var(--danger); }
      .hidden { display: none !important; }
      .auth {
        max-width: 460px;
        margin: 7vh auto;
      }
      .nav {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 10px;
      }
      .nav button.active {
        background: #112f4b;
        color: #fff;
        border-color: transparent;
      }
      .section { display: none; }
      .section.active { display: block; }
      img.qr {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #fff;
        width: 190px;
        height: 190px;
        object-fit: contain;
      }
      @media (max-width: 980px) {
        .span-3, .span-4, .span-5, .span-6, .span-7, .span-8 { grid-column: span 12; }
        .kpi { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <div id="authCard" class="card auth">
        <h1 class="brand">Tote Tracker Login</h1>
        <p class="muted">Sign in to use inventory actions.</p>
        <label>Email</label>
        <input id="loginEmail" type="email" value="admin@example.com" />
        <label>Password</label>
        <input id="loginPassword" type="password" value="changeme" />
        <div class="row" style="margin-top: 10px;">
          <button id="loginBtn" class="btn primary">Login</button>
        </div>
      </div>

      <div id="appShell" class="hidden">
        <div class="topbar">
          <h1 class="brand">Tote Tracker</h1>
          <div class="row">
            <span id="whoami" class="pill">Session active</span>
            <button id="refreshBtn" class="btn ghost">Refresh</button>
            <button id="logoutBtn" class="btn danger">Logout</button>
          </div>
        </div>
        <div id="status"></div>

        <div class="nav">
          <button class="btn active" data-section="overview">Overview</button>
          <button class="btn" data-section="create">Create</button>
          <button class="btn" data-section="search">Search</button>
          <button class="btn" data-section="moves">Moves</button>
          <button class="btn" data-section="checkout">Checkout</button>
          <button class="btn" data-section="audit">Audit</button>
          <button class="btn" data-section="qr">QR</button>
        </div>

        <section id="section-overview" class="section active">
          <div class="kpi">
            <div class="card"><h2>Locations</h2><div id="countLocations">0</div></div>
            <div class="card"><h2>Totes</h2><div id="countTotes">0</div></div>
            <div class="card"><h2>Items</h2><div id="countItems">0</div></div>
          </div>
          <div class="grid" style="margin-top: 12px;">
            <div class="card span-6">
              <h2>Locations</h2>
              <div class="list"><table id="locationsTable"></table></div>
            </div>
            <div class="card span-6">
              <h2>Totes</h2>
              <div class="list"><table id="totesTable"></table></div>
            </div>
            <div class="card span-12">
              <h2>Items</h2>
              <div class="list"><table id="itemsTable"></table></div>
            </div>
          </div>
        </section>

        <section id="section-create" class="section">
          <div class="grid">
            <div class="card span-4">
              <h2>Create Location</h2>
              <label>Name</label><input id="newLocationName" />
              <label>Parent Location ID (optional)</label><input id="newLocationParentId" type="number" />
              <button id="createLocationBtn" class="btn primary" style="margin-top: 10px;">Create Location</button>
            </div>
            <div class="card span-4">
              <h2>Create Tote</h2>
              <label>Name (optional)</label><input id="newToteName" />
              <label>Location ID (optional)</label><input id="newToteLocationId" type="number" />
              <button id="createToteBtn" class="btn primary" style="margin-top: 10px;">Create Tote</button>
            </div>
            <div class="card span-4">
              <h2>Create Item</h2>
              <label>Name</label><input id="newItemName" />
              <label>Tote ID (optional)</label><input id="newItemToteId" type="number" />
              <label>Quantity</label><input id="newItemQuantity" type="number" value="1" />
              <label>Category</label><input id="newItemCategory" />
              <label>Notes</label><textarea id="newItemNotes"></textarea>
              <label><input id="newItemCheckoutable" type="checkbox" /> Checkoutable</label>
              <button id="createItemBtn" class="btn primary" style="margin-top: 10px;">Create Item</button>
            </div>
          </div>
        </section>

        <section id="section-search" class="section">
          <div class="card">
            <h2>Search Items</h2>
            <div class="row wrap">
              <input id="searchQuery" placeholder="search by item, tote, notes..." />
              <button id="searchBtn" class="btn primary">Search</button>
            </div>
            <div class="list" style="margin-top: 10px;"><table id="searchTable"></table></div>
          </div>
        </section>

        <section id="section-moves" class="section">
          <div class="grid">
            <div class="card span-6">
              <h2>Move Item to Tote</h2>
              <label>Item ID</label><input id="moveItemId" type="number" />
              <label>New Tote ID (blank to clear)</label><input id="moveItemToteId" type="number" />
              <button id="moveItemBtn" class="btn primary" style="margin-top: 10px;">Move Item</button>
            </div>
            <div class="card span-6">
              <h2>Move Tote to Location</h2>
              <label>Tote ID</label><input id="moveToteId" type="number" />
              <label>New Location ID (blank to clear)</label><input id="moveToteLocationId" type="number" />
              <button id="moveToteBtn" class="btn primary" style="margin-top: 10px;">Move Tote</button>
            </div>
          </div>
        </section>

        <section id="section-checkout" class="section">
          <div class="grid">
            <div class="card span-6">
              <h2>Check Out Item</h2>
              <label>Item ID</label><input id="checkoutItemId" type="number" />
              <label>Checked Out To</label><input id="checkoutTo" />
              <label>Due Back (optional)</label><input id="checkoutDue" type="datetime-local" />
              <label>Notes</label><textarea id="checkoutNotes"></textarea>
              <button id="checkoutBtn" class="btn primary" style="margin-top: 10px;">Check Out</button>
            </div>
            <div class="card span-6">
              <h2>Check In Item</h2>
              <label>Item ID</label><input id="checkinItemId" type="number" />
              <button id="checkinBtn" class="btn primary" style="margin-top: 10px;">Check In</button>
            </div>
          </div>
        </section>

        <section id="section-audit" class="section">
          <div class="card">
            <h2>Audit Log</h2>
            <div class="row">
              <input id="auditLimit" type="number" min="1" max="500" value="100" />
              <button id="loadAuditBtn" class="btn primary">Load</button>
            </div>
            <div class="list" style="margin-top: 10px;"><table id="auditTable"></table></div>
          </div>
        </section>

        <section id="section-qr" class="section">
          <div class="card">
            <h2>Tote QR</h2>
            <label>Tote ID</label>
            <div class="row">
              <input id="qrToteId" type="number" />
              <button id="loadQrBtn" class="btn primary">Load QR</button>
              <a id="printQrLink" class="btn" href="#" target="_blank" rel="noopener">Print Labels</a>
            </div>
            <div style="margin-top: 12px;">
              <img id="qrImage" class="qr hidden" alt="QR code" />
            </div>
          </div>
        </section>
      </div>
    </div>

    <script>
      const state = {
        locations: [],
        totes: [],
        items: [],
      };

      const $ = (id) => document.getElementById(id);

      function setStatus(message, isError = false) {
        const el = $("status");
        if (!el) return;
        el.className = isError ? "status-err" : "status-ok";
        el.textContent = message;
      }

      function toIntOrNull(value) {
        const trimmed = String(value || "").trim();
        if (!trimmed) return null;
        const num = Number(trimmed);
        return Number.isFinite(num) ? num : null;
      }

      function escapeHtml(value) {
        return String(value ?? "")
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#39;");
      }

      function row(cells) {
        return "<tr>" + cells.map((c) => `<td>${c}</td>`).join("") + "</tr>";
      }

      function header(cols) {
        return "<tr>" + cols.map((c) => `<th>${c}</th>`).join("") + "</tr>";
      }

      async function api(path, options = {}) {
        const res = await fetch(path, {
          credentials: "same-origin",
          headers: { "Content-Type": "application/json", ...(options.headers || {}) },
          ...options,
        });
        if (!res.ok) {
          let detail = res.statusText;
          try {
            const body = await res.json();
            detail = body.detail || JSON.stringify(body);
          } catch (_err) {}
          throw new Error(`${res.status}: ${detail}`);
        }
        const contentType = res.headers.get("content-type") || "";
        return contentType.includes("application/json") ? res.json() : res.text();
      }

      function switchSection(name) {
        if (!name) return;
        const section = document.getElementById(`section-${name}`) || document.getElementById("section-overview");
        const sectionName = section.id.replace("section-", "");
        document.querySelectorAll(".section").forEach((s) => s.classList.remove("active"));
        document.querySelectorAll(".nav .btn").forEach((b) => b.classList.remove("active"));
        section.classList.add("active");
        const button = document.querySelector(`.nav [data-section="${sectionName}"]`);
        if (button) button.classList.add("active");
        history.replaceState(null, "", `#${sectionName}`);
      }

      function renderOverview() {
        $("countLocations").textContent = String(state.locations.length);
        $("countTotes").textContent = String(state.totes.length);
        $("countItems").textContent = String(state.items.length);

        $("locationsTable").innerHTML = [
          header(["ID", "Name", "Path", "Parent"]),
          ...state.locations.map((loc) =>
            row([
              loc.id,
              escapeHtml(loc.name),
              escapeHtml(loc.path_string),
              loc.parent_id ?? "",
            ])
          ),
        ].join("");

        $("totesTable").innerHTML = [
          header(["ID", "No.", "Name", "Location", "QR"]),
          ...state.totes.map((tote) =>
            row([
              tote.id,
              tote.tote_number,
              escapeHtml(tote.tote_name || ""),
              tote.location_id ?? "",
              escapeHtml(tote.qr_value),
            ])
          ),
        ].join("");

        $("itemsTable").innerHTML = [
          header(["ID", "Name", "Tote", "Qty", "Category", "Status"]),
          ...state.items.map((item) =>
            row([
              item.id,
              escapeHtml(item.name),
              item.tote_id ?? "",
              item.quantity ?? "",
              escapeHtml(item.category || ""),
              escapeHtml(item.status || ""),
            ])
          ),
        ].join("");
      }

      async function refreshAll() {
        const [locations, totes, items] = await Promise.all([
          api("/locations"),
          api("/totes"),
          api("/items"),
        ]);
        state.locations = locations;
        state.totes = totes;
        state.items = items;
        renderOverview();
      }

      function showApp(loggedIn) {
        $("authCard").classList.toggle("hidden", loggedIn);
        $("appShell").classList.toggle("hidden", !loggedIn);
      }

      async function trySession() {
        try {
          await refreshAll();
          showApp(true);
          setStatus("Loaded inventory data.");
          return true;
        } catch (_err) {
          showApp(false);
          return false;
        }
      }

      async function onLogin() {
        try {
          const payload = {
            email: $("loginEmail").value.trim(),
            password: $("loginPassword").value,
          };
          const result = await api("/auth/login", { method: "POST", body: JSON.stringify(payload) });
          showApp(true);
          $("whoami").textContent = `${result.user.name} (${result.user.role})`;
          await refreshAll();
          setStatus("Login successful.");
        } catch (err) {
          setStatus(`Login failed: ${err.message}`, true);
        }
      }

      async function onLogout() {
        try {
          await api("/auth/logout", { method: "POST", body: "{}" });
        } catch (_err) {}
        showApp(false);
        setStatus("Logged out.");
      }

      async function createLocation() {
        const payload = {
          name: $("newLocationName").value.trim(),
          parent_id: toIntOrNull($("newLocationParentId").value),
        };
        if (!payload.name) throw new Error("Location name is required");
        await api("/locations", { method: "POST", body: JSON.stringify(payload) });
        await refreshAll();
        setStatus("Location created.");
      }

      async function createTote() {
        const payload = {
          tote_name: $("newToteName").value.trim() || null,
          location_id: toIntOrNull($("newToteLocationId").value),
        };
        await api("/totes", { method: "POST", body: JSON.stringify(payload) });
        await refreshAll();
        setStatus("Tote created.");
      }

      async function createItem() {
        const payload = {
          tote_id: toIntOrNull($("newItemToteId").value),
          name: $("newItemName").value.trim(),
          quantity: toIntOrNull($("newItemQuantity").value),
          category: $("newItemCategory").value.trim() || null,
          notes: $("newItemNotes").value.trim() || null,
          is_checkoutable: $("newItemCheckoutable").checked,
        };
        if (!payload.name) throw new Error("Item name is required");
        await api("/items", { method: "POST", body: JSON.stringify(payload) });
        await refreshAll();
        setStatus("Item created.");
      }

      async function runSearch() {
        const q = $("searchQuery").value.trim();
        if (!q) throw new Error("Search query is required");
        const results = await api(`/search?q=${encodeURIComponent(q)}&limit=80`);
        $("searchTable").innerHTML = [
          header(["Item", "Qty", "Category", "Tote", "Location"]),
          ...results.map((r) =>
            row([
              `${r.item_id}: ${escapeHtml(r.item_name)}`,
              r.quantity ?? "",
              escapeHtml(r.category || ""),
              r.tote_number ? `#${r.tote_number}` : "",
              escapeHtml(r.location_path || ""),
            ])
          ),
        ].join("");
        setStatus(`Search returned ${results.length} row(s).`);
      }

      async function moveItem() {
        const itemId = toIntOrNull($("moveItemId").value);
        if (!itemId) throw new Error("Item ID is required");
        const payload = { tote_id: toIntOrNull($("moveItemToteId").value) };
        await api(`/moves/items/${itemId}`, { method: "POST", body: JSON.stringify(payload) });
        await refreshAll();
        setStatus("Item moved.");
      }

      async function moveTote() {
        const toteId = toIntOrNull($("moveToteId").value);
        if (!toteId) throw new Error("Tote ID is required");
        const payload = { location_id: toIntOrNull($("moveToteLocationId").value) };
        await api(`/moves/totes/${toteId}`, { method: "POST", body: JSON.stringify(payload) });
        await refreshAll();
        setStatus("Tote moved.");
      }

      async function checkoutItem() {
        const itemId = toIntOrNull($("checkoutItemId").value);
        if (!itemId) throw new Error("Item ID is required");
        const dueRaw = $("checkoutDue").value.trim();
        const payload = {
          checked_out_to: $("checkoutTo").value.trim() || null,
          due_back_at: dueRaw ? new Date(dueRaw).toISOString() : null,
          notes: $("checkoutNotes").value.trim() || null,
        };
        await api(`/items/${itemId}/checkouts`, { method: "POST", body: JSON.stringify(payload) });
        await refreshAll();
        setStatus("Item checked out.");
      }

      async function checkinItem() {
        const itemId = toIntOrNull($("checkinItemId").value);
        if (!itemId) throw new Error("Item ID is required");
        await api(`/items/${itemId}/checkins`, { method: "POST", body: "{}" });
        await refreshAll();
        setStatus("Item checked in.");
      }

      async function loadAudit() {
        const limit = toIntOrNull($("auditLimit").value) || 100;
        const rows = await api(`/audit?limit=${limit}`);
        $("auditTable").innerHTML = [
          header(["Time", "Entity", "ID", "Action", "Actor"]),
          ...rows.map((r) =>
            row([
              escapeHtml(new Date(r.timestamp).toLocaleString()),
              escapeHtml(r.entity_type),
              r.entity_id,
              escapeHtml(r.action),
              r.actor_user_id ?? "",
            ])
          ),
        ].join("");
        setStatus(`Loaded ${rows.length} audit rows.`);
      }

      function loadQr() {
        const toteId = toIntOrNull($("qrToteId").value);
        if (!toteId) throw new Error("Tote ID is required");
        $("qrImage").src = `/totes/${toteId}/qr`;
        $("qrImage").classList.remove("hidden");
        $("printQrLink").href = `/totes/${toteId}/qr/print`;
        setStatus("QR loaded.");
      }

      function bindActions() {
        $("loginBtn").addEventListener("click", onLogin);
        $("logoutBtn").addEventListener("click", onLogout);
        $("refreshBtn").addEventListener("click", async () => {
          try {
            await refreshAll();
            setStatus("Refreshed.");
          } catch (err) {
            setStatus(`Refresh failed: ${err.message}`, true);
          }
        });

        document.querySelectorAll(".nav [data-section]").forEach((btn) => {
          btn.addEventListener("click", () => switchSection(btn.dataset.section));
        });

        const guarded = (fn) => async () => {
          try {
            await fn();
          } catch (err) {
            setStatus(err.message || String(err), true);
          }
        };

        $("createLocationBtn").addEventListener("click", guarded(createLocation));
        $("createToteBtn").addEventListener("click", guarded(createTote));
        $("createItemBtn").addEventListener("click", guarded(createItem));
        $("searchBtn").addEventListener("click", guarded(runSearch));
        $("moveItemBtn").addEventListener("click", guarded(moveItem));
        $("moveToteBtn").addEventListener("click", guarded(moveTote));
        $("checkoutBtn").addEventListener("click", guarded(checkoutItem));
        $("checkinBtn").addEventListener("click", guarded(checkinItem));
        $("loadAuditBtn").addEventListener("click", guarded(loadAudit));
        $("loadQrBtn").addEventListener("click", guarded(async () => loadQr()));
      }

      async function init() {
        bindActions();
        const initialSection = window.location.hash.replace("#", "").trim();
        if (initialSection) {
          switchSection(initialSection);
        }
        const hasSession = await trySession();
        if (!hasSession) {
          setStatus("Please log in.", true);
        }
      }

      init();
    </script>
  </body>
</html>
"""


@router.get("/app", response_class=HTMLResponse)
def app_page() -> HTMLResponse:
    return HTMLResponse(content=APP_HTML)
