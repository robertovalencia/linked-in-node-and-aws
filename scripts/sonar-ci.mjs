// A fresh, isolated SonarQube server provides a release gate without a Cloud account.
// It reads real LCOV reports and never accesses laptop Sonar credentials or volumes.
import { randomBytes } from 'node:crypto';
import { chmod, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';

const project = `linked-in-node-ci-quality-${process.pid}`;
const projectKey = 'linked-in-node-and-aws';
const revision = spawnSync('git', ['rev-parse', 'HEAD'], {encoding:'utf8'});
if (revision.status !== 0 || !/^[a-f0-9]{40}$/.test(revision.stdout.trim())) throw new Error('Require a real Git source revision for release evidence');
const sourceSha = revision.stdout.trim();
const base = 'http://127.0.0.1:9292';
const output = resolve('work/ci-sonar');
// Same immutable amd64 scanner as local; native on GitHub, emulated on Apple silicon.
const scannerImage = 'sonarsource/sonar-scanner-cli@sha256:a3f4215076706c95a17a68c19322ee916e40a3acd081a8c1a1e839e0194afa57';
const env = { ...process.env, CI_SONAR_DB_PASSWORD: randomBytes(32).toString('hex') };
const compose = ['compose', '-p', project, '-f', 'compose.ci-quality.yaml'];
const password = `N!${randomBytes(32).toString('hex')}`;
let tokenIssued = false;
const tokenName = `ci-${Date.now()}`;
const tokenFile = resolve('work/ci-sonar-token.env');
const auth = pass => `Basic ${Buffer.from(`admin:${pass}`).toString('base64')}`;

function docker(args, options = {}) {
  const run = spawnSync('docker', args, { env, encoding: 'utf8', maxBuffer: 10_000_000, ...options });
  if (run.error || run.status !== 0) {
    throw new Error(`docker ${args.slice(0, 3).join(' ')} failed: ${run.error?.message ?? run.stderr ?? run.stdout}`);
  }
  return run.stdout;
}
async function api(path, body, pass = password) {
  const response = await fetch(`${base}${path}`, {
    method: body ? 'POST' : 'GET',
    headers: { Connection: 'close', Authorization: auth(pass), ...(body ? { 'Content-Type': 'application/x-www-form-urlencoded' } : {}) },
    ...(body ? { body: new URLSearchParams(body) } : {}),
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) throw new Error(`${path.split('?')[0]} returned HTTP ${response.status}`);
  const text = await response.text();
  return text ? JSON.parse(text) : {};
}
async function waitReady() {
  const deadline = Date.now() + 300000;
  while (Date.now() < deadline) {
    try { if ((await api('/api/system/status')).status === 'UP') return; } catch { /* Startup is expected. */ }
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  throw new Error('Isolated SonarQube not ready within 300 seconds');
}

await mkdir(output, { recursive: true });
// Refuse missing/empty coverage; Sonar must evaluate fresh test output, not assumptions.
for (const report of ['backend/coverage/lcov.info', 'frontend/coverage/lcov.info']) {
  const content = await readFile(report, 'utf8');
  if (!content.includes('SF:') || !content.includes('DA:')) throw new Error(`Missing LCOV data: ${report}`);
}
try {
  docker([...compose, 'up', '-d', '--wait', '--wait-timeout', '180', 'sonar-db']);
  docker([...compose, 'up', '-d', 'sonarqube']);
  await waitReady();
  await api('/api/users/change_password', { login: 'admin', previousPassword: 'admin', password }, 'admin');
  await api('/api/projects/create', { project: projectKey, name: 'Marketplace release verification' });
  // Copy Sonar Way unchanged, then add equivalent overall conditions: first scans have
  // no historical new-code baseline, so the entire analyzed source must meet the bar.
  const gateName = 'Marketplace release (Sonar way plus overall checks)';
  const gate = await api('/api/qualitygates/copy', { sourceName: 'Sonar way', name: gateName });
  for (const condition of [
    { metric: 'coverage', op: 'LT', error: '80' },
    { metric: 'violations', op: 'GT', error: '0' },
    { metric: 'duplicated_lines_density', op: 'GT', error: '3' },
    { metric: 'security_hotspots_reviewed', op: 'LT', error: '100' },
  ]) await api('/api/qualitygates/create_condition', { gateName, ...condition });
  await api('/api/qualitygates/select', { projectKey, gateName });
  const definition = await api(`/api/qualitygates/show?name=${encodeURIComponent(gateName)}`);
  await writeFile(`${output}/gate-definition.json`, JSON.stringify({ copiedFrom: 'Sonar way', copyResponse: gate, ...definition }, null, 2) + '\n');
  for (const [metric, op, error] of [
    ['new_coverage', 'LT', '80'], ['new_violations', 'GT', '0'],
    ['new_duplicated_lines_density', 'GT', '3'], ['new_security_hotspots_reviewed', 'LT', '100'],
  ]) if (!definition.conditions?.some(condition => condition.metric === metric && condition.op === op && condition.error === error)) {
    throw new Error(`Copied Sonar Way gate is missing required condition: ${metric}`);
  }
  tokenIssued = true;
  const generated = await api('/api/user_tokens/generate', { name: tokenName });
  await writeFile(tokenFile, `SONAR_TOKEN=${generated.token}\n`, { mode: 0o600 });
  const scannerDir = `${output}/scanner`;
  await rm(scannerDir, { recursive: true, force: true });
  await mkdir(scannerDir, { recursive: true });
  await chmod(scannerDir, 0o777);
  // Writable scanner temp is the only writable mount; source and Git metadata are read-only.
  const scan = spawnSync('docker', ['run', '--rm', '--platform', 'linux/amd64', '--network', `${project}_default`,
    '--env-file', tokenFile, '-e', 'SONAR_HOST_URL=http://sonarqube:9000', '-e', 'SONAR_USER_HOME=/tmp/.sonar',
    '-v', `${process.cwd()}:/usr/src:ro`, '-v', `${scannerDir}:/tmp/scan`, scannerImage,
    '-Dsonar.working.directory=/tmp/scan', '-Dsonar.qualitygate.timeout=300'],
  { encoding: 'utf8', maxBuffer: 10_000_000 });
  const scanLog = `${scan.stdout ?? ''}${scan.stderr ?? ''}`;
  process.stdout.write(scanLog);
  await writeFile(`${output}/scan.txt`, scanLog);
  const task = Object.fromEntries((await readFile(`${scannerDir}/report-task.txt`, 'utf8')).trim().split('\n').map(line => line.split('=', 2)));
  if (!task.ceTaskId) throw new Error('Fresh scanner did not report a CE task ID');
  let ce;
  const deadline = Date.now() + 300000;
  do {
    ce = await api(`/api/ce/task?id=${encodeURIComponent(task.ceTaskId)}`);
    if (['SUCCESS', 'FAILED', 'CANCELED'].includes(ce.task?.status)) break;
    if (Date.now() >= deadline) throw new Error('Fresh CE task timed out');
    await new Promise(resolve => setTimeout(resolve, 2000));
  } while (true);
  if (ce.task?.status !== 'SUCCESS' || !ce.task.analysisId) throw new Error(`Fresh CE task failed: ${ce.task?.status}`);
  const status = await api(`/api/qualitygates/project_status?analysisId=${encodeURIComponent(ce.task.analysisId)}`);
  await writeFile(`${output}/gate.json`, JSON.stringify({ sourceSha, ceTaskId: task.ceTaskId, analysisId: ce.task.analysisId, ...status }, null, 2) + '\n');
  const issues = await api(`/api/issues/search?componentKeys=${projectKey}&ps=100`);
  await writeFile(`${output}/issues.json`, JSON.stringify(issues, null, 2) + '\n');
  const overall = status.projectStatus?.conditions?.find(condition => condition.metricKey === 'coverage');
  if (scan.error || scan.status !== 0 || status.projectStatus?.status !== 'OK' || !overall || overall.comparator !== 'LT' || Number(overall.errorThreshold) !== 80 || !Number.isFinite(Number(overall.actualValue)) || Number(overall.actualValue) < 80) {
    throw new Error('Release SonarQube gate failed or did not evaluate the required 80% source coverage condition');
  }
  console.log(`Release SonarQube gate passed: ${overall.actualValue}% coverage, analysis ${ce.task.analysisId}`);
} finally {
  try {
    if (tokenIssued) await api('/api/user_tokens/revoke', { name: tokenName });
  } finally {
    await rm(tokenFile, { force: true });
    try { await writeFile(`${output}/server.log`, docker([...compose, 'logs', '--no-color'])); }
    finally { docker([...compose, 'down', '-v', '--remove-orphans']); }
  }
}
