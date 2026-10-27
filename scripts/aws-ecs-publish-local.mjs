// Publish verified ECS image digests only. No ECS/SSM/Terraform apply operations.
import { spawnSync } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';

const root = fileURLToPath(new URL('..', import.meta.url));
process.chdir(root);
const repository = 'robertovalencia/linked-in-node-and-aws';
const runId = process.argv[2];
const env = { ...process.env, AWS_REGION: process.env.AWS_REGION || 'us-east-2' };
env.AWS_DEFAULT_REGION = env.AWS_REGION;
let evidence;
function requireThat(condition, message) { if (!condition) throw new Error(message); }
function execute(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: root, env, encoding: 'utf8', maxBuffer: 64_000_000, ...options });
  if (result.error || result.status !== 0) throw new Error(`${command} ${args[0] || ''} failed: ${result.error?.message || String(result.stderr || '').slice(0, 2000)}`);
  return result.stdout;
}
const json = (command, args) => JSON.parse(execute(command, args));
const saved = async (name, value) => writeFile(join(evidence, name), JSON.stringify(value, null, 2) + '\n');
function cleanSource(sha) {
  requireThat(execute('git', ['status', '--porcelain', '--untracked-files=all']).trim() === '', 'Require a clean Git checkout, including untracked source files');
  requireThat(execute('git', ['rev-parse', 'HEAD']).trim() === sha, 'Source revision changed during release');
}
function validateAcceptance(report) {
  requireThat(report.expected === 48 && report.passed === 48 && report.failed === 0 && report.results?.length === 48 && report.results.every(result => result.status === 'PASS'), 'CI acceptance evidence must contain exactly 48 PASS results and zero failures');
}
function validateSonar(gate, sha) {
  requireThat(gate.sourceSha === sha && gate.ceTaskId && gate.analysisId && gate.projectStatus?.status === 'OK', 'Require a successful Sonar analysis bound to this source revision');
  for (const [metric, comparator, threshold, check] of [
    ['coverage', 'LT', 80, value => value >= 80],
    ['violations', 'GT', 0, value => value === 0],
    ['duplicated_lines_density', 'GT', 3, value => value <= 3],
  ]) {
    const condition = gate.projectStatus.conditions?.find(item => item.metricKey === metric);
    requireThat(condition?.status === 'OK' && condition.comparator === comparator && Number(condition.errorThreshold) === threshold && Number.isFinite(Number(condition.actualValue)) && check(Number(condition.actualValue)), `Sonar did not enforce required overall ${metric} condition`);
  }
}
try {
  requireThat(/^\d+$/.test(runId || '') && process.argv.length === 3, 'Usage: AWS_PROFILE=marketplace-dev node scripts/aws-ecs-publish-local.mjs <successful-verification-run-id>');
  requireThat(env.AWS_PROFILE?.trim(), 'AWS_PROFILE must name a temporary AWS login profile');
  requireThat(/^[a-z]{2}-[a-z]+-\d+$/.test(env.AWS_REGION), 'Invalid AWS_REGION');
  const sha = execute('git', ['rev-parse', 'HEAD']).trim();
  requireThat(/^[a-f0-9]{40}$/.test(sha), 'Require a committed source revision');
  requireThat(execute('git', ['branch', '--show-current']).trim() === 'main', 'Local release must use main');
  const origin = execute('git', ['remote', 'get-url', 'origin']).trim();
  requireThat([`https://github.com/${repository}`, `https://github.com/${repository}.git`, `git@github.com:${repository}.git`].includes(origin), 'Git origin must be the independent marketplace repository');
  cleanSource(sha);
  requireThat(execute('trivy', ['--version']).split('\n').some(line => line.trim() === 'Version: 0.76.1'), 'Install the approved Trivy 0.76.1 binary and add its directory to PATH');
  execute('docker', ['info']);
  execute('docker', ['buildx', 'version']);
  evidence = join(root, 'work', 'local-ecs-publication', `${sha}-${runId}-${Date.now()}-${process.pid}`);
  await mkdir(evidence, {recursive:true});
  const run = json('gh', ['api', `repos/${repository}/actions/runs/${runId}`]);
  await saved('github-run.json', run);
  requireThat(String(run.id) === runId && run.path === '.github/workflows/deploy-dev.yml' && run.head_repository?.full_name === repository && run.head_sha === sha && run.head_branch === 'main' && run.event === 'workflow_dispatch' && run.status === 'completed' && run.conclusion === 'success', 'Require a successful Deploy AWS dev workflow_dispatch run for this exact repository/main/SHA');
  const jobs = json('gh', ['api', `repos/${repository}/actions/runs/${runId}/jobs?filter=latest`]);
  await saved('github-jobs.json', jobs);
  const verification = jobs.jobs?.filter(job => job.name === 'verify');
  const deployment = jobs.jobs?.filter(job => job.name === 'deploy');
  requireThat(verification?.length === 1 && verification[0].conclusion === 'success' && deployment?.length === 1 && deployment[0].conclusion === 'skipped', 'Require successful verification-only CI with the AWS deploy job skipped');
  const artifactDir = join(evidence, 'verification');
  execute('gh', ['run', 'download', runId, '--repo', repository, '--name', 'release-verification', '--dir', artifactDir]);
  const acceptance = JSON.parse(await readFile(join(artifactDir, 'work/release-acceptance.json'), 'utf8'));
  const gate = JSON.parse(await readFile(join(artifactDir, 'work/ci-sonar/gate.json'), 'utf8'));
  validateAcceptance(acceptance);
  validateSonar(gate, sha);
  const backendMetadata = JSON.parse(await readFile(join(root, 'infra/aws-ecs-dev/.terraform/terraform.tfstate'), 'utf8'));
  requireThat(backendMetadata.backend?.type === 's3' && backendMetadata.backend.config?.key === 'linked-in-node/ecs-dev/terraform.tfstate' && backendMetadata.backend.config?.bucket, 'Require initialized isolated AWS dev S3 Terraform state');
  requireThat(execute('terraform', ['-chdir=infra/aws-ecs-dev', 'workspace', 'show']).trim() === 'default', 'Require the default workspace with the explicit AWS dev state key');
  const outputs = json('terraform', ['-chdir=infra/aws-ecs-dev', 'output', '-json']);
  const value = name => outputs[name]?.value;
  const account = value('deployment_account_id');
  requireThat(/^\d{12}$/.test(account || ''), 'Terraform must output deployment_account_id');
  requireThat(value('deployment_region') === env.AWS_REGION, 'AWS_REGION does not match the Terraform deployment region');
  const caller = json('aws', ['sts', 'get-caller-identity', '--region', env.AWS_REGION, '--output', 'json']);
  requireThat(caller.Account === account, 'AWS login account does not match the reviewed Terraform deployment account');
  env.GITHUB_SHA = sha;
  const repos = value('repository_urls');
  const registry = `${account}.dkr.ecr.${env.AWS_REGION}.amazonaws.com`;
  const prefix = repos?.backend?.slice(registry.length + 1, -'/backend'.length);
  requireThat(/^[a-z][a-z0-9-]*-ecs-dev$/.test(prefix || '') && repos.backend === `${registry}/${prefix}/backend` && repos.frontend === `${registry}/${prefix}/frontend`, 'ECS repositories must belong to this account/region/namespace');
  requireThat(value('cluster_name') === prefix, 'Cluster and repositories must share the reviewed ECS namespace');
  await saved('release-context.json', {sourceSha:sha,verificationRunId:runId,analysisId:gate.analysisId,accountId:account,region:env.AWS_REGION,cluster:prefix,backend:repos.backend,frontend:repos.frontend,createdAt:new Date().toISOString()});
  cleanSource(sha);
  // All checks above are read-only. From here, ECR publication writes require explicit authorization. No service rollout is performed.
  const login = execute('aws', ['ecr', 'get-login-password', '--region', env.AWS_REGION]);
  execute('docker', ['login', '--username', 'AWS', '--password-stdin', registry], { input: login });
  const source = join(evidence, 'source');
  await mkdir(source);
  const archive = execute('git', ['archive', '--format=tar', sha, 'backend', 'frontend'], {encoding:null});
  execute('tar', ['-xf', '-', '-C', source], {input:archive});
  const emptyIgnore = join(evidence, 'empty.trivyignore');
  await writeFile(emptyIgnore, '');
  for (const [app, repo] of Object.entries(repos)) {
    const name = repo.slice(registry.length + 1);
    requireThat(execute('aws', ['ecr', 'describe-repositories', '--repository-names', name, '--region', env.AWS_REGION, '--query', 'repositories[0].imageTagMutability', '--output', 'text']).trim() === 'IMMUTABLE', 'ECR source tags must be immutable');
    const getDigest = () => {
      const result = json('aws', ['ecr', 'batch-get-image', '--repository-name', name, '--image-ids', `imageTag=${sha}`, '--region', env.AWS_REGION, '--output', 'json']);
      requireThat((result.failures || []).every(failure => failure.failureCode === 'ImageNotFound'), 'ECR image lookup failed');
      return result.images?.[0]?.imageId?.imageDigest;
    };
    let digest = getDigest();
    if (!digest) {
      cleanSource(sha);
      execute('docker', ['buildx', 'build', '--platform', 'linux/amd64', '--label', `org.opencontainers.image.revision=${sha}`, '--push', '--tag', `${repo}:${sha}`, '--metadata-file', join(evidence, `${app}-build.json`), join(source, app)]);
      digest = getDigest();
    }
    requireThat(/^sha256:[a-f0-9]{64}$/.test(digest || ''), 'ECR did not return a valid immutable image digest');
    const image = `${repo}@${digest}`;
    execute('docker', ['pull', '--platform', 'linux/amd64', image]);
    const inspection = json('docker', ['image', 'inspect', image]);
    await saved(`${app}-image.json`, inspection);
    requireThat(inspection.length === 1 && inspection[0].Architecture === 'amd64' && inspection[0].Os === 'linux' && inspection[0].Config?.Labels?.['org.opencontainers.image.revision'] === sha, 'Published image architecture/source label does not match the verified source');
    const scanFile = join(evidence, `${app}-image-scan.json`);
    execute('trivy', ['image', '--platform', 'linux/amd64', '--exit-code', '1', '--severity', 'HIGH,CRITICAL', '--ignore-unfixed=false', '--ignorefile', emptyIgnore, '--format', 'json', '--output', scanFile, image]);
    const scan = JSON.parse(await readFile(scanFile, 'utf8'));
    requireThat(scan.ArtifactName === image && Array.isArray(scan.Results) && scan.Results.length > 0 && scan.Results.every(result => (result.Vulnerabilities || []).every(vulnerability => !['HIGH','CRITICAL'].includes(vulnerability.Severity))), 'Trivy evidence is missing or contains HIGH/CRITICAL vulnerabilities');
    env[`${app.toUpperCase()}_IMAGE`] = image;
  }
  cleanSource(sha);
  await saved('publication-manifest.json', {sha, sourceSha:sha, verificationRunId:runId, region:env.AWS_REGION, account, cluster:prefix, backend:env.BACKEND_IMAGE, frontend:env.FRONTEND_IMAGE, deployed:false});
  console.log(`ECS images published and scanned for ${sha}; application NOT deployed; evidence: ${evidence}`);
} catch (error) {
  console.error(`Publication blocked: ${error.message}`);
  process.exitCode = 1;
}
