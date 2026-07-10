const userPath = "../dataset/data/social_users.csv";
const connectionPath = "../dataset/data/social_connections.csv";
const benchmarkPath = "../dataset/benchmark/part2_benchmark_results.csv";

const palette = ["#8ecae6", "#b7e4c7", "#ffd166", "#cdb4db", "#a8dadc", "#f4a261"];
let graph = null;
let positions = {};
let communityColor = {};

async function loadCsv(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Cannot load ${path}`);
  return parseCsv(await response.text());
}

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines.shift().split(",");
  return lines.map((line) => {
    const values = line.split(",");
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

function buildGraph(users, edges) {
  const nodes = new Map();
  const following = new Map();
  const followers = new Map();
  users.forEach((row) => {
    const id = Number(row.user_id);
    nodes.set(id, { id, username: row.username, country: row.country, followerCount: 0 });
    following.set(id, new Set());
    followers.set(id, new Set());
  });

  edges.forEach((row) => {
    const follower = Number(row.follower_id);
    const followee = Number(row.followee_id);
    if (!nodes.has(follower) || !nodes.has(followee) || follower === followee) return;
    following.get(follower).add(followee);
    followers.get(followee).add(follower);
  });

  nodes.forEach((node, id) => {
    node.followerCount = followers.get(id).size;
  });
  return { nodes, following, followers };
}

function userIds() {
  return [...graph.nodes.keys()].sort((a, b) => a - b);
}

function setupControls() {
  const source = document.querySelector("#sourceSelect");
  const target = document.querySelector("#targetSelect");
  userIds().forEach((id) => {
    const label = `${id} ${graph.nodes.get(id).username}`;
    source.add(new Option(label, id));
    target.add(new Option(label, id));
  });
  source.value = graph.nodes.has(8) ? 8 : userIds()[0];
  target.value = graph.nodes.has(11) ? 11 : userIds().at(-1);

  document.querySelector("#pathBtn").addEventListener("click", showPath);
  document.querySelector("#communityBtn").addEventListener("click", showCommunities);
  document.querySelector("#recommendBtn").addEventListener("click", showRecommendations);
  document.querySelector("#resetBtn").addEventListener("click", () => renderGraph());
}

function computePositions() {
  const ids = userIds();
  const cx = 460;
  const cy = 310;
  const r = 245;
  ids.forEach((id, index) => {
    const angle = (2 * Math.PI * index) / ids.length;
    positions[id] = { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) };
  });
}

function renderStats() {
  const edgeCount = [...graph.following.values()].reduce((sum, set) => sum + set.size, 0);
  document.querySelector("#stats").textContent = `Users / 用户 ${graph.nodes.size} | Edges / 关系 ${edgeCount}`;
}

function renderGraph(options = {}) {
  const svg = document.querySelector("#graphSvg");
  svg.querySelectorAll("line,circle,text").forEach((item) => item.remove());

  const highlightNodes = options.highlightNodes || new Set();
  const highlightEdges = options.highlightEdges || new Set();
  const useCommunities = options.useCommunities || false;
  const maxFollowers = Math.max(1, ...[...graph.nodes.values()].map((node) => node.followerCount));
  const radii = new Map(userIds().map((id) => [id, nodeRadius(id, maxFollowers)]));

  graph.following.forEach((targets, source) => {
    targets.forEach((target) => {
      const points = edgePoints(source, target, radii);
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", points.x1);
      line.setAttribute("y1", points.y1);
      line.setAttribute("x2", points.x2);
      line.setAttribute("y2", points.y2);
      line.setAttribute("class", highlightEdges.has(`${source}-${target}`) ? "edge highlight" : "edge");
      svg.appendChild(line);
    });
  });

  userIds().forEach((id) => {
    const node = graph.nodes.get(id);
    const position = positions[id];
    const radius = radii.get(id);
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("class", highlightNodes.has(id) ? "node highlight" : "node");
    circle.setAttribute("cx", position.x);
    circle.setAttribute("cy", position.y);
    circle.setAttribute("r", radius);
    circle.setAttribute("fill", useCommunities ? communityColor[id] || "#e5e7eb" : "#dbeafe");
    circle.appendChild(svgTitle(`${node.username}, followers=${node.followerCount}`));
    svg.appendChild(circle);

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("class", "node-label");
    label.setAttribute("x", position.x);
    label.setAttribute("y", position.y + 4);
    label.textContent = id;
    svg.appendChild(label);
  });
}

function nodeRadius(id, maxFollowers) {
  const node = graph.nodes.get(id);
  return 12 + Math.round((20 * node.followerCount) / maxFollowers);
}

function edgePoints(source, target, radii) {
  const a = positions[source];
  const b = positions[target];
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const distance = Math.max(Math.hypot(dx, dy), 1);
  const startPad = radii.get(source) + 2;
  const endPad = radii.get(target) + 8;
  return {
    x1: a.x + (dx / distance) * startPad,
    y1: a.y + (dy / distance) * startPad,
    x2: b.x - (dx / distance) * endPad,
    y2: b.y - (dy / distance) * endPad,
  };
}

function svgTitle(text) {
  const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
  title.textContent = text;
  return title;
}

function shortestPath(source, target) {
  if (source === target) return [source];
  const queue = [source];
  const parent = new Map([[source, null]]);
  while (queue.length) {
    const current = queue.shift();
    for (const next of graph.following.get(current)) {
      if (parent.has(next)) continue;
      parent.set(next, current);
      if (next === target) return buildPath(parent, target);
      queue.push(next);
    }
  }
  return [];
}

function buildPath(parent, target) {
  if (!parent.has(target)) return [];
  const path = [];
  for (let current = target; current !== null; current = parent.get(current)) path.push(current);
  return path.reverse();
}

function showPath() {
  const source = Number(document.querySelector("#sourceSelect").value);
  const target = Number(document.querySelector("#targetSelect").value);
  const path = shortestPath(source, target);
  const edgeSet = new Set(path.slice(1).map((id, index) => `${path[index]}-${id}`));
  renderGraph({ highlightNodes: new Set(path), highlightEdges: edgeSet });
  output(`Path / 路径: ${path.length ? path.join(" -> ") : "None / 无"}\nDegrees / 间隔: ${path.length ? path.length - 1 : "N/A"}`);
}

function stronglyConnectedComponents() {
  let index = 0;
  const stack = [];
  const onStack = new Set();
  const indices = new Map();
  const lowlinks = new Map();
  const components = [];

  function visit(id) {
    indices.set(id, index);
    lowlinks.set(id, index);
    index += 1;
    stack.push(id);
    onStack.add(id);

    graph.following.get(id).forEach((next) => {
      if (!indices.has(next)) {
        visit(next);
        lowlinks.set(id, Math.min(lowlinks.get(id), lowlinks.get(next)));
      } else if (onStack.has(next)) {
        lowlinks.set(id, Math.min(lowlinks.get(id), indices.get(next)));
      }
    });

    if (lowlinks.get(id) === indices.get(id)) {
      const component = [];
      let member = null;
      do {
        member = stack.pop();
        onStack.delete(member);
        component.push(member);
      } while (member !== id);
      components.push(component.sort((a, b) => a - b));
    }
  }

  userIds().forEach((id) => {
    if (!indices.has(id)) visit(id);
  });
  return components.sort((a, b) => b.length - a.length || a[0] - b[0]);
}

function colorCommunities(components) {
  communityColor = {};
  components.forEach((component, index) => {
    if (component.length === 1) return;
    component.forEach((id) => {
      communityColor[id] = palette[index % palette.length];
    });
  });
}

function showCommunities() {
  const components = stronglyConnectedComponents();
  const strong = components.filter((group) => group.length > 1);
  const singletons = components.length - strong.length;
  colorCommunities(components);
  renderGraph({ useCommunities: true });
  output(
    [
      ...strong.map((group, index) => `Community ${index + 1} / 社群${index + 1}: ${group.join(", ")}`),
      `Single users / 单点: ${singletons}`,
    ].join("\n"),
  );
}

function recommend(userId, limit = 3) {
  const followed = graph.following.get(userId);
  const counts = new Map();
  followed.forEach((followee) => {
    graph.following.get(followee).forEach((candidate) => {
      if (candidate !== userId && !followed.has(candidate)) {
        counts.set(candidate, (counts.get(candidate) || 0) + 1);
      }
    });
  });

  return [...counts.keys()]
    .sort((a, b) => counts.get(b) - counts.get(a) || graph.nodes.get(b).followerCount - graph.nodes.get(a).followerCount || a - b)
    .slice(0, limit)
    .map((id) => ({ id, mutual: counts.get(id), followers: graph.nodes.get(id).followerCount }));
}

function showRecommendations() {
  const source = Number(document.querySelector("#sourceSelect").value);
  const recs = recommend(source);
  renderGraph({ highlightNodes: new Set([source, ...recs.map((item) => item.id)]) });
  output(
    recs.length
      ? [`Source / 起点: ${source}`, ...recs.map((item) => `${item.id} ${graph.nodes.get(item.id).username}: mutual=${item.mutual}, followers=${item.followers}`)].join("\n")
      : "No friend-of-friend / 无朋友的朋友推荐",
  );
}

function output(text) {
  document.querySelector("#output").textContent = text;
}

async function drawBenchmark() {
  const svg = document.querySelector("#benchmarkSvg");
  try {
    const rows = await loadCsv(benchmarkPath);
    const metrics = ["insert_seconds", "construction_seconds", "degree_seconds", "scc_seconds", "path_seconds"];
    const xs = rows.map((row) => Number(row.users));
    const maxX = Math.max(...xs);
    const maxY = Math.max(...rows.flatMap((row) => metrics.map((key) => Number(row[key]))));
    drawAxes(svg);
    metrics.forEach((metric, index) => {
      const points = rows
        .map((row) => {
          const x = 36 + (290 * Number(row.users)) / maxX;
          const y = 182 - (150 * Number(row[metric])) / Math.max(maxY, 0.000001);
          return `${x},${y}`;
        })
        .join(" ");
      const polyline = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
      polyline.setAttribute("class", "plot-line");
      polyline.setAttribute("stroke", palette[index]);
      polyline.setAttribute("points", points);
      svg.appendChild(polyline);
    });
  } catch {
    svg.textContent = "";
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("class", "plot-label");
    text.setAttribute("x", 24);
    text.setAttribute("y", 42);
    text.textContent = "Run benchmark first / 先运行性能测试";
    svg.appendChild(text);
  }
}

function drawAxes(svg) {
  svg.textContent = "";
  const xAxis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  xAxis.setAttribute("class", "plot-axis");
  xAxis.setAttribute("x1", 34);
  xAxis.setAttribute("y1", 184);
  xAxis.setAttribute("x2", 330);
  xAxis.setAttribute("y2", 184);
  svg.appendChild(xAxis);

  const yAxis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  yAxis.setAttribute("class", "plot-axis");
  yAxis.setAttribute("x1", 34);
  yAxis.setAttribute("y1", 28);
  yAxis.setAttribute("x2", 34);
  yAxis.setAttribute("y2", 184);
  svg.appendChild(yAxis);
}

async function init() {
  try {
    const [users, connections] = await Promise.all([loadCsv(userPath), loadCsv(connectionPath)]);
    graph = buildGraph(users, connections);
    computePositions();
    setupControls();
    renderStats();
    colorCommunities(stronglyConnectedComponents());
    renderGraph();
    output("Ready / 已就绪");
    drawBenchmark();
  } catch (error) {
    output(`${error.message}\nUse a local server / 请用本地服务器打开`);
  }
}

init();
